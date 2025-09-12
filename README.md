# Simple Flask HelloWorld -> Kubernetes (step-by-step)

## What is included
- `app.py` : small Flask app that returns "Hello from Kubernetes!"
- `Dockerfile`
- `requirements.txt`
- `k8s/deployment.yaml` and `k8s/service.yaml`
- `.dockerignore`

## Prerequisites
- Git, Docker, kubectl
- Either **minikube** or **kind** (local k8s)
- VSCode (optional, but recommended)
- (Optional) A container registry (Docker Hub, GHCR, ECR) if you want to push images

## Quick local test (in VSCode terminal)
1. Create a virtualenv (optional) and install:
   ```
   python -m venv venv
   source venv/bin/activate   # on PowerShell: venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   python app.py
   ```
   Visit: http://localhost:8080

## Docker (build & run)
```
docker build -t myapp:dev .
docker run -p 8080:8080 myapp:dev
curl http://localhost:8080
```

## Deploy to Kubernetes (minikube) - option A
1. Start minikube (driver docker):
   ```
   minikube start --driver=docker
   ```
2. Use minikube's docker daemon so images are available to the cluster:
   ```
   eval $(minikube -p minikube docker-env)
   docker build -t myapp:dev .
   ```
3. Apply manifests:
   ```
   kubectl apply -f k8s/
   ```
4. Expose/test:
   ```
   minikube service myapp --url
   # or
   kubectl port-forward svc/myapp 8080:80
   curl http://localhost:8080
   ```

## Deploy to Kubernetes (kind) - option B
1. Create cluster:
   ```
   kind create cluster
   ```
2. Build image and load into kind:
   ```
   docker build -t myapp:dev .
   kind load docker-image myapp:dev --name kind
   ```
3. Apply manifests:
   ```
   kubectl apply -f k8s/
   kubectl port-forward svc/myapp 8080:80
   curl http://localhost:8080
   ```

## Push image to a registry (if using remote k8s)
1. Tag & push:
   ```
   docker tag myapp:dev ghcr.io/<your-org>/myapp:v1
   docker push ghcr.io/<your-org>/myapp:v1
   ```
2. Update `k8s/deployment.yaml` image field:
   ```yaml
   image: ghcr.io/<your-org>/myapp:v1
   ```
   Then:
   ```
   kubectl apply -f k8s/deployment.yaml
   ```

## Optional GitOps (ArgoCD) short notes
1. Install ArgoCD:
   ```
   kubectl create namespace argocd
   kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
   ```
2. Create a Git repo with the `k8s/` folder (the GitOps repo).
3. Create an ArgoCD Application pointing to that repo and path; ArgoCD will sync the manifests.

## Want CI (Jenkins/GitHub Actions)?
- Let me know and I'll add a sample `Jenkinsfile` / GitHub Actions workflow that:
  1. builds the image
  2. pushes to registry
  3. updates the GitOps repo (or directly applies k8s manifests)

----
Good luck — agar chaahe to main Jenkinsfile + ArgoCD Application bhi bana ke de sakta hoon.
