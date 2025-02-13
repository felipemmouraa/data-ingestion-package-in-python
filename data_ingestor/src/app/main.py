# app/main.py
import uvicorn
import asyncio
from fastapi import FastAPI
from app.tasks.scheduler import periodic_publisher
from app.consumers.consumer import start_all_consumers
from app.utils.logger import get_logger

logger = get_logger(__name__)
app = FastAPI(title="Data Ingestion Service")

@app.get("/")
async def read_root():
    return {"message": "Data Ingestion Service is running."}

@app.on_event("startup")
async def startup_event():
    # Start periodic publisher as background task
    asyncio.create_task(periodic_publisher(30))
    # Optionally, start RabbitMQ consumers in separate threads
    import threading
    threading.Thread(target=start_all_consumers, daemon=True).start()
    logger.info("Application startup completed.")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
