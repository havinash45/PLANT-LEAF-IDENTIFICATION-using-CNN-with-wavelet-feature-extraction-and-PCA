"""
Entry point for FastAPI application.
Configures lifespan, CORS middleware, static file serving, and API routers.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.config import settings
from app.database import init_db
from app.routes import auth, admin, prediction, researcher

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting LeafAI Hub Python Backend...")
    await init_db()
    
    # Ensure upload directory exists
    Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
    yield
    # Shutdown logic if any

app = FastAPI(
    title="LeafAI Hub Python API",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for uploads
upload_path = Path(settings.upload_dir).resolve()
upload_path.mkdir(parents=True, exist_ok=True)
print(f"Configuring resource handler for uploads: {upload_path}")
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

# Include Routers
app.include_router(auth.router)
app.include_router(prediction.router)
app.include_router(admin.router)
app.include_router(researcher.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=settings.server_port, reload=True)
