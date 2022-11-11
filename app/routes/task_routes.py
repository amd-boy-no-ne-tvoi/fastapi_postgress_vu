from sys import flags
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import true
from sqlalchemy.orm import session
from app.models.user_models import User
from app.models.task_models import Task
from app.routes.user_routes import *
from app.schema.engine import SessionLocal
from app.schema.model import *
from app.utils.user_utils import * 
from app.utils.jwt_utils import * 
from app.models.task_DTO import TaskDTO

from app.routes.auth_routes import oauth2_scheme


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def return_user(db,token:str):
    id=decodeToken(token=token)["id"]
    user=db.query(User).filter_by(id=id).first()
    return user

router = APIRouter()


@router.post("/Tasks/Create", tags=['Tasks'])
async def CreateTask(task:Task, au:str = Depends(oauth2_scheme), db: session = Depends(get_db)):

    if task.store_name == None:
        task_store_name = ""
    else:
        task_store_name = task.store_name

    if task.phone_number == None:
        task_phone_number = ""
    else:
        task_phone_number = task.phone_number

    newTask = Tasks(
        theme = task.theme,
        title = task.title,
        text = task.text,
        priority = task.priority,
        status = Status.open,
        tags = task.tags,
        files = task.files,
        dealer_id = getMyId(au),
        store_name = task_store_name,
        phone_number = task_phone_number
    )

    db.add(newTask)
    db.commit()

    newTask = db.query(Tasks).filter_by(theme = task.theme).first()

    return newTask


@router.get("/Tasks/All", tags=['Tasks'])
async def GetTask(au:str = Depends(oauth2_scheme), db: session = Depends(get_db)):
    if checkaccsess(au) == str(Role.admin):
        tasks = db.query(Tasks).all()
        return tasks
    else:
        raise HTTPException(status_code=401, detail="No access")


@router.delete("/Task/{id}", tags=['Tasks'])
async def DeleteATaskById(id:int, au:str = Depends(oauth2_scheme), db: session = Depends(get_db)):
    if checkaccsess(au) == str(Role.admin):
        task = db.query(Tasks).filter_by(id = id).first()

        if (task==None):
            raise HTTPException(status_code=400, detail=f"Task not found")
            
        db.query(Tasks).options().filter_by(id=id).delete()
        db.commit()
        name=task.theme

        raise HTTPException(status_code=200, detail=f"Task '{name}' was successful deleted")
    
    else:
        raise HTTPException(status_code=401, detail="No access")


@router.put("/Task/{id}", tags=['Tasks'])
async def UpdateTaskById(id:int,task:Task, au:str = Depends(oauth2_scheme), db: session = Depends(get_db)):
    if checkaccsess(au) == str(Role.admin) or str(Role.dealer):
        upd_task = db.query(Tasks).filter_by(id = id).first()
        if (upd_task==None):
            raise HTTPException(status_code=400, detail=f"Task not found")
        else:
            upd_task.thme = task.theme
            upd_task.title = task.title
            upd_task.priority = task.priority
            upd_task.status = task.status
            upd_task.text = task.text

            db.commit()
            upd_task = db.query(Tasks).filter_by(id = id).first()
            return upd_task
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.get("/Task/{id}/AddContractor/{u_id}", tags=['Tasks'])
async def UpdateTaskContractorById(id:int, u_id:int, au:str = Depends(oauth2_scheme), db: session = Depends(get_db)):

    if checkaccsess(au) == str(Role.admin):

        # task
        upd_task = db.query(Tasks).filter_by(id = id).first()

        if (upd_task==None):
            raise HTTPException(status_code=400, detail=f"Task not found")
        else:
            # users
            users = await GetContractorsFromUsers(au, db)

            flag = False

            for val in users:
                if val.id == u_id:
                    flag = True
                    break

            if flag:
                upd_task.contractor_id = u_id
                db.commit()
                usr = await getUserById(u_id, db, au)
                name = usr.email
                raise HTTPException(status_code=200, detail=f"User {name} was assigned to the task with no {id}")
            else:
                str_for_exception = ""
                for val in users:
                    str_for_exception += " " + str(val.id)

                raise HTTPException(status_code=401, detail=f"User with id = {id} isn't a contractor\nPlease choose from contractors: {str_for_exception}")
        
    else:
        raise HTTPException(status_code=401, detail="Method not allowed. Only admin can assign a contractor")

    
@router.get("/Task/{id}", tags=['Tasks'])
async def GetTask(id:int, au:str = Depends(oauth2_scheme), db: session = Depends(get_db)):
    if checkaccsess(au) == str(Role.admin) or str(Role.dealer):
        task = db.query(Tasks).filter_by(id = id).first()
        if not task:
            raise HTTPException(status_code=403, detail="Task not found")
        return task
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.get("/Tasks/{status}", tags=['Tasks'])
async def GetTasksByStatus(status:Status, au:str = Depends(oauth2_scheme), db: session = Depends(get_db)):
    if checkaccsess(au) != None:
        task = db.query(Task).filter_by(id = id).first()
        if not task:
            raise HTTPException(status_code=403, detail="Task not found")
        return task
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
        