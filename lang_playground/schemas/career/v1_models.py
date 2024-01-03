from pydantic.v1 import BaseModel, Field

from lang_playground.schemas.career import models


class ResumeModel(BaseModel):
    name: str = Field(..., description="지원자의 이름")
    email: str = Field(..., description="지원자의 이메일")
    phone_number: str = Field(..., description="지원자의 휴대폰 번호")

    @classmethod
    def of(cls, model: models.ResumeModel) -> "ResumeModel":
        return cls(name=model.name, email=model.email, phone_number=model.phone_number)

    def to_model(self) -> models.ResumeModel:
        return models.ResumeModel(name=self.name, email=self.email, phone_number=self.phone_number)
