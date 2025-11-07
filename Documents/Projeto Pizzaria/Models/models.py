from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm  import relationship, declarative_base

#Conexão com o banco de dados 
db = create_engine("sqlite:///db.db")


#Base parra modelo das tabelas
base= declarative_base()

#Tabela usuario
#Users table
class Users (base):
    __tablename__="Users"

    id = Column("id", Integer,primary_key=True, autoincrement=True)
    name = Column("name",String, nullable=False)
    email = Column("email",String, nullable=False)
    password = Column("password",String, nullable=False)
    addres = Column("addres",String, nullable=False)
    number =  Column("number",String, nullable=False)
    admin = Column("admin",Boolean)

    orders = relationship("Orders", back_populates="users")

    def __init__(self, name, email, password, addres, number, admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.addres = addres
        self.number = number
        self.admin = admin

#Tabelas de pizzas
#Pizzas table
class Pizzas (base):
    __tablename__="Pizzas"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    flavor = Column("flavor", String)
    value = Column("value", Float)
    size = Column("size", String)
    stock = Column("stock", Integer)

    PRelation = relationship("Relation", back_populates="pizzas")
    orders = relationship("Orders", back_populates="pizzas")
    def __init__(self, flavor, value, size):
        self.flavor = flavor
        self.value = value
        self.size = size

#Tabelas d ingredientes
#Ingredients table

class Ingredients (base):
    __tablename__="Ingredients"
    
    id = Column("id",Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    value = Column("value", Float)
    stock = Column("stock", Float)
    unit_measure = Column("unit_measure", String)

    IRelation = relationship("Relation", back_populates="ingredients")

    def __init__(self, name, value, stock, unit_measure):
        self.name = name
        self. value = value
        self.stock = stock
        self.unit_measure = unit_measure

#Tabela para relacionar pizzas x ingredients
#Table to relate pizzas and ingredients
class Relation (base):
    __tablename__="Relation"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    id_pizza = Column("id_pizza", ForeignKey("Pizzas.id"))
    id_ingredients = Column("id_ingredients", ForeignKey("Ingredients.id"))
    ing_qnty = Column("ing_qnty", Float)
    unit_measure = Column("unit_measure", String)

    pizzas = relationship("Pizzas", back_populates="PRelation")
    ingredients = relationship("Ingredients", back_populates="IRelation")

    def __init__(self, id_pizza, id_ingredients, ing_qnty, unit_measure):
        self.id_pizza = id_pizza
        self.id_ingredients = id_ingredients
        self.ing_qnty = ing_qnty
        self.unit_measure = unit_measure

#Tabela de pedidos
# Orders table    
class Orders (base):
    __tablename__="Orders"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    users_id = Column("users_id", ForeignKey("Users.id")) 
    pizza_id = Column("pizza_id", ForeignKey("Pizzas.id"))
    total_value = Column("total_value", Float)
    qnty = Column("qnty", Integer)
    size = Column("size", String)
    status = Column("status", String)

    pizzas = relationship("Pizzas", back_populates="orders")
    users = relationship("Users", back_populates="orders")
    def __init__(self, users_id, status = "AGUARDANDO"):
        self.users_id = users_id
        self.status = status
#Tabela de items do pedido
#Items of  Orders table
class ItemsOrders (base):
    __tablename__="ItemsOrders"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    order_id = Column("orders_id", ForeignKey("Orders.id"))
    pizza_id = Column("pizza_id", ForeignKey("Pizzas.id"))    
    qnty = Column("qnty", Integer)
    value = Column("value", Float)
    size = Column("size", String)

    pizza = relationship("Pizzas")
    order = relationship("Orders")

    def __init__(self, pizza_id, qnty, size ):

        self.pizza_id = pizza_id
        self.qnty = qnty
        self.size = size