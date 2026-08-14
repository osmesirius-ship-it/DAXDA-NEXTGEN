# Docker for DAX: Containerization Fundamentals

Before diving into the complexities of orchestrating services with Kubernetes, it's crucial to understand and implement containerization using Docker. Docker serves as the foundational layer, packaging our applications and their dependencies into isolated, portable units called containers. This document outlines why Docker is a prerequisite for Kubernetes, provides a practical Dockerfile example for the `dax-api` service, details a `docker-compose.yml` structure for local development, and offers guidance on `.dockerignore`.

## Why Docker Precedes Kubernetes

**Containerization (`Docker`) MUST precede Orchestration (`Kubernetes`).** This is a fundamental principle in modern cloud-native development. Docker provides the mechanism to create self-contained, runnable units (containers) that encapsulate an application and its environment. Kubernetes, on the other hand, is an orchestration system designed to manage, scale, and deploy these pre-packaged containers across a cluster of machines.

Think of it this way:

*   **Docker:** You wouldn't try to manage a fleet of cars (Kubernetes) if you hadn't first built the individual cars themselves (Docker containers). Docker ensures that each service, like our `dax-api`, runs consistently regardless of the underlying infrastructure.
*   **Isolation and Portability:** Docker containers provide process isolation, ensuring that our `dax-api` service runs in a consistent environment, free from conflicts with other applications or host system configurations. This portability is key for moving from local development to production environments.
*   **Dependency Management:** All application dependencies are bundled within the container, eliminating "it works on my machine" scenarios. This simplifies deployment and debugging.

Manus, our autonomous build/workflow coordinator, facilitates the creation of these Docker images and deployment files. However, it's important to reiterate that **Manus is NOT a runtime orchestrator and NOT a Kubernetes plugin**. Similarly, **Kubernetes is not a Manus plugin**; it operates independently to manage the containerized services.

## Dockerfile Pattern for `dax-api`

For Python-based services like `dax-api`, a multi-stage Dockerfile is highly recommended. This approach allows us to use a larger base image with build tools to compile dependencies, and then copy only the necessary artifacts into a smaller, production-ready runtime image. This results in smaller, more secure, and faster-to-deploy images.

Here's a suggested `Dockerfile` for a simple `dax-api` service, focusing on a basic `/health` endpoint as a starting point:

```dockerfile
# Stage 1: Build dependencies
FROM python:3.11-slim-bookworm as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Create final runtime image
FROM python:3.11-slim-bookworm

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy application code
COPY . .

# Expose the port our API will run on
EXPOSE 8000

# Define environment variables (example)
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**`requirements.txt` example:**

```
fastapi==0.111.0
uvicorn==0.30.1
```

**`app/main.py` example (simple `/health` endpoint):**

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Docker Compose Structure for Local Development

Docker Compose is an excellent tool for defining and running multi-container Docker applications locally. It allows us to spin up all necessary services (like `dax-api`, databases, etc.) with a single command. This structure is ideal for local validation before deploying to Kubernetes.

```yaml
version: '3.8'

services:
  dax-api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      # Example environment variables; avoid exposing sensitive credentials directly
      DATABASE_URL: postgres://user:password@postgres:5432/dax_db
      REDIS_URL: redis://redis:6379/0
    depends_on:
      - postgres
      - redis
    # > **[SPECULATIVE]** Add health checks for robust local development
    # healthcheck:
    #   test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
    #   interval: 30s
    #   timeout: 10s
    #   retries: 3

  dax-worker:
    # > **[PLACEHOLDER]** This service will process background tasks.
    # > It will likely depend on Redis for a message queue and Postgres for data.
    build:
      context: ./dax-worker # Assuming dax-worker has its own Dockerfile in a subdirectory
      dockerfile: Dockerfile
    environment:
      DATABASE_URL: postgres://user:password@postgres:5432/dax_db
      REDIS_URL: redis://redis:6379/0
    depends_on:
      - postgres
      - redis
    # command: python worker.py # Example command

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: dax_db
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"

  dashboard:
    # > **[PLACEHOLDER]** This service will provide a UI for monitoring or interaction.
    # > It might be a simple web server or a more complex frontend application.
    # build:
    #   context: ./dashboard
    #   dockerfile: Dockerfile
    image: nginx:alpine # Example placeholder image
    ports:
      - "80:80"
    depends_on:
      - dax-api

volumes:
  postgres_data:
  redis_data:
```

## Build, Test, and Run Commands

Here are the essential Docker commands for managing your services locally:

### Build Images

To build the `dax-api` image (or any service with a `Dockerfile` in the current directory):

```bash
docker build -t dax-api:latest .
```

To build all services defined in `docker-compose.yml`:

```bash
docker compose build
```

### Run Services (Local Development)

To start all services defined in `docker-compose.yml` in detached mode:

```bash
docker compose up -d
```

To view logs for all services:

```bash
docker compose logs -f
```

To stop and remove all services, networks, and volumes defined in `docker-compose.yml`:

```bash
docker compose down -v
```

### Test the `dax-api` Health Endpoint

After running `docker compose up -d`, you can test the `dax-api` health endpoint:

```bash
curl http://localhost:8000/health
# Expected output: {"status": "ok"}
```

## `.dockerignore` Guidance

A `.dockerignore` file is crucial for optimizing Docker builds. It prevents unnecessary files and directories from being copied into your Docker image, leading to smaller image sizes, faster builds, and improved security. It works similarly to `.gitignore`.

Create a file named `.dockerignore` in the root of your project (alongside your `Dockerfile` and `docker-compose.yml`).

```
# Ignore Git-related files
.git
.gitignore

# Ignore Python-specific files and directories
__pycache__/
*.pyc
*.pyo
*.pyd
.pytest_cache/
.venv/
virtualenv/
venv/

# Ignore local development files
.env
.vscode/
*.log

# Ignore Docker-specific files (except Dockerfile itself)
docker-compose.yml
Dockerfile

# Ignore documentation files (if not needed in the final image)
docs/
README.md

# Ignore any temporary or sensitive files
*.tmp
*.bak
```

By carefully managing your `.dockerignore` file, you ensure that your Docker images are lean and contain only what's essential for your application to run.