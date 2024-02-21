from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import uvicorn

from db import User, user_db, Token
from utils import authenticate_user, generate_access_token, get_current_active_user, hash_password

app = FastAPI()


@app.post("/token", response_model=Token)
async def login_user_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(user_db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Incorrect username or password", 
                            headers={"WWW-Authenticate": "Bearer"})
    
    access_token = generate_access_token(data={"data": user.username})

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("user/me", response_model=User)
async def get_current_user(current_user: User = Depends(get_current_active_user)):
    return current_user

 
@app.get("user/me/data", response_model=User)
async def get_current_user_data(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": 1, "author": current_user}]



if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info", reload=True)
    # hashed_passwprd = hash_password('password@1')
    # print(hashed_passwprd)