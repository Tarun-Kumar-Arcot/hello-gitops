from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from Kubernetes + ArgoCD + GitHub Actions!"}

@app.get("/healthz")
def healthz():
    return {"ok": True}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)