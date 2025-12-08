from typing import Optional

from pydantic import BaseModel


class UserRequestBody(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    active: bool


class PayloadUpdateUser(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    active: Optional[bool] = None
