from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Optional, List
import uvicorn
import os
import sys

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

# Import routes
from api.routes import auth_routes, chatbot_routes, diagnosis_routes
from api.models import user_models, chat_models, diagnosis_models
from api.database import get_db, Base, engine
from api.auth.utils import get_current_user, create_access_token

# Create FastAPI app
app = FastAPI(
    title="MedBot API",
    description="API for medical diagnosis chatbot",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_routes, prefix="/api/auth", tags=["Authentication"])
app.include_router(chatbot_routes, prefix="/api/chatbot", tags=["Chatbot"])
app.include_router(diagnosis_routes, prefix="/api/diagnosis", tags=["Diagnosis"])

# Startup event
@app.on_event("startup")
async def startup_event():
    # Initialize database
    Base.metadata.create_all(bind=engine)
    print("Database initialized")

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to MedBot API", "status": "online"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Run the application
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True) 