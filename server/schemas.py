from pydantic import BaseModel


class UserRegister(BaseModel):
    username: str
    password: str
    full_name: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    full_name: str
    is_online: bool

    class Config:
        from_attributes = True