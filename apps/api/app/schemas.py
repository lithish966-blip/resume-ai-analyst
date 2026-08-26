from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=2, max_length=160)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ResumeResponse(BaseModel):
    id: str
    file_name: str
    status: str
    analysis: dict | None = None

class JobCreate(BaseModel):
    title: str
    company: str
    description: str
    location: str | None = None
    url: str | None = None
    required_skills: list[str] = []
