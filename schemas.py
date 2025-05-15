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


class UpdateConsultRequest(BaseModel):
    consult_id: Optional[int] = None
    batch_no: Optional[str] = None
    diagnosis: Optional[str] = None
    report_think: Optional[str] = None
    report: Optional[str] = None
    report_start_time: Optional[str] = None
    report_end_time: Optional[str] = None


class QuestionNextRequest(BaseModel):
    consult_id: Optional[int] = None
    answer: Optional[str] = None


class VLLMChatCompletionRequest(BaseModel):
    messages: list[dict]
    model: Optional[str] = None
