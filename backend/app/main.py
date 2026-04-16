from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, ideas, ai, notes, projects, checklist
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://creator-hub-frontend-nine.vercel.app/"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routes
app.include_router(auth.router)
app.include_router(ideas.router)
app.include_router(ai.router)
app.include_router(notes.router)
app.include_router(projects.router)
app.include_router(checklist.router)

@app.get("/")
async def root():
    return {"message": "Welcome to IdeaFlow API", "docs": "/docs"}
