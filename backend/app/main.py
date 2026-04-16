from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")

app = FastAPI(title="IdeaFlow API")

# 1. ADD MIDDLEWARE IMMEDIATELY AFTER APP INIT
# 2. NO ROUTER IMPORTS BEFORE THIS LINE
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://creator-hub-frontend-nine.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Debug Middleware to log Origin headers
@app.middleware("http")
async def log_origin_header(request: Request, call_next):
    origin = request.headers.get("origin")
    method = request.method
    path = request.url.path
    if origin:
        logger.info(f"Incoming Request: {method} {path} from Origin: {origin}")
    else:
        logger.info(f"Incoming Request: {method} {path} (No Origin header)")
    
    response = await call_next(request)
    return response

# 3. INCLUDE ROUTERS AFTER MIDDLEWARE
from app.routes import auth, ideas, ai, notes, projects, checklist

app.include_router(auth.router)
app.include_router(ideas.router)
app.include_router(ai.router)
app.include_router(notes.router)
app.include_router(projects.router)
app.include_router(checklist.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to IdeaFlow API", 
        "docs": "/docs",
        "status": "online",
        "environment": "production"
    }
