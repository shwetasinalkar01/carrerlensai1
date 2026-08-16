from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse

from database import Base, engine
from models import User, Resume, Job, Analysis

from routes.auth import router as auth_router
from routes.resume import router as resume_router
from routes.job import router as job_router
from routes.analysis import router as analysis_router


# Load environment variables from .env
load_dotenv()


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="CareerLens AI API",
    description="AI-powered resume analysis and job matching platform",
    version="1.0.0"
)


# Register API routes
app.include_router(auth_router)
app.include_router(resume_router)
app.include_router(job_router)
app.include_router(analysis_router)


# Serve CareerLens frontend
@app.get("/")
def root():
    return FileResponse("static/index.html")


# Health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }