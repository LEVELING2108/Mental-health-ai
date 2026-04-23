from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import predict
from core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Mental Health AI Enterprise API for risk detection and support."
)

# Enterprise standard: Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "project": settings.PROJECT_NAME,
        "version": "1.0.0",
        "api_docs": f"{settings.API_V1_STR}/docs"
    }

app.include_router(predict.router, prefix=f"{settings.API_V1_STR}/predict", tags=["predict"])

if __name__ == "__main__":
    import uvicorn
    # Use port 8001 by default to avoid conflicts with other common services on 8000
    uvicorn.run(app, host="0.0.0.0", port=8001)
