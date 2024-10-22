from pydantic import BaseModel

class CreateUserCommand(BaseModel):
    user_id: int
    name: str

class UserResponse(BaseModel):
    id: int
    name: str