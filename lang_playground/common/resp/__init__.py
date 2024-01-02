from typing import Generic, Optional, TypeVar

from pydantic import BaseModel


T = TypeVar("T")


class BaseApiResp(BaseModel, Generic[T]):
    code: int = 0
    message: str = "success"
    data: Optional[T] = None
