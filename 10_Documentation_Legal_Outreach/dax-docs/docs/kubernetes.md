# Kubernetes Primer for the DAX Project

Kubernetes (abbreviated **K8s**) is an open-source system for automating the deployment, scaling, and management of containerized applications. In this project, Kubernetes is the **runtime orchestrator** that manages containerized DAX services after they have been built with Docker and validated locally.

**Critical clarification:** Kubernetes is **not** a Manus plugin. Manus coordinates the workflow that produces deployment files and images; Kubernetes is the separate system that consumes those artifacts and runs them in a cluster.

---

## Plain-English Explanation

Think of Kubernetes as a very capable supervisor for a fleet of containers. You describe what you want — "run 2 copies of `dax-api`, restart them if they crash, and expose them on port 80" — and Kubernetes makes it happen and keeps it that way. You do not SSH into individual servers; you declare desired state in YAML files and apply them with `kubectl`.

Docker is the packaging step. Kubernetes is the running step. You cannot skip Docker and go straight to Kubernetes.

---

## Kubernetes Object Map

The table below covers every Kubernetes object relevant to this project, with a plain-English purpose and guidance on when to use it.

| Object | Plain-English Purpose | When to Use in DAX |
|---|---|---|
| **Namespace** | A virtual partition inside a cluster. Keeps DAX resources separate from other workloads. | Always. Use `dax-system` for all DAX objects. |
| **Deployment** | Declares how many copies of a container to run and how to update them. | For every long-running DAX service (e.g., `dax-api`, `dax-worker`). |
| **Service** | A stable network address that routes traffic to the correct pods, even as pods restart. | For every Deployment that needs to receive network traffic. |
| **Ingress** | An HTTP router that maps external URLs to internal Services. Requires an Ingress Controller. | When you need to expose a Service to the internet or to other clusters via HTTP/HTTPS. |
| **ConfigMap** | Stores non-sensitive configuration as key-value pairs or files. | For environment variables like `DAX_ENV`, `LOG_LEVEL`, `DAX_API_PORT`. |
| **Secret** | Stores sensitive data (base64-encoded). Not encrypted by default; use external secret managers in production. | For `DATABASE_URL`, `MODEL_API_KEY`, `SECRET_KEY`, `REDIS_URL`. |
| **PersistentVolumeClaim (PVC)** | Requests durable storage that survives pod restarts. | For Postgres data, model weights, or any state that must persist. |
| **Job** | Runs a container to completion once. | For one-off tasks: database migrations, data import, audit snapshots. |
| **CronJob** | Runs a Job on a schedule. | For recurring tasks: nightly audit sweeps, log rotation, health reports. |
| **HorizontalPodAutoscaler (HPA)** | Automatically scales the number of pod replicas based on CPU/memory metrics. | **Phase 6 only.** Do not configure HPA until the service is stable, observable, and load-tested. |

---

## Local Kubernetes First-Run Checklist

Before applying any manifest to a local cluster, complete the following steps in order.

**Tool installation**

- [ ] Install Docker Desktop, minikube, or kind — pick one and stick with it locally.
- [ ] Install `kubectl` and verify it is on your PATH: `kubectl version --client`.
- [ ] If using minikube: `minikube start --driver=docker` and confirm `minikube status`.
- [ ] If using kind: `kind create cluster --name dax-local` and confirm `kubectl cluster-info`.

**Pre-flight checks**

- [ ] `kubectl get nodes` returns at least one node in `Ready` state.
- [ ] `kubectl get namespaces` shows the default namespaces (`default`, `kube-system`).
- [ ] Your `kubeconfig` is pointing at the local cluster, not a production cluster. Verify: `kubectl config current-context`.
- [ ] The `dax-api` Docker image has been built locally and is accessible to the cluster (see note below).

> **Local image access note:** By default, a local Kubernetes cluster cannot pull images from your local Docker daemon. With minikube, run `eval $(minikube docker-env)` before building, or use `minikube image load your-registry/dax-api:latest`. With kind, use `kind load docker-image your-registry/dax-api:latest --name dax-local`.

