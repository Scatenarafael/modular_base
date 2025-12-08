from dataclasses import dataclass


@dataclass
class UserDTO:
    full_name: str
    email: str
    active: bool

    def __init__(self, first_name: str, last_name: str, email: str, active: bool):
        self.full_name = f"{first_name}_{last_name}"
        self.email = email
        self.active = active
