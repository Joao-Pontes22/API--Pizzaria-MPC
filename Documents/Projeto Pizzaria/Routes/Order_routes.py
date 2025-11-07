from fastapi import APIRouter, Depends, HTTPException
from Models.models import Orders, Users, Pizzas, Ingredients, Relation
from sqlalchemy.orm import Session
from Schemes.Schemes import Items_to_Order_Schemes, update_order_scheme
from Dependecies.Dependecies import init_session, Verify_Token
Order_Router = APIRouter(prefix="/Order", tags=["/Order"], dependencies=  [Depends(Verify_Token)])


def Sum_value(qnty: int, pizzaid: int, orderid: int, session: Session = Depends(init_session)):
    pizza = session.query(Pizzas).filter(Pizzas.id == pizzaid).first()
    value = pizza.value
    total = qnty * value
    order = session.query(Orders).filter(Orders.id == orderid).first()
    order.total_value=total
    session.commit()

def subtract_stock(pizzaid: int, qnty: int, session: Session = Depends(init_session)):
    pizza = session.query(Relation).filter(Relation.id_pizza==pizzaid).all()
    for r in pizza:
        qnty_to_subtract = qnty * r.ing_qnty
        ing = session.query(Ingredients).filter(Ingredients.id == r.id_ingredients).first()
        if ing.stock <= qnty_to_subtract:
            raise HTTPException(status_code=400, detail=f"Not enough igredients {ing.name}")
        qnty_subtracted = ing.stock - qnty_to_subtract
        ing.stock = qnty_subtracted
    session.commit()

@Order_Router.post("/Create_Order")
async def Create_Order(userid: Users= Depends(Verify_Token), session: Session = Depends(init_session)):
    user = session.query(Users).filter(Users.id==userid.id).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    new_Order= Orders(users_id= user.id)
    session.add(new_Order)
    session.commit()
    return{"message": "Order created succsseful",
           "Order": new_Order.id}
@Order_Router.put("/ADD_Items_to_Order")
async def   ADD_Items(orderid: int, itemsScheme: Items_to_Order_Schemes ,userid: int = Depends(Verify_Token),session:Session = Depends(init_session)):
    order = session.query(Orders).filter(Orders.id == orderid).first()
    user = session.query(Users).filter(Users.id==userid.id).first()
    if not order: 
        raise HTTPException(status_code=400, detail="Order not found")
    if not itemsScheme.pizza_id:
        raise HTTPException(status_code=400, detail="Pizza do not exist" )
    if user.id != order.users_id and not user.admin:
        raise HTTPException(status_code=403, detail="You do not have permission to update this order")
    order.pizza_id = itemsScheme.pizza_id
    order.qnty = itemsScheme.pizza_qnty
    order.size = itemsScheme.size
    order.status = "EM PREPARO"  
    Sum_value(itemsScheme.pizza_qnty, itemsScheme.pizza_id, orderid, session=session)
    subtract_stock(itemsScheme.pizza_id, itemsScheme.pizza_qnty, session=session)
    session.commit()
    return {"message": "Items successfully added to the order"}

@Order_Router.put("/Update_Order")
async def Update_Order(orderid: int, statusScheme: update_order_scheme, user: Users = Depends(Verify_Token),  session: Session = Depends(init_session)):
    order = session.query(Orders).filter(Orders.id == orderid).first()
    user = session.query(Users).filter(Users.id==user.id)
    if  not user.admin:
        raise HTTPException(status_code=403, detail="You do not have permission to update orders")
    if not order: 
        raise HTTPException(status_code=400, detail="Order not found")
    order.status = statusScheme.status.upper()
    session.commit()
    return{"message": "Status successfully updated ",
           "status": statusScheme.status}

@Order_Router.get("/View_Orders")
async def  View_Order(user: Users = Depends(Verify_Token), session: Session = Depends(init_session)):
    user = session.query(Users).filter(Users.id == user.id).first()
    orders = user.orders
    return orders

@Order_Router.get("/View_Order{Orders.id}")
async def View_Order_id (orderid : int, actualuser: Users = Depends(Verify_Token), session:Session = Depends(init_session)):
    order = session.query(Orders).filter(Orders.id == orderid).first()
    if not actualuser.admin and  order.users_id != actualuser.id:
        raise HTTPException (status_code=401, detail="You do not have permission to view this order")
    return order

@Order_Router.get("/View_All_Orders")
async def  View_all_Order(user: Users = Depends(Verify_Token), session: Session = Depends(init_session)):
    user = session.query(Users).filter(Users.id == user.id).first()
    order = session.query(Orders).all()
    if not user.admin:
        raise HTTPException (status_code=401, detail="You do not have permission to view all orders")
    return order