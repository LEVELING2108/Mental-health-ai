import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.routes import auth, moods, predict, users
from core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Mental Health AI Enterprise API for risk detection and support."
)

# Mount static files for profile pictures
if not os.path.exists("uploads"):
    os.makedirs("uploads")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Enterprise standard: Add CORS middleware
# Note: Using ["*"] for local network testing to ensure mobile connectivity
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False, # Must be False if using ["*"]
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

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(moods.router, prefix=f"{settings.API_V1_STR}/moods", tags=["moods"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(predict.router, prefix=f"{settings.API_V1_STR}/predict", tags=["predict"])

if __name__ == "__main__":
    import uvicorn
    # Use port 8001 by default to avoid conflicts with other common services on 8000
    uvicorn.run(app, host="0.0.0.0", port=8001)
