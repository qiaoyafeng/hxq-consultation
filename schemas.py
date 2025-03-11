import datetime
from typing import List, Union, Optional
from fastapi import File, Form, UploadFile

from pydantic import BaseModel


class CreateConsultRequest(BaseModel):
    name: str
    sex: int = None
    age: int = None
    chief_complaint: Optional[str] = None
    batch_no: Optional[str] = None


class QuestionNextRequest(BaseModel):
    consult_id: Optional[int] = None
    answer: Optional[str] = None

