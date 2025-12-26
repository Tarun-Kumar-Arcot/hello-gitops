from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from Kubernetes + ArgoCD + GitHub Actions!"}

@app.get("/healthz")
def healthz():
    return {"ok": True}

