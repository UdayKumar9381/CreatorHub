from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy import text
import time
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")

# Disable redirect_slashes to prevent CORS issues with trailing slashes
app = FastAPI(title="IdeaFlow API", redirect_slashes=False)

def get_cors_headers(request: Request):
    """Utility to generate CORS headers for exception responses"""
    origin = request.headers.get("origin")
    return {
        "Access-Control-Allow-Origin": origin if origin else "*",
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Allow-Methods": "*",
        "Access-Control-Allow-Headers": "*",
    }

# 1. Global Exception Handler (All internal crashes)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"CRITICAL ERROR: {type(exc).__name__}: {str(exc)}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal Server Error",
            "error_type": type(exc).__name__,
            "error_msg": str(exc),
            "path": request.url.path
        },
        headers=get_cors_headers(request)
    )

# 2. HTTP Exception Handler (404, 401, etc.)
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "path": request.url.path},
        headers=get_cors_headers(request)
    )

# 3. Validation Error Handler (422)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body, "path": request.url.path},
        headers=get_cors_headers(request)
    )

# --- MIDDLEWARE STACK ---
# NOTE: In Starlette/FastAPI, the LAST middleware added is the OUTERMOST wrapper.

# 1. Diagnostic Middleware (Innermost)
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
        logger.error(f"Middleware caught error for {method} {path}: {str(e)}")
        raise e

# 2. CORS Middleware (Outermost)
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

# 3. INCLUDE ROUTERS AFTER ALL MIDDLEWARE
from app.routes import auth, ideas, ai, notes, projects, checklist
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

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

@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """Diagnostic endpoint to verify DB and API health"""
    try:
        start_time = time.time()
        await db.execute(text("SELECT 1"))
        latency = time.time() - start_time
        return {
            "status": "healthy",
            "database": "connected",
            "latency_seconds": round(latency, 4),
            "environment": "production"
        }
    except Exception as e:
        logger.error(f"HEALTH CHECK FAILED: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e)
            },
            headers=get_cors_headers(None) # Generic headers
        )
