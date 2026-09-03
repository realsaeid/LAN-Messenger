from fastapi import FastAPI

app = FastAPI(
    title="LAN-Messenger", 
    description="Local Network Messaging Server",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "massege":"Lan Massneger Server is running"
    }
@app.get("/health")
def health_check():
    return{
        "stutus":"ok"
    }