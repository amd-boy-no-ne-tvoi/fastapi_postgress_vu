from fastapi import APIRouter, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import session
from app.schema.engine import SessionLocal
from app.models.user_Dto import *
from app.schema.model import *
from app.utils.jwt_utils import *
from app.utils.user_utils import verifyPassword, getRandomString

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="Token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.post("/Token", tags=['Token'])
async def token(userdto: OAuth2PasswordRequestForm = Depends(), db:session = Depends(get_db)):
    check_user = db.query(Users).filter_by(email = userdto.username).first()
    if not check_user:
        raise HTTPException(status_code=403, detail="User do not exist")
    if not verifyPassword(userdto.password, check_user.hashedPassword):
        raise HTTPException(status_code=403, detail="Incorrect username or password")

    check_user.secret = getRandomString(25)
    token = createToken(check_user.secret, {"userid":f"{check_user.id}","userrole":f"{check_user.role}"})
    db.commit()
    return {"access_token":f"{token}", "token_type": "bearer"}
    