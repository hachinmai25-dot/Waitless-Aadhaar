from fastapi import FastAPI
from routes import auth, application, centers

app = FastAPI(title="Waitless Aadhaar API")

app.include_router(auth.router)
app.include_router(application.router)
app.include_router(centers.router)

@app.get("/")
def home():
    return {"message": "Waitless Aadhaar API Running"}
