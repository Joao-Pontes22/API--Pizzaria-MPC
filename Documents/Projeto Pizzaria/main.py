from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
import os
from passlib.context import CryptContext
from fastapi_mcp import FastApiMCP

load_dotenv()
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES= int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="Auth/Login_Form")
app = FastAPI()

app.get("/")
async def Root():
    return "Rota principal"

from Routes.auth_routes import auth_router
from Routes.stock_routes import Stock_Router
from Routes.Order_routes import Order_Router
from Routes.Users_routes import Users_Router

app.include_router(auth_router)
app.include_router(Stock_Router)
app.include_router(Users_Router)
app.include_router(Order_Router)


mcp = FastApiMCP(app,
                 name= "Pizzaria",
                 description="Api para pizzaria com atenimento mcp")
mcp.mount_http()
mcp.setup_server()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)