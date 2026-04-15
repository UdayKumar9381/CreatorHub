from enum import Enum

class IdeaStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"

class ProjectStatus(str, Enum):
    PLANNING = "planning"
    BUILDING = "building"
    JUDGING = "judging"
    COMPLETED = "completed"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TokenType(str, Enum):
    ACCESS = "access"
    RESET = "reset"
