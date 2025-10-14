from pydantic import BaseModel

class UserCredentials(BaseModel):
    name: str
    email: str
    app_password: str