from fastapi import FastAPI, HTTPException, Depends # making api and (app) in api 
import os                                           # using opreting system function 
from sqlalchemy import text,distinct                # to execute raw sql queries
from pydantic import BaseModel, ConfigDict          # for validation and data scheme
from sqlalchemy.orm import session                  # database session
from model import Product                           # table
from database.database import Base, engine, get_db  # database

app = FastAPI()
Base.metadata.create_all(bind = engine)

#Class to Create product
class CreateProduct(BaseModel):
    pro_name : str
    pro_cat : str
    pro_price : float
    

#Class to give product resonse
class ProductResponse(BaseModel):
    pro_id : int
    pro_name : str
    pro_cat : str
    pro_price : float
    

    model_config = ConfigDict(from_attributes=True)

#Class for updating only price
class UpdatePrice(BaseModel):
    pro_price : float

#Class for updating details
class UpdateProduct(BaseModel):
    pro_name : str | None = None
    pro_cat : str | None = None 
    pro_price : float | None = None
    


@app.get("/")
def home():
    return{
        "message : API in online"
    }

@app.get("/db-test")
def db_test():
    try:
        with engine.connect as connection:
            connection.execute(text("SELECT 1"))
            print("Database is online")
    except Exception as e:
        print("Database Connection Failed")
        print(e)


#Create Product
@app.post("/products",response_model=ProductResponse,status_code=201)
def create_product(
    product: CreateProduct,
    db: session = Depends(get_db)
):

    new_product = Product(
        pro_name = product.pro_name,
        pro_cat = product.pro_cat,
        pro_price = product.pro_price
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


#Delete product
@app.delete("/products/{pro_id}")
def delete_product(
    pro_id: int,
    db: session = Depends(get_db)
):
    product = db.query(Product).filter(Product.pro_id == pro_id).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        )
    db.delete(product)
    db.commit()

    return{
        "Message : Product Deleted Successfully"
        "Pro_id" : pro_id
    }


#List product
@app.get("/products",response_model=list[ProductResponse])
def get_products(db: session = Depends(get_db)):
    products = db.query(Product).all()

    return products


#Change product price
@app.put("/products/{pro_id}/price")
def update_price(
    pro_id: int,
    product: UpdatePrice,
    db: session = Depends(get_db)
):
    db_pro = db.query(Product).filter(Product.pro_id == pro_id).first()

    if not db_pro:
        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        )

    db_pro.pro_price = product.pro_price

    db.commit()

    return db_pro


#Change product details
@app.put("/products/{pro_id}")
def update_product(
    pro_id: int,
    product: UpdateProduct,
    db: session = Depends(get_db)
):
    db_pro = db.query(Product).filter(Product.pro_id == pro_id).first()

    if not db_pro:
        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        )

    db_pro.pro_name = product.pro_name
    db_pro.pro_cat = product.pro_cat
    db_pro.pro_price = product.pro_price

    db.commit()

    return db_pro