# API Messages
ERROR_MSG_USER_NOT_FOUND = "User not found"
ERROR_MSG_INVALID_CREDENTIALS = "Invalid credentials"
ERROR_MSG_EMAIL_TAKEN = "Email already registered"
ERROR_MSG_IDEA_NOT_FOUND = "Idea not found"
ERROR_MSG_NOTE_NOT_FOUND = "Note not found"
ERROR_MSG_PROJECT_NOT_FOUND = "Project not found"
ERROR_MSG_CHECKLIST_NOT_FOUND = "Checklist item not found"
ERROR_MSG_INVALID_TOKEN = "Invalid or expired token"
ERROR_MSG_INVALID_TOKEN_TYPE = "Invalid token type"

# AI Prompts
AI_SYSTEM_PROMPT_IDEA_GEN = (
    "You are a creative startup incubator assistant. Generate a unique, innovative, and practical startup idea. "
    "Respond with a JSON object containing 'title' and 'description' keys only. Keep the description under 200 characters."
)

AI_SYSTEM_PROMPT_CHAT = (
    "You are IdeaFlow Bot, a helpful AI assistant for creators. You help with brainstorming, "
    "project planning, and technical advice. Keep responses concise and inspiring."
)
