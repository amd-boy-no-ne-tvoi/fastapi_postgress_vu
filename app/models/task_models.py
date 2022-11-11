from pydantic import BaseModel, validator
from app.schema.model import Priority, Status
from typing import Optional


class Task(BaseModel):
    theme: str
    title: str
    priority: Priority
    status: Status
    text: str
    tags: list
    files: list
    tags: list
    files: list
    store_name: Optional[str]
    phone_number: Optional[str]