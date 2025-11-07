from fastapi import APIRouter, Depends, HTTPException
from Schemes.Schemes import Ingredients_Scheme, Pizzas_Schemes, Relation_Schemes
from Dependecies.Dependecies import Verify_Token, init_session
from sqlalchemy.orm import Session
from Models.models import Users, Ingredients, Pizzas, Relation
Stock_Router = APIRouter(prefix="/Stock", tags=["Stock"])



def Update_Pizzas_Stock(pizza_id: int, session: Session):
    VARpizza = session.query(Pizzas).filter(Pizzas.id==pizza_id).first()
    VARrelation = session.query(Relation).filter(Relation.id_pizza == pizza_id).all()
    
    qnty_list = []
    for pizza in VARrelation:
        ing = pizza.ingredients
        qnty_pizza = ing.stock // pizza.ing_qnty
        qnty_list.append(qnty_pizza)
    
    VARpizza.stock=min(qnty_list)
    session.commit()
    return VARpizza.stock



@Stock_Router.get("View_pizza")
async def View_pizza(session:Session=Depends(init_session)):
    pizzas = session.query(Pizzas).all()
    return pizzas


@Stock_Router.post("/ADD_Ingredients")
async def Add_Ingredients(ingScheme: Ingredients_Scheme,user: Users = Depends(Verify_Token), session: Session = Depends(init_session)):
    VARing = session.query(Ingredients).filter(Ingredients.name==ingScheme.name).first()
    if VARing:
        raise HTTPException(status_code=400, detail="Ingredient already exist")
    if not user.admin:
        raise HTTPException(status_code=400, detail="You do not have permission to do it")
    new_ing = Ingredients(name=ingScheme.name,
                          value=ingScheme.value,
                          stock=ingScheme.stock,
                          unit_measure=ingScheme.unit_measure)
    session.add(new_ing)
    session.commit()
    return{"message": "Ingredient added",
           "Ingredient":new_ing.name }

@Stock_Router.post("/ADD_Pizzas")
async def ADD_Pizzas(pizzaSchemes: Pizzas_Schemes, user: Users = Depends(Verify_Token),session: Session = Depends(init_session)):
    if not user.admin:
        return HTTPException (status_code=401, detail="You do not have permission to update this")
    VARpizza = session.query(Pizzas).filter(Pizzas.flavor==pizzaSchemes.flavor).first()
    if VARpizza:
        raise HTTPException(status_code=400, detail="Flavo already exist")
    new_pizza = Pizzas(flavor=pizzaSchemes.flavor,
                       value=pizzaSchemes.value,
                       size=pizzaSchemes.size)
    session.add(new_pizza)
    session.commit()
    return{"message": "Pizza added",
           "Flavor": new_pizza.flavor}

@Stock_Router.post("/ADD_Ing_to_Pizzas")
async def ADD_Ing_to_Pizzas(relationSchemes: Relation_Schemes, user: Users = Depends(Verify_Token), session:Session=Depends(init_session)):
    if not user.admin:
        return HTTPException (status_code=401, detail="You do not have permission to update this")
    VARpizza = session.query(Pizzas).filter(Pizzas.id == relationSchemes.Pizza_id).first()
    VARing = session.query(Ingredients).filter(Ingredients.id == relationSchemes.Ing_id).first()
    if not VARpizza:
        raise HTTPException(status_code=400, detail="Pizza not found")
    if not VARing:
        raise HTTPException(status_code=400, detail="Ingredient not found")
    
    VARnew_relation = Relation(id_pizza=relationSchemes.Pizza_id,
                               id_ingredients=relationSchemes.Ing_id,
                               ing_qnty=relationSchemes.ing_qnty,
                               unit_measure=relationSchemes.unit_measure)
    session.add(VARnew_relation)
    Update_Pizzas_Stock(VARnew_relation.id_pizza, session=session)
    session.commit()
    return{"message": "Relation added, and quantity of pizza updated",
           "Stock of pizza": VARpizza.stock}

@Stock_Router.put("/Update_Ingredient_Stock")
async def Updade_Stock(Ingrendtid: int, qnty: float, user: Users = Depends(Verify_Token),session:Session=Depends(init_session)):
    if not user.admin:
        return HTTPException (status_code=401, detail="You do not have permission to update this")
    VARing = session.query(Ingredients).filter(Ingredients.id==Ingrendtid).first()
    VARpizza = session.query(Relation).filter(Relation.id_ingredients == Ingrendtid).all()
    if not VARing:
        raise HTTPException(status_code=400, detail="Ingredient not found")
    VARing.stock = qnty
    VARpizzasupdadet = []
    for p in VARpizza:
        Update_Pizzas_Stock(p.id_pizza, session=session)
        VARpizzasupdadet.append(p.id_pizza)
    session.commit()
    return {"message": "Stock updated",
            "Ingredient Stock": VARing.stock,
            "Pizzas updated stock ": VARpizzasupdadet}

@Stock_Router.delete("/Delete_Ingredient")
async def Delete_Ingredient(ingid: int, user: Users = Depends(Verify_Token),session: Session = Depends(init_session)):
    if not user.admin:
        return HTTPException (status_code=401, detail="You do not have permission to update this")
    VARing = session.query(Ingredients).filter(Ingredients.id == ingid).first()
    
    if not VARing:
        raise HTTPException(status_code=400, detail="Ingredient not found")
    
    # Delete the ingredient
    session.delete(VARing)
    session.commit()
    
    return {"message": f"Ingredient {ingid} deleted successfully"}

@Stock_Router.delete("/Delete_Ingredient_to_Pizza")
async def Delete_Ingredient(relid: int, user: Users = Depends(Verify_Token), session: Session = Depends(init_session)):
    if not user.admin:
        return HTTPException (status_code=401, detail="You do not have permission to update this")
    VARrel = session.query(Relation).filter(Relation.id == relid).first()
    
    if not VARrel:
        raise HTTPException(status_code=400, detail="Relation not found")
    
    # Delete the ingredient
    session.delete(VARrel)
    session.commit()
    
    return {"message": f"Relation {VARrel} deleted successfully"}