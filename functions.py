from fastapi import FastAPI, HTTPException, Depends # making api and (app) in api 
import os                                           # using opreting system function 
from sqlalchemy import text,distinct                # to execute raw sql queries
from pydantic import BaseModel, ConfigDict          # for validation and data scheme
from sqlalchemy.orm import session                  # database session
from model import Product                           # table
from database.database import Base, engine, get_db  # database

app = FastAPI()
Base.metadata.create_all(bind = engine)

#Class to give product resonse
class ProductResponse(BaseModel):
    pro_id : int 
    pro_name : str
    pro_cat : str
    pro_price : float

    model_config = ConfigDict(from_attributes=True)

#Class to give product category
class ProductCat(BaseModel):
    pro_cat : str


@app.get("/")
def home():
    return{
        "message : Welcome to functions"
    }

#List product
@app.get("/products",response_model=list[ProductResponse])
def get_products(db: session = Depends(get_db)):
    products = db.query(Product).all()

    return products


#Calculate Discounted Price
@app.get("/products/function/disc")
def disk(
    pro_id: int,
    discount : int,
    db: session = Depends(get_db)
):
    db_pro = db.query(Product).filter(Product.pro_id == pro_id).first()

    if not db_pro:
        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        )

    final_price = db_pro.pro_price - (db_pro.pro_price * discount / 100)

    return {
        "Product" : db_pro.pro_name,
        "Original price" : db_pro.pro_price,
        "Discount" : discount,
        "Final Price" : final_price
    }



#Count total no of products
@app.get("/products/function")
def cal_count(db: session = Depends(get_db)):
    with engine.connect() as connection:
        count =  connection.execute(text("SELECT COUNT(pro_id) FROM product")).scalar()
    return {
        "Product Count": count
    }


#List all products of a category
@app.get("/products/function/pro_cat",response_model=list[ProductResponse])
def cat_sort(
    pro_cat: str,
    db: session = Depends(get_db)
):
    db_pro = db.query(Product).filter(Product.pro_cat == pro_cat).all()

    return db_pro


#List all categories
@app.get("/products/function/cat",response_model=list[ProductCat])
def cat_list(db: session = Depends(get_db)):
    cat = db.query(Product.pro_cat).distinct().all()

    return cat


#Total inventory price
@app.get("/products/function/sum")
def pro_total(db: session = Depends(get_db)):
    with engine.connect() as connection:
        sum =  connection.execute(text("SELECT SUM(pro_price) FROM product")).scalar()
    return {
        "Product Total": sum
    }


#Total price of a category
@app.get("/products/function/cat-sum")
def cat_sum(
    pro_cat : str,
    db: session = Depends(get_db)
):
    with engine.connect() as connection:
        sum1 =  connection.execute(text("""SELECT SUM(pro_price) FROM product WHERE pro_cat=:pro_cat"""),{"pro_cat": pro_cat}).scalar()
    return {
        "Product Total": sum1
    }