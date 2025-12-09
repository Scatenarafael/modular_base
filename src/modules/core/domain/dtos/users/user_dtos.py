from dataclasses import dataclass
from typing import Optional


@dataclass
class PayloadCreateUserDTO:
    first_name: str
    last_name: str
    email: str
    password: str
    active: bool = True


@dataclass
class PayloadUpdateUserDTO:
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    active: Optional[bool] = None
