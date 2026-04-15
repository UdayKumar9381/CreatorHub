from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from enum import Enum

class IdeaStatus(str, Enum):
    todo = "todo"
    in_progress = "in-progress"
    done = "done"

# Auth Schemas
class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

# Idea Schemas
class IdeaBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: IdeaStatus = IdeaStatus.todo

class IdeaCreate(IdeaBase):
    pass

class IdeaUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[IdeaStatus] = None

class IdeaOut(IdeaBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class AIResponse(BaseModel):
    title: str
    description: str

class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = None

# Note Schemas
class NoteBase(BaseModel):
    title: str
    content: Optional[str] = None

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class NoteOut(NoteBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Project Schemas
class ProjectStatus(str, Enum):
    planning = "planning"
    building = "building"
    judging = "judging"
    completed = "completed"

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: ProjectStatus = ProjectStatus.planning
    deadline: Optional[datetime] = None
    tech_stack: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    deadline: Optional[datetime] = None
    tech_stack: Optional[str] = None

class ProjectOut(ProjectBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Checklist Schemas
class ChecklistPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class ChecklistItemBase(BaseModel):
    title: str
    is_completed: bool = False
    priority: ChecklistPriority = ChecklistPriority.medium
    category: Optional[str] = "general"
    due_date: Optional[datetime] = None

class ChecklistItemCreate(ChecklistItemBase):
    pass

class ChecklistItemUpdate(BaseModel):
    title: Optional[str] = None
    is_completed: Optional[bool] = None
    priority: Optional[ChecklistPriority] = None
    category: Optional[str] = None
    due_date: Optional[datetime] = None

class ChecklistItemOut(ChecklistItemBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
