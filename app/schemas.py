
from datetime import datetime
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    model_validator,
)


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    created_at: datetime


CalculationType = Literal["Add", "Sub", "Multiply", "Divide"]


class CalculationCreate(BaseModel):
    a: float = Field(allow_inf_nan=False)
    b: float = Field(allow_inf_nan=False)
    type: CalculationType
    user_id: int = Field(gt=0)

    @model_validator(mode="after")
    def validate_division(self):
        if self.type == "Divide" and self.b == 0:
            raise ValueError("Cannot divide by zero")
        return self


class CalculationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    a: float
    b: float
    type: CalculationType
    result: float
    user_id: int


class UserLogin(BaseModel):
    username: str
    password: str


class UserLoginResponse(BaseModel):
    message: str
    user: UserRead
