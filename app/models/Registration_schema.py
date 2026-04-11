from pydantic import BaseModel, field_validator

class RegisterRequest(BaseModel):
    username: str
    password: str

    @field_validator('password')
    @classmethod
    def password_length(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Password too long (maximum 72 bytes)')
        return v

    @field_validator('username')
    @classmethod
    def username_length(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        if len(v) > 50:
            raise ValueError('Username too long (maximum 50 characters)')
        return v

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
