
# Orchestration with Manus: Coordinating DAX Build/Deploy Workflows

This document outlines how Manus, as an autonomous build/workflow coordinator, integrates with the DAX reasoning engine and Kubernetes for deployment. It focuses on defining clear coordination mechanisms, prompt templates for Manus, expected outputs, human approval checkpoints, and areas explicitly excluded from current automation.

## Manus's Role in DAX Build/Deploy Workflows

Manus acts as the central coordinator for the DAX project's build, audit, documentation generation, and deployment file creation processes. It is crucial to understand that **Manus is NOT a runtime orchestrator and NOT a Kubernetes plugin**. Its function is to manage the workflow leading up to deployment, ensuring that all prerequisites are met and artifacts are correctly generated and validated. The workflow emphasizes a clear separation of concerns: Docker for containerization, Manus for workflow coordination, and Kubernetes for runtime orchestration of containerized services.

**Key Principles:**

*   **Containerization First:** All DAX services MUST be containerized using Docker before any Kubernetes deployment. This ensures portability and consistency.
*   **Workflow Coordination, Not Runtime:** Manus orchestrates the *process* of building and deploying, not the *execution* of services in a live environment.
*   **Explicit Hand-offs:** Clear hand-off points are defined between Manus-coordinated tasks and Kubernetes deployments, often involving human approval.
*   **Security by Design:** Sensitive information like `kubeconfig`, API keys, cloud credentials, or model endpoints are never exposed casually within automated workflows.
*   **Start Simple:** The initial focus is on deploying a simple DAX API `/health` endpoint before progressing to more complex components like workers, dashboards, or autoscaling.

## Manus Prompt Templates

Manus utilizes specific prompt templates to trigger various stages of the DAX build/deploy workflow. These templates ensure consistency and provide all necessary context for Manus to execute its tasks effectively.

### 1. Build Trigger Prompt Template

This template initiates the build process for a specified DAX service, including Docker image creation and initial validation.

```yaml
# Prompt Template: Build Trigger
name: "Build Trigger for DAX Service"
description: "Initiates the Docker build process for a specific DAX service."
inputs:
  - name: DAX_SERVICE_NAME
    type: string
    description: "The name of the DAX service to build (e.g., dax-api)."
  - name: GIT_REPOSITORY_URL
    type: string
    description: "The URL of the Git repository containing the service code."
  - name: GIT_BRANCH_OR_TAG
    type: string
    description: "The branch or tag to build from."
  - name: PATH_TO_DOCKERFILE
    type: string
    description: "The path to the Dockerfile within the repository."
task: >
  Build a Docker image for the service {{DAX_SERVICE_NAME}} using the code from {{GIT_REPOSITORY_URL}} at {{GIT_BRANCH_OR_TAG}}.
  Use the Dockerfile located at {{PATH_TO_DOCKERFILE}}.
  Run all associated unit tests.
  If tests pass, push the resulting image to the designated container registry.
expected_output: >
  - The final Docker image tag.
  - A summary of the unit test results.
  - A direct link to the pushed image in the container registry.
```

### 2. Audit Trigger Prompt Template

This template triggers an audit of a specific DAX service or a set of generated artifacts, ensuring compliance and quality before further progression.

```yaml
# Prompt Template: Audit Trigger
name: "Audit Trigger for DAX Artifacts"
description: "Initiates an audit of specified DAX artifacts (code, images, configs)."
inputs:
  - name: SCOPE_OF_AUDIT
    type: string
    description: "A brief description of what is being audited."
  - name: LIST_OF_ARTIFACTS_TO_AUDIT
    type: list
    description: "Specific artifacts to review (e.g., Docker image tags, YAML file paths)."
  - name: TYPE_OF_AUDIT
    type: string
    description: "The focus of the audit (e.g., Security Scan, Code Review)."
task: >
  Perform a {{TYPE_OF_AUDIT}} on the following artifacts: {{LIST_OF_ARTIFACTS_TO_AUDIT}}.
  The scope of this audit is: {{SCOPE_OF_AUDIT}}.
  Evaluate the artifacts against established DAX security and quality standards.
expected_output: >
  - A detailed audit report document (Markdown format).
  - A prioritized list of identified issues, including severity assessments.
  - A clear Pass/Fail recommendation for the audited artifacts.
```

### 3. Deployment File Generation Prompt Template

This template instructs Manus to generate Kubernetes deployment files (e.g., YAML) for a given DAX service, based on predefined templates and configuration.

```yaml
# Prompt Template: Deployment File Generation
name: "Deployment File Generation for DAX Service"
description: "Generates Kubernetes YAML manifests for deploying a DAX service."
inputs:
  - name: DAX_SERVICE_NAME
    type: string
    description: "The name of the DAX service."
  - name: ENVIRONMENT
    type: string
    description: "The target deployment environment (e.g., staging, production)."
  - name: DOCKER_IMAGE_TAG
    type: string
    description: "The specific Docker image tag to deploy."
task: >
  Generate Kubernetes deployment YAML files for the service {{DAX_SERVICE_NAME}} intended for the {{ENVIRONMENT}} environment.
  Use the container image {{DOCKER_IMAGE_TAG}}.
  Ensure the generated files adhere to the standard DAX Kubernetes templates, including appropriate resource requests/limits and basic networking setup.
expected_output: >
  - The complete Kubernetes YAML files (Deployment, Service, and potentially Ingress).
  - A brief summary of the generated resources.
```

## Expected Manus Task Outputs

For each coordinated task, Manus is expected to produce structured and easily consumable outputs. These outputs serve as inputs for subsequent stages or as records for auditing and human review.

*   **Build Tasks:**
    *   Docker image tag (e.g., `registry.example.com/dax-api:1.0.0`)
    *   Unit test results (summary and detailed logs)
    *   Link to container registry artifact
    *   Build logs

*   **Audit Tasks:**
    *   Comprehensive audit report (Markdown format)
    *   List of identified issues with severity and recommendations
    *   Pass/Fail status for the audit

*   **Deployment File Generation Tasks:**
    *   Kubernetes YAML files (e.g., `deployment.yaml`, `service.yaml`, `ingress.yaml`)
    *   Checksums or hashes of generated files for integrity verification
    *   Summary of generated resources

## Human Approval Checkpoints

To maintain control and ensure critical decisions are reviewed, specific human approval checkpoints are integrated into the workflow. These checkpoints prevent automated progression without explicit human consent.

| Stage | Description | Required Approver(s) | Action Required |
| :--- | :--- | :--- | :--- |
| **Initial `/health` Endpoint Deployment** | The very first deployment of the basic `/health` endpoint to a production Kubernetes cluster. | Lead Engineer / DevOps | Manual review of generated YAML and manual execution of `kubectl apply`. |
| **Production Deployment File Review** | Review of Manus-generated Kubernetes YAML files intended for the production environment. | DevOps / SRE | Review YAML for correctness, resource limits, and security configurations before applying. |
| **Audit Failure Override** | Proceeding with a workflow despite a failed automated audit. | Security Lead / Project Manager | Explicit sign-off acknowledging and accepting the risks identified in the audit report. |
| **Model Endpoint Exposure** | Configuration and exposure of sensitive model endpoints within Kubernetes. | Security Lead / AI Lead | Manual review and approval of the networking and security configuration for the endpoint. |

## What NOT to Automate Yet (Explicit List)

To ensure stability, security, and human oversight, the following aspects of the DAX + Manus + Kubernetes workflow are explicitly **NOT** to be automated at this stage. These require manual intervention and approval.

*   **Initial DAX API `/health` Endpoint Deployment to Production:** The very first deployment of the basic `/health` endpoint to a production Kubernetes cluster MUST be a manual process, thoroughly validated by human operators.
*   **`kubeconfig` Management:** Direct manipulation or automated generation of `kubeconfig` files by Manus is prohibited. Access to Kubernetes clusters remains under strict human control.
*   **Cloud Credential Rotation:** Automation of cloud credential rotation (e.g., AWS IAM keys, GCP service account keys) is out of scope for Manus. This sensitive operation requires dedicated security processes.
*   **Model Endpoint Configuration (Sensitive):** While deployment files can be generated, the final configuration and exposure of sensitive model endpoints (e.g., for proprietary AI models) within Kubernetes MUST involve manual review and approval.
*   **Autoscaling Policy Adjustments:** Dynamic adjustment of Kubernetes autoscaling policies (e.g., Horizontal Pod Autoscaler, Cluster Autoscaler) based on real-time metrics is not yet automated by Manus. These changes require careful analysis and human decision-making.
*   **Database Schema Migrations:** Automated execution of database schema migrations is explicitly excluded. These operations carry significant risk and require human review and rollback planning.
*   **Rollback Initiation:** While Manus can assist in preparing rollback artifacts, the decision and initiation of a production rollback in Kubernetes MUST be a human-triggered event.
*   **Local LM Studio Networking Configuration:** The networking setup for local LM Studio instances to connect with DAX services is a manual configuration task. Manus will not attempt to automate this complex local environment setup.
*   **Kubernetes Cluster Provisioning/Deprovisioning:** The creation or deletion of Kubernetes clusters themselves is a high-impact operation and remains outside Manus's automation scope.

> **[PLACEHOLDER]** Further areas for potential future automation will be identified and evaluated based on system maturity and operational confidence. Prioritization will be given to low-risk, high-frequency tasks.