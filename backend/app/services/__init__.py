from .base_service import BaseService
from ..models.models import Idea, ChecklistItem, Note, Project

idea_service = BaseService(Idea)
checklist_service = BaseService(ChecklistItem)
note_service = BaseService(Note)
project_service = BaseService(Project)
