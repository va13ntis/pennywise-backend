from fastapi import FastAPI
from contextlib import asynccontextmanager
from models.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App is starting...")  # Startup logic here (e.g., DB connection)
    init_db()

    yield
    print("App is shutting down...")  # Cleanup logic here (e.g., closing DB connection)

app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
