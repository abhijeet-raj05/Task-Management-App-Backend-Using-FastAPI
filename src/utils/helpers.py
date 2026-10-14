from src.user.models import UserModel
from fastapi import HTTPException, status, Request, Depends
from src.utils.settings import settings
from src.utils.db import get_db
from pwdlib import PasswordHash
from datetime import datetime, timedelta
import jwt
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

## Authentication
def is_authenticated(request : Request, db : Session = Depends(get_db)):
    try:
        token = request.headers.get("authorization")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "You are unauthorized.")
        token = token.split(" ")[-1]
        data = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        user_id = data.get("_id")
        exp_time = data.get("exp")

        curr_time = datetime.now().timestamp()
        if curr_time > exp_time:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "You are unauthorized.")
        
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "You are unauthorized.")

        return user 
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "You are unauthorized.")