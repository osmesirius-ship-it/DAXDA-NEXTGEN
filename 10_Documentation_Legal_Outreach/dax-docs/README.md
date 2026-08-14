# DAX + Manus + Kubernetes Orchestration Project

This repository contains the documentation and deployment artifacts for the DAX reasoning engine, coordinated by Manus and eventually orchestrated by Kubernetes.

---

## Project Overview

DAX is an AI reasoning, governance, and recursive audit engine. This project establishes the workflow for building, containerizing, and deploying DAX services in a structured, secure, and observable way. The development sequence is deliberate: build the service first, containerize it second, validate it locally third, and only then consider Kubernetes.

Manus coordinates the build and deployment workflow. Kubernetes orchestrates the running containers. These are separate tools with separate responsibilities.

---

## What is DAX?

**DAX** is the core service being built and deployed. It functions as a reasoning engine, governance layer, and recursive audit system for AI operations. DAX is responsible for:

- Processing and evaluating AI model inputs and outputs
- Enforcing governance rules and compliance policies
- Maintaining an auditable, traceable record of decisions
- Exposing a stable API that other services and operators can query

DAX is the thing being deployed. Everything else in this project exists to support its development and operation.

---

## What Manus Does and Does Not Do

**Manus** is an autonomous build and workflow coordinator. In this project, Manus is used to:

- Trigger and coordinate Docker builds
- Run audit workflows against code and artifacts
- Generate documentation
- Produce Kubernetes deployment YAML files from templates
- Coordinate multi-step deployment preparation tasks

**Manus does NOT:**

- Serve as a runtime orchestrator for live services
- Act as a Kubernetes plugin or controller
- Replace `kubectl`, Helm, or any Kubernetes-native tooling
- Make autonomous production deployment decisions without human approval

Manus operates in the build and preparation layer. Kubernetes operates in the runtime layer. They do not overlap.

---

## What Kubernetes Does and Does Not Do

**Kubernetes** is an open-source system for automating the deployment, scaling, and management of containerized applications. In this project, Kubernetes:

- Runs containerized DAX services as Pods
- Ensures the desired number of replicas are always running
- Routes network traffic to healthy pods via Services
- Restarts failed containers automatically
- Manages configuration and secrets injection

**Kubernetes does NOT:**

- Build Docker images (that is Docker's job)
- Coordinate the build workflow (that is Manus's job)
- Write code or generate deployment files (Manus assists with that)
- Connect automatically to local tools like LM Studio without explicit network configuration

---

## High-Level Architecture

```
  Developer
      |
      | writes code, triggers Manus workflows
      v
  Manus (Coordinator)
  +-- triggers Docker builds
  +-- runs audit checks
  +-- generates deployment YAML
  +-- hands off to human for review
      |
      | human reviews and approves
      v
  Docker (Containerization)
  +-- dax-api image
  +-- dax-worker image
  +-- local validation via docker-compose
      |
      | after local validation passes
      v
  Kubernetes (Runtime Orchestration)
  +-- Namespace: dax-system
  +-- Deployment: dax-api (2 replicas)
  +-- Service: dax-api (ClusterIP)
  +-- ConfigMap: dax-api-config
  +-- Secret: dax-api-secrets
  +-- [future] dax-worker, HPA, Ingress, PVC
      |
      | services running in cluster
      v
  Supporting Infrastructure
  +-- Redis (queue)
  +-- Postgres (storage)
  +-- Telemetry (metrics/logs)
  +-- Model endpoint (LM Studio local or cloud LLM)
```

---

## Repository File Tree

```
.
+-- README.md
+-- docs/
|   +-- architecture.md       # System model, component roles, data flow
|   +-- orchestration.md      # Manus workflow coordination guide
|   +-- kubernetes.md         # K8s primer, object map, local setup
|   +-- docker.md             # Dockerfile patterns, Compose setup
|   +-- security.md           # Credential rules, secrets, network warnings
|   +-- roadmap.md            # Phase-by-phase build plan
|   +-- glossary.md           # Plain-English definitions
|   +-- checklists.md         # Pre-K8s, local K8s, security, production
+-- examples/
    +-- .env.example
    +-- docker-compose.yml
    +-- k8s/
        +-- namespace.yaml
        +-- dax-api-configmap.yaml
        +-- dax-api-deployment.yaml
        +-- dax-api-service.yaml
```

---

## Quickstart

Follow these steps in order. Do not skip ahead to Kubernetes until each prior step is complete and validated.

**Step 1: Build the dax-api service**

Create a minimal FastAPI application with a `/health` endpoint:

```python
# dax-api/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
```

Run it locally without Docker first:

```bash
cd dax-api
pip install fastapi uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000
curl http://localhost:8000/health
# Expected: {"status": "ok"}
```

**Step 2: Write a Dockerfile**

```dockerfile
# dax-api/Dockerfile
FROM python:3.11-slim AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and test the container:

```bash
docker build -t dax-api:latest ./dax-api
docker run --rm -p 8000:8000 dax-api:latest
curl http://localhost:8000/health
```

**Step 3: Add Docker Compose**

Copy the example files and run the full local stack:

```bash
cp examples/docker-compose.yml ./docker-compose.yml
cp examples/.env.example ./.env
# Edit .env with your actual values before proceeding
docker compose up --build
curl http://localhost:8000/health
```

**Step 4: Local Kubernetes (only after Steps 1-3 pass)**

See `docs/kubernetes.md` and `docs/checklists.md` for the full local K8s checklist before running any of the following:

```bash
kubectl apply -f examples/k8s/namespace.yaml
kubectl apply -f examples/k8s/dax-api-configmap.yaml
kubectl apply -f examples/k8s/dax-api-deployment.yaml
kubectl apply -f examples/k8s/dax-api-service.yaml
kubectl port-forward -n dax-system svc/dax-api 8080:80
curl http://localhost:8080/health
```

---

## Current Development Stage

This project is in **Phase 1** of the roadmap: building the local DAX API with a `/health` endpoint. Kubernetes deployment is a future phase. See `docs/roadmap.md` for the full phase plan with success criteria and blockers for each stage.

> **First concrete action:** Create `dax-api/main.py` with a `/health` endpoint and `dax-api/Dockerfile`. Validate both locally before writing a single line of Kubernetes YAML.

---

## Documentation Index


| File                    | Purpose                                                  |
| ----------------------- | -------------------------------------------------------- |
| `docs/architecture.md`  | Full system model, component roles, architecture diagram |
| `docs/orchestration.md` | How to use Manus for build/deploy coordination           |
| `docs/kubernetes.md`    | K8s primer, object map, local setup checklist            |
| `docs/docker.md`        | Dockerfile patterns, Docker Compose guide                |
| `docs/security.md`      | Credential rules, secrets management, network warnings   |
| `docs/roadmap.md`       | Phase-by-phase development plan                          |
| `docs/glossary.md`      | Plain-English definitions for all key terms              |
| `docs/checklists.md`    | Actionable checklists for each deployment stage          |


