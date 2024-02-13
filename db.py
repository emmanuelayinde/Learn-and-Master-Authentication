from passlib.context import CryptContext
from pydantic import BaseModel


# Password hashing
password_hashing_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define user model
class User(BaseModel):
    username: str
    password: str


users_db = {
    'id-001': {
        'username': 'Engr_SoluTion',
        'password': 'cdckmckm'
    }
}