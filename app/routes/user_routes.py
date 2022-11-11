import imp
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import session
from app.models.user_models import User
from app.models.user_Dto import UserDto
from app.schema.engine import SessionLocal
from app.schema.model import *
from app.utils.user_utils import * 
from app.schema.model import *
from app.routes.auth_routes import oauth2_scheme


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()


@router.post("/User/Create", tags=['Users'])
async def CreateUser(user:User, db: session = Depends(get_db)):
    check_user = db.query(Users).filter_by(email = user.email).first()
    if check_user == None: 
        newUser = Users(
            email = user.email,
            hashedPassword = getPasswordHash(user.password),
            secret = getRandomString(25),
            phone = user.phone,
            role = Role.dealer
            )
        db.add(newUser)
        db.commit()
        newUser = db.query(Users).filter_by(email = user.email).first()
    else:
        raise HTTPException(status_code=403, detail="User alredy exist")

    return newUser


@router.get("/All/Users", tags=['Users'])
async def GetUsers(au:str = Depends(oauth2_scheme), db: session = Depends(get_db)):
    if checkaccsess(au) == str(Role.admin):
        users = db.query(Users).all()
        return users
    else:
        raise HTTPException(status_code=401, detail="No access")


@router.get("/Users/Contractors", tags=['Users'])
async def GetContractorsFromUsers(au:str = Depends(oauth2_scheme), db: session = Depends(get_db)):
    if checkaccsess(au) == str(Role.admin):
        users = db.query(Users).filter_by(role = "contractor").all()
        return users
    else:
        raise HTTPException(status_code=401, detail="No access")


@router.get("/Users/Dealers", tags=['Users'])
async def GetDealersFromUsers(au:str = Depends(oauth2_scheme), db: session = Depends(get_db)):
    if checkaccsess(au) == str(Role.admin):
        users = db.query(Users).filter_by(role = "dealer").all()
        return users
    else:
        raise HTTPException(status_code=401, detail="No access")


@router.get("/Users/Admins", tags=['Users'])
async def GetAdminsFromUsers(au:str = Depends(oauth2_scheme), db: session = Depends(get_db)):
    if checkaccsess(au) == str(Role.admin):
        users = db.query(Users).filter_by(role = "admin").all()
        return users
    else:
        raise HTTPException(status_code=401, detail="No access")


@router.get("/Users/{id}",tags=['Users'])
async def getUserById(id: int, db: session = Depends(get_db), au:str = Depends(oauth2_scheme) ):
    if checkaccsess(au) == str(Role.admin):
        user = db.query(Users).filter_by(id = id).first()
        return user
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.delete("/Users/{id}", tags=['Users'])
async def deleteUserById(id: int, db: session = Depends(get_db), au:str = Depends(oauth2_scheme)):

    if  checkaccsess(au) == str(Role.admin):
        user = db.query(Users).filter_by(id = id).first()
        if (user==None):
            raise HTTPException(status_code=400, detail=f"User not found")
        else:
            db.query(Users).options().filter_by(id=id).delete()
            db.commit()
            name=user.email
            raise HTTPException(status_code=200, detail=f"User {name} successful delete")
    
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.put("/Users/{id}", tags=['Users'])
async def updateUserById(id: int, upd_email, upd_pass, upd_phone, db: session = Depends(get_db), au:str = Depends(oauth2_scheme)):

    if  checkaccsess(au) == str(Role.admin):
        user = db.query(Users).filter_by(id = id).first()
        if (user==None):
            raise HTTPException(status_code=400, detail=f"User not found")
        else:
            upd_user = db.query(Users).filter_by(id = id).first()
            upd_user.email = upd_email
            upd_user.password = upd_pass
            upd_user.phone = upd_phone

            db.add(upd_user)
            db.commit()

            name=upd_email
            raise HTTPException(status_code=200, detail=f"User {name} successful updated")
            
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.get("/User/Me", tags=['Users'])
async def GetMe(db: session = Depends(get_db), au:str = Depends(oauth2_scheme)):
    _id = getMyId(au)
    user = db.query(Users).filter_by(id = _id).first()
    return user