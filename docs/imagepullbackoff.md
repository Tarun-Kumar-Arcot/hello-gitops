### Issue 1: `403 Forbidden` while pulling image

* Root cause: Missing GHCR authentication in Kubernetes
* Fix: Create `imagePullSecret` and patch ServiceAccount
```bash
kubectl -n hello create secret docker-registry ghcr-pull-secret \
  --docker-server=ghcr.io \
  --docker-username=<github-username> \
  --docker-password=<github-personal-access-token> \ 
  --docker-email=<your-email>
kubectl -n hello patch serviceaccount default \
  -p '{"imagePullSecrets":[{"name":"ghcr-pull-secret"}]}'
```
My details of github:-

* username: Tarun-Kumar-Arcot
* github-personal-access-token: Go to Profile Settings ---> Developer Settings ---> Personal access token ---> Tokens (clasic) ---> Generate new token --> clasic and check these:-
~~~
read:packages
repo        (safe to include)
~~~

###Root Causes Identified

* Container image tag did not exist in GHCR

* GHCR image was private and Kubernetes had no authentication

* imagePullSecrets were not applied to the ServiceAccount

###Debugging Steps

* Checked pod events using kubectl describe pod

* Verified image tags in GitHub Container Registry

* Confirmed GitHub Actions pipeline status

* Checked ServiceAccount configuration

###Resolution

* Fixed GitHub Actions workflow to push correct image tags

* Created a GHCR imagePullSecret

* Patched the default ServiceAccount to use the pull secret

* Restarted the deployment to create new pods

###Key Learnings

* imagePullSecrets are read only at pod creation time

* GitOps requires debugging both Git and cluster state

* Image tags must exactly match what Kubernetes requests