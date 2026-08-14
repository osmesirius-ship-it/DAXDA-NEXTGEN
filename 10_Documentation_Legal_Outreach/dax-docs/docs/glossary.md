
# Glossary

This glossary provides plain-English definitions for key terms used in the DAX + Manus + Kubernetes orchestration project documentation. These definitions aim to be beginner-accessible and builder-oriented.

---

### API (Application Programming Interface)
A set of defined rules that enable different software applications to communicate with each other. In the context of DAX, it refers to the interface through which other services or users interact with DAX functionalities, such as its `/health` endpoint.

### Cluster
A group of interconnected computers (nodes) that work together as a single system. In Kubernetes, a cluster is the foundation for running containerized applications, providing high availability and scalability.

### ConfigMap
A Kubernetes object used to store non-confidential data in key-value pairs. It allows you to decouple configuration artifacts from image content, making applications more portable and easier to manage.

### Container
A lightweight, standalone, executable package of software that includes everything needed to run an application: code, runtime, system tools, system libraries, and settings. Docker is a popular technology for creating and managing containers.

### DAX
The core service being built and deployed, functioning as the reasoning, governance, and recursive audit engine for the project. It provides critical functionalities for ensuring compliance and operational integrity.

### Deployment
A Kubernetes object that manages a replicated set of pods, ensuring that a specified number of replicas are running at any given time. It handles rolling updates and rollbacks, providing declarative updates to applications.

### Docker
A platform that enables developers to package applications into containers. It provides tools to build, distribute, and run containerized applications efficiently, ensuring consistency across different environments. Docker/containerization must precede Kubernetes in the workflow.

### Ingress
A Kubernetes object that manages external access to services within a cluster, typically HTTP. It provides load balancing, SSL termination, and name-based virtual hosting, routing traffic to the correct service.

### Kubernetes
An open-source system for automating deployment, scaling, and management of containerized applications. It orchestrates containerized DAX services after local validation, but it is not a Manus plugin.

### LM Studio
A local environment for running large language models (LLMs) on your own machine. It facilitates local development and testing of AI applications, requiring explicit networking decisions to connect with cloud services like Kubernetes.

### Manus
The autonomous build and workflow coordinator for the project. Manus helps coordinate builds, audits, documentation generation, and deployment file creation, but it is NOT a runtime orchestrator and NOT a Kubernetes plugin.

### Model endpoint
A network address where a trained machine learning model is exposed for inference requests. Access to model endpoints should be carefully managed and secured, avoiding casual exposure.

### Namespace
A virtual cluster within a Kubernetes cluster, used to divide cluster resources among multiple users or teams. Namespaces provide a scope for names and allow for resource isolation and access control.

### Node
A worker machine in a Kubernetes cluster, which can be a virtual machine or a physical computer. Each node runs pods and is managed by the Kubernetes control plane.

### Pod
The smallest deployable unit in Kubernetes, representing a single instance of a running process in a cluster. A pod typically encapsulates one or more containers, storage resources, a unique network IP, and options that govern how the containers should run.

### Queue
A data structure used for storing and managing tasks or messages in a specific order, typically first-in, first-out (FIFO). In distributed systems, queues are essential for decoupling services and handling asynchronous processing, such as for worker tasks.

### Secret
A Kubernetes object used to store sensitive information, such as passwords, OAuth tokens, and SSH keys. Secrets are designed to be more secure than ConfigMaps for confidential data, but their exposure must still be carefully controlled.

### Service
A Kubernetes object that defines a logical set of pods and a policy by which to access them. Services enable network access to a set of pods, providing a stable IP address and DNS name regardless of pod changes.

### Telemetry
The process of collecting and transmitting data from remote sources to a central location for monitoring and analysis. In the context of DAX, telemetry would provide insights into the system's health, performance, and operational metrics.

### Worker
A component or process responsible for executing specific tasks, often asynchronously, from a queue. In the DAX system, workers would handle computational tasks or background jobs, separate from the main API service.