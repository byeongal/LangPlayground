from pydantic import BaseModel, Field


class ResumeModel(BaseModel):
    name: str = Field(..., description="지원자의 이름")
    email: str = Field(..., description="지원자의 이메일")
    phone_number: str = Field(..., description="지원자의 휴대폰 번호")
