from pydantic import BaseModel


user_db = {
    'solution': {
        "full_name": "Emmanuel",
        "username": "solution",
        "hashed_password": "$2b$12$Ytazit0wPnf7ew9uEb1K/Oc7I2CMeCblEI4kevRaGbOpTq0Nb/aZy",
        "email": "solution@gmail.com",
        "disabled": False 
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
    

class User(BaseModel):
    full_name: str
    username: str
    hashed_password: str
    email: str
    disabled: bool


class UserInData(User):
    hashed_password: str

