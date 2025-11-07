from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Dependecies.Dependecies import Verify_Token, init_session
from Models.models import Users
from Schemes.Schemes import response_Users_Scheme, Update_Users_Scheme

Users_Router = APIRouter(prefix="/Users", tags=["/Users"], dependencies=[Depends(Verify_Token)])

@Users_Router.get("/Users", response_model=list[response_Users_Scheme])
async def Get_users(userid: Users = Depends(Verify_Token),session: Session = Depends(init_session)):
    if not userid.admin:
        raise HTTPException(status_code=400, detail="You do not have permission to view the users list")
    users = session.query(Users).all()
    return users
@Users_Router.get("/User", response_model=response_Users_Scheme)
async def Get_users(useremail: str,actualuser: Users = Depends(Verify_Token),session: Session = Depends(init_session)):
    if not actualuser.admin:
        raise HTTPException(status_code=400, detail="You do not have permission to view the users list")
    user = session.query(Users).filter(Users.email==useremail).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    return user

@Users_Router.put("/Update_Usersinfo", response_model=response_Users_Scheme)
async def Update_User(userid: int, updateinfoschemes: Update_Users_Scheme, actualUser: Users = Depends(Verify_Token), session: Session = Depends(init_session)):
    user = session.query(Users).filter(Users.id == userid).first()
    if not user:
        raise HTTPException( status_code=400, detail="User not found")
    
    if not actualUser.admin and user.id != actualUser.id:
        raise HTTPException (status_code=400, detail="You do not have permission to do this")
    if updateinfoschemes.name is not None:
        user.name = updateinfoschemes.name
    if updateinfoschemes.addres is not None:
        user.addres = updateinfoschemes.addres
    if updateinfoschemes.email is not None:
        user.email = updateinfoschemes.email
    if updateinfoschemes.number is not None:
        user.number = updateinfoschemes.number
    if updateinfoschemes.admin is not None:
        user.admin = updateinfoschemes.admin
    session.commit()
    return user

@Users_Router.delete("/Delete_User")
async def Delete_User (userid: int, user: Users = Depends(Verify_Token), session: Session = Depends(init_session)):
    if not user.admin:
        raise HTTPException (status_code=401, detail="You do not have permission to delete users")
    user = session.query(Users).filter(Users.id == userid).first()
    session.delete(user)
    session.commit()
    return {"message": "User succesfully deleted",
            "User": user}