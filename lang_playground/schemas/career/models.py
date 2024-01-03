from datetime import date

from pydantic import BaseModel, Field
from typing_extensions import List, Literal, Optional


class CareerModel(BaseModel):
    company_name: str = Field(..., description="회사 이름")
    employment_type: Optional[Literal["정규직", "계약직", "인턴"]] = Field(None, description="고용 형태")
    start_date: Optional[date] = Field(None, description="근무 시작일")
    end_date: Optional[date] = Field(None, description="근무 종료일")
    position: Optional[str] = Field(None, description="직급")
    department: Optional[str] = Field(None, description="부서")
    task: Optional[str] = Field(None, description="담당 업무")


class ResumeModel(BaseModel):
    name: str = Field(..., description="지원자의 이름")
    email: str = Field(..., description="지원자의 이메일")
    phone_number: str = Field(..., description="지원자의 휴대폰 번호")

    careers: List[CareerModel] = Field([], description="경력")
