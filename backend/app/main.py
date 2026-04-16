from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")

# Disable redirect_slashes to prevent CORS issues with trailing slashes
app = FastAPI(title="IdeaFlow API", redirect_slashes=False)

# Global Exception Handler - Catch everything and log traceback
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"GLOBAL ERROR: {str(exc)}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An internal server error occurred.",
            "error_type": type(exc).__name__,
            "error_msg": str(exc)
        }
    )

# 1. ADD MIDDLEWARE IMMEDIATELY AFTER APP INIT
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://creator-hub-frontend-nine.vercel.app",
        "https://creator-hub-frontend-nine.vercel.app/",
        "https://ideaflow-f.vercel.app",
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
    
    if method == "OPTIONS":
        logger.info(f"Handling OPTIONS preflight for {path}")

    try:
        response = await call_next(request)
        return response
    except Exception as e:
        # This will be caught by the global exception handler too, 
        # but logging here gives us the context of the request
        logger.error(f"Error handling request {method} {path}: {str(e)}")
        raise e

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
