from datetime import date

from pydantic.v1 import BaseModel, Field
from typing_extensions import List, Literal, Optional

from lang_playground.schemas.career import models


class CareerModel(BaseModel):
    company_name: str = Field("NOT_FOUND", description="회사 이름")
    employment_type: Optional[Literal["정규직", "계약직", "인턴"]] = Field(None, description="고용 형태")
    start_date: Optional[date] = Field(None, description="근무 시작일")
    end_date: Optional[date] = Field(None, description="근무 종료일")
    position: Optional[str] = Field(None, description="직급")
    department: Optional[str] = Field(None, description="부서")
    task: Optional[str] = Field(None, description="담당 업무")

    @classmethod
    def of(cls, model: models.CareerModel) -> "CareerModel":
        return cls(
            company_name=model.company_name,
            employment_type=model.employment_type,
            start_date=model.start_date,
            end_date=model.end_date,
            position=model.position,
            department=model.department,
            task=model.task,
        )

    def to_model(self) -> models.CareerModel:
        return models.CareerModel(
            company_name=self.company_name,
            employment_type=self.employment_type,
            start_date=self.start_date,
            end_date=self.end_date,
            position=self.position,
            department=self.department,
            task=self.task,
        )


class ResumeModel(BaseModel):
    name: str = Field("NOT_FOUND", description="지원자의 이름")
    email: str = Field("NOT_FOUND", description="지원자의 이메일")
    phone_number: str = Field("NOT_FOUND", description="지원자의 휴대폰 번호")

    careers: List[CareerModel] = Field([], description="경력")

    @classmethod
    def of(cls, model: models.ResumeModel) -> "ResumeModel":
        return cls(
            name=model.name,
            email=model.email,
            phone_number=model.phone_number,
            careers=[CareerModel.of(career) for career in model.careers],
        )

    def to_model(self) -> models.ResumeModel:
        return models.ResumeModel(
            name=self.name,
            email=self.email,
            phone_number=self.phone_number,
            careers=[career.to_model() for career in self.careers],
        )
