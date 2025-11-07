from pydantic import BaseModel, EmailStr
from typing import Optional

class Users_Scheme (BaseModel):
    name: str
    email: EmailStr
    password: str  
    addres: str
    number: str
    admin: bool
    class Config:
        from_attributes = True

class Login_Scheme (BaseModel):
    email: EmailStr
    password:str

    class Config:
        from_attributes = True

class Ingredients_Scheme(BaseModel):
    name: str
    value: float
    stock: float
    unit_measure: str
    
    class Config:
        from_attributes = True

class Pizzas_Schemes(BaseModel):
    flavor: str
    value: float
    size: str
    class Config:
        from_attributes = True

class Relation_Schemes(BaseModel):
    Pizza_id: int
    Ing_id: int
    ing_qnty: float
    unit_measure: str
    class Config:
        from_attributes = True

class Items_to_Order_Schemes(BaseModel):
    pizza_id: int  
    pizza_qnty: int
    size: str
    class Config:
        from_attributes = True
class update_order_scheme (BaseModel):
    status:str
    class Config:    
        from_attributes = True

class response_Users_Scheme(BaseModel):
    id: int
    name: str
    email: EmailStr
    number: str
    addres: str
    admin: bool
    class Config:    
        from_attributes = True

class Update_Users_Scheme (BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    number: Optional[str] = None
    addres: Optional[str] = None
    admin: Optional[bool] = None
    class Config:    
        from_attributes = True
