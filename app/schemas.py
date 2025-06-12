from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

class QueryInput(BaseModel):
    query: str

class UpdateInput(BaseModel):
    sql: str