**Namespace and first deployment**

- [ ] Apply the namespace: `kubectl apply -f examples/k8s/namespace.yaml`
- [ ] Apply the ConfigMap: `kubectl apply -f examples/k8s/dax-api-configmap.yaml`
- [ ] Apply the Deployment: `kubectl apply -f examples/k8s/dax-api-deployment.yaml`
- [ ] Apply the Service: `kubectl apply -f examples/k8s/dax-api-service.yaml`
- [ ] Confirm pods are running: `kubectl get pods -n dax-system`
- [ ] Check logs: `kubectl logs -n dax-system deployment/dax-api`
- [ ] Port-forward and test the health endpoint:

```bash
kubectl port-forward -n dax-system svc/dax-api 8080:80
curl http://localhost:8080/health
```

---

## Minimal dax-api Deployment Example

This is the minimal Deployment manifest for `dax-api`. See `examples/k8s/dax-api-deployment.yaml` for the full annotated version.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dax-api
  namespace: dax-system
  labels:
    app: dax-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: dax-api
  template:
    metadata:
      labels:
        app: dax-api
    spec:
      containers:
        - name: dax-api
          # Replace with your actual registry and tag
          image: your-registry/dax-api:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8000
          envFrom:
            - configMapRef:
                name: dax-api-config
            - secretRef:
                name: dax-api-secrets
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 15
            periodSeconds: 20
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 10
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
```

---

## Minimal dax-api Service Example

```yaml
apiVersion: v1
kind: Service
metadata:
  name: dax-api
  namespace: dax-system
  labels:
    app: dax-api
spec:
  type: ClusterIP
  selector:
    app: dax-api
  ports:
    - name: http
      port: 80
      targetPort: 8000
      protocol: TCP
```

Access this service from within the cluster at `http://dax-api.dax-system.svc.cluster.local`.

---

## Local-Only Warnings

The following behaviors apply to local Kubernetes setups and differ significantly from production:

- **Image pull policy:** Use `imagePullPolicy: IfNotPresent` locally. In production, use `Always` with a pinned image tag (never `latest`).
- **No persistent storage by default:** Local clusters may not have a storage provisioner. PVCs may remain in `Pending` state until one is configured.
- **LoadBalancer Services do not work locally** without additional tooling (e.g., `minikube tunnel` or MetalLB). Use `ClusterIP` + `kubectl port-forward` for local access.
- **Resource limits are advisory locally.** Your laptop may not enforce them the same way a production node does.
- **LM Studio is not reachable from inside the cluster by default.** If `dax-api` needs to call a local LM Studio instance, you must configure the model endpoint to use the host machine's IP (e.g., `host.docker.internal` on Docker Desktop, or the minikube host IP). Do not assume `localhost` inside a pod refers to your laptop.

---

## Production Caveats

> **[SPECULATIVE]** The following applies to future cloud deployment. Do not act on these until Phase 6 of the roadmap is reached.

- **Never use `latest` image tags in production.** Pin to a specific digest or semantic version tag.
- **Enable RBAC.** Ensure service accounts have only the permissions they need. Do not run pods as `root`.
- **Use a proper Secrets manager.** Kubernetes Secrets are base64-encoded, not encrypted at rest by default. Use AWS Secrets Manager, GCP Secret Manager, HashiCorp Vault, or the Kubernetes External Secrets Operator.
- **Set resource requests and limits on every container.** Without them, a runaway pod can starve other services.
- **Configure network policies.** By default, all pods in a cluster can communicate with each other. Restrict this.
- **Do not expose `kubeconfig` files.** Store them securely and never commit them to version control.
- **Ingress requires an Ingress Controller** (e.g., nginx-ingress, Traefik). It is not built into Kubernetes itself.
- **HPA requires the Metrics Server** to be installed in the cluster before it can function.
- **Cloud Kubernetes and local LM Studio do not connect by default.** If the model endpoint is cloud-hosted, it must be explicitly configured with the correct URL, authentication, and network access rules.
