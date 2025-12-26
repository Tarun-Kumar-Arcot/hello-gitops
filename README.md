# 🚀 GitOps CI/CD Pipeline with GitHub Actions, GHCR, Kubernetes & Argo CD

## 📌 Project Overview

This project demonstrates a **real-world GitOps-based CI/CD pipeline** for deploying a containerized Python application to Kubernetes using:

* **GitHub Actions** for CI
* **GitHub Container Registry (GHCR)** for image storage
* **Kubernetes** for orchestration
* **Argo CD** for GitOps-based continuous deployment

The pipeline follows **industry best practices** such as immutable image tags, private container registry authentication, and declarative infrastructure.

---

## 🧱 Architecture

```
Developer Push (GitHub)
        |
        v
GitHub Actions (CI)
  - Build Docker Image
  - Push to GHCR
  - Update Kubernetes manifest (image tag)
        |
        v
Git Repository (GitOps Source of Truth)
        |
        v
Argo CD
  - Detects manifest change
  - Syncs to Kubernetes cluster
        |
        v
Kubernetes Cluster
  - Pulls image from GHCR
  - Runs application Pods
```

---

## 📁 Repository Structure

```
hello-gitops/
├── app/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── k8s/
│   ├── namespace.yaml
│   ├── deployment.yaml
│   └── service.yaml
├── argocd/
│   └── application.yaml
├── .github/
│   └── workflows/
│       └── ci-build-push.yaml
└── README.md
```

---

## 🛠️ Technologies Used

* **Python** – Sample application
* **Docker** – Containerization
* **GitHub Actions** – CI pipeline
* **GitHub Container Registry (GHCR)** – Private image registry
* **Kubernetes** – Container orchestration
* **Argo CD** – GitOps deployment tool

---

## 🔁 CI/CD Workflow (GitHub Actions)

### Trigger

* Runs on every push to `main` branch
* Only when files under `app/` or workflow files change

### CI Steps

1. Checkout code
2. Build Docker image
3. Push image to **GHCR**
4. Tag image with:

   * `latest`
   * Git commit SHA
5. Automatically update Kubernetes manifest with new image tag
6. Commit updated manifest back to Git (GitOps pattern)

---

## 🔐 Container Registry Authentication (Key Learning)

GHCR images are **private by default**, so Kubernetes requires authentication.

### Solution Implemented

1. Created GHCR pull secret:

```bash
kubectl -n hello create secret docker-registry ghcr-pull-secret \
  --docker-server=ghcr.io \
  --docker-username=<github-username> \
  --docker-password=<github-token> \
  --docker-email=<email>
```

2. Patched Kubernetes ServiceAccount:

```bash
kubectl -n hello patch serviceaccount default \
  -p '{"imagePullSecrets":[{"name":"ghcr-pull-secret"}]}'
```

3. Restarted deployment to create new pods:

```bash
kubectl -n hello rollout restart deploy/hello-app
```

📌 **Important Insight**:
Existing pods do **not** automatically pick up new imagePullSecrets. Only newly created pods can pull images successfully.

---

## ⚠️ Debugging & Troubleshooting

### Issue 1: `InvalidImageName`

* Root cause: Uppercase letters in GHCR image path
* Fix: Convert GitHub username to lowercase in CI pipeline

### Issue 2: `403 Forbidden` while pulling image

* Root cause: Missing GHCR authentication in Kubernetes
* Fix: Create `imagePullSecret` and patch ServiceAccount

### Issue 3: `manifest unknown`

* Root cause: Image tag not pushed or mismatched
* Fix: Ensure GitHub Actions completed successfully and image exists in GHCR

---

## ✅ Final Verification

```bash
kubectl -n hello get pods
kubectl -n hello get deploy
kubectl -n hello logs deploy/hello-app
```

Expected result:

```
READY   STATUS    RESTARTS
1/1     Running   0
```

---

## 🎯 Key DevOps Concepts Demonstrated

* GitOps as **single source of truth**
* Immutable container images (SHA-based tags)
* Secure private registry authentication
* Declarative Kubernetes deployments
* CI/CD automation using GitHub Actions
* Real-world Kubernetes debugging skills

---

## 💡 Why This Project Matters (Interview Perspective)

This project reflects **real production scenarios**, not toy examples:

✔ Handles private container registries
✔ Solves real `ImagePullBackOff` issues
✔ Uses GitOps instead of manual kubectl apply
✔ Shows CI + CD separation clearly

**This is exactly what DevOps/SRE interviewers look for.**

---

## 🚀 Possible Enhancements

* Add liveness & readiness probes
* Add Ingress / TLS
* Use Argo Rollouts (Blue-Green / Canary)
* Add image retention & cleanup policy
* Integrate security scanning (Trivy)

---

## 👤 Author

**Tarun Kumar Arcot**
DevOps | Kubernetes | OpenShift | GitOps
GitHub: [https://github.com/Tarun-Kumar-Arcot](https://github.com/Tarun-Kumar-Arcot)

---

If you want, next I can:

* Rewrite this into **resume bullet points**
* Add **architecture diagram**
* Convert this into an **Argo Rollouts demo**
* Prepare **interview questions from this project**

Just say the word 🚀
