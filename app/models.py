from pydantic import BaseModel, Field
from typing import List

class LogEntry(BaseModel):
    message: str = Field(..., example="Hello World")
    priority: str = Field(..., example="high")
    tags: List[str] = Field(..., example=["test", "example"])
