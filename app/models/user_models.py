from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    email: str
    password: str
    phone: str
    # fullname: Optional[str]
    # company: Optional[str]
