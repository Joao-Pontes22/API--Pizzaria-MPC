from sqlalchemy.orm import Session, sessionmaker
from Models.models import db, Users
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from main import oauth2_scheme, SECRET_KEY, ALGORITHM
from Schemes.Schemes import Update_Users_Scheme
def init_session():
    session = None
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()
        print("Session closed.")

def Verify_Token (token = Depends(oauth2_scheme), session:Session = Depends(init_session) ):
    try:
        array_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_user = array_info.get("sub")
        print(id_user)
    except JWTError:
        raise HTTPException (status_code=401, detail="Invalid token")
    user = session.query(Users).filter(Users.id == id_user).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    return(user)
