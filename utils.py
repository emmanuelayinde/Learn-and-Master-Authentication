from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestFormStrict
from typing import Dict
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

from db import TokenData, User, UserInData, user_db


SECRET_KEY = "21fda1cf085aba208002760910474b293b8adb38d1f4e455cdd5709ada2e35f5"
ALGORITHM = "HS256"
TTL_IN_MINS = 30

password_hashing_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")




def verify_password(plain_password, hashed_password):
    return password_hashing_context.verify(plain_password, hashed_password)


def hash_password(password_to_be_hashed):
    return password_hashing_context.hash(password_to_be_hashed)


def get_user(db, username: str):
    if username in db:
        user_data = db[username]
        return user_data



def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return user
    
    return user


def generate_access_token(data: dict, expires_delta: timedelta | None = None):
    data_to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=TTL_IN_MINS)
    data_to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



# Dependency to get the current user
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub") or ''
        if username is None:
            raise credentials_exception
        user_token =  TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(user_db, username=user_token.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserInData = Depends(get_current_user)):
    if current_user.disabled:
        return HTTPException(status_code=400, detail="Inative User")
    
    return current_user



