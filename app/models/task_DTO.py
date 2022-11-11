from datetime import datetime
from pydantic import BaseModel
from app.schema.model import Priority

class TaskDTO(BaseModel):
    theme: str
    title: str
    priority: Priority
    text: str
    tags: list
    files: list
    contractor_id: int
    date_of_submission: datetime
    date_of_closing: datetime
    