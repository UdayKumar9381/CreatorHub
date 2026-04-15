from fastapi import APIRouter, HTTPException
import random
import os
from groq import Groq
from ..schemas.schemas import AIResponse, ChatRequest
from ..core.config import settings

router = APIRouter(prefix="/ai", tags=["ai"])

# Fallback ideas in case AI is unavailable
MOCK_IDEAS = [
    {
        "title": "AI-Powered Personal Chef",
        "description": "An app that generates recipes based on what's in your fridge using computer vision and suggests nutrition-balanced meals."
    },
    {
        "title": "Eco-Tracker Marketplace",
        "description": "A platform where users can track their carbon footprint and earn tokens to spend on sustainable products."
    },
    {
        "title": "Virtual Study Hall",
        "description": "A 24/7 moderated space for students to co-work with productivity features and peer tutoring integration."
    },
    {
        "title": "Skill-Swap Network",
        "description": "A local community platform for exchanging services (e.g., plumbing for piano lessons) without using money."
    }
]

client = None
if settings.GROQ_API_KEY:
    try:
        client = Groq(api_key=settings.GROQ_API_KEY)
    except Exception as e:
        print(f"Error initializing Groq client: {e}")

@router.get("/generate", response_model=AIResponse)
async def generate_idea():
    if not client:
        return random.choice(MOCK_IDEAS)
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a creative startup incubator assistant. Generate a unique, innovative, and practical startup idea. Respond with a JSON object containing 'title' and 'description' keys only. Keep the description under 200 characters."},
                {"role": "user", "content": "Generate a new startup idea."}
            ],
            response_format={"type": "json_object"}
        )
        import json
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        print(f"Groq API error: {e}")
        return random.choice(MOCK_IDEAS)

@router.post("/chat")
async def ai_chat(request: ChatRequest):
    if not client:
        return {"response": "AI is currently resting. Try again later or check your API key configuration."}
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are IdeaFlow Bot, a helpful AI assistant for creators. You help with brainstorming, project planning, and technical advice. Keep responses concise and inspiring."},
                {"role": "user", "content": request.message}
            ]
        )
        return {"response": completion.choices[0].message.content}
    except Exception as e:
        print(f"Groq API error: {e}")
        return {"response": "I'm having trouble connecting to my brain right now. Please try again in a moment."}
