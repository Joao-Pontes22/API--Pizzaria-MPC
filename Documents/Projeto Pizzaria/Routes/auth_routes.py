from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Dependecies.Dependecies import init_session, Verify_Token
from Schemes.Schemes import Users_Scheme,  Login_Scheme
from Models.models import Users
from main import bcrypt_context, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from jose import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm
auth_router = APIRouter(prefix="/Auth", tags=["Auth"])


def Create_Token(user_id, token_duration: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):

    expiration_date = datetime.now(timezone.utc) + token_duration
    array_info = {"sub": str(user_id),
               "exp": expiration_date
            }

    token = jwt.encode(array_info, SECRET_KEY, algorithm=ALGORITHM)
    return token


@auth_router.post("/Create_account")
async def Create_account(Usersscheme: Users_Scheme, session: Session = Depends(init_session)):
    VARuser = session.query(Users).filter(Users.email == Usersscheme.email).first()
    if VARuser:
        raise HTTPException(status_code=400, detail="Email is already in use.")
    VARpass_crypt = bcrypt_context.hash(Usersscheme.password)
    VARnew_user = Users(name= Usersscheme.name,
                        email= Usersscheme.email,
                        password=VARpass_crypt,
                        addres=Usersscheme.addres,
                        number=Usersscheme.number,
                        admin=Usersscheme.admin)

    session.add(VARnew_user)
    session.commit()
    return{"message": "Account created",
           "email": VARnew_user.email}

@auth_router.post("/Login")
async def Login (loginscheme: Login_Scheme, session: Session = Depends(init_session)):
    VARuser = session.query(Users).filter(Users.email == loginscheme.email).first()
    if VARuser and bcrypt_context.verify(loginscheme.password, VARuser.password):
            VARaccess_token = Create_Token(VARuser.id)
            VARrefresh_token = Create_Token(VARuser.id, token_duration=timedelta(days=7))
            return{"Access_token":VARaccess_token,
                    "Refresh_token":VARrefresh_token}
    raise HTTPException(status_code=400, detail="Account not found")

@auth_router.post("/Login_Form")
async def Login_Form(form_info: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(init_session)):
    VARuser = session.query(Users).filter(Users.email==form_info.username).first()
    if VARuser and bcrypt_context.verify(form_info.password, VARuser.password):
        VARaccess_token = Create_Token(VARuser.id)
        return{"access_token":VARaccess_token,
               "token_type":"bearer"}
    raise HTTPException (status_code=400, detail="Invalid Email or Password")  
    
@auth_router.post("/Refresh_Token")
async def Refresh_token(user: Users = Depends(Verify_Token)):
    access_token = Create_Token(user.id)
    return{"Acces_Token":access_token,
           "token_type":"bearer"}
    
