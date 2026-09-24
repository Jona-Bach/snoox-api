from fastapi import FastAPI, Depends, Header, HTTPException
from dotenv import load_dotenv
import os
from pydantic import BaseModel


load_dotenv()

class Stock(BaseModel):
    symbol : str
    name : str
    price : float

database : dict[str, Stock] = {}


API_KEY = os.getenv("API_KEY")

app = FastAPI()


def verify_api_key(x_api_key : str = Header(...)):
    if x_api_key.strip() != API_KEY:
        raise HTTPException(401, "Api_Key is not corret")

    return {"message":"Welcome to Snoox Api!"}


@app.get("/secure")
def send_key(result = Depends(verify_api_key)):
    return {"secure_data":"I like python"}



@app.get("/")
def read_root():
    return {"message":"Hello from Snoox API"}

@app.post("/stocks")
def add_stock(stock: Stock):
    database[stock.symbol] = stock

    return {"stock": f"Added {stock.name}"}

@app.get("/stocks")
def get_all_stocks():
    return database

@app.get("/stocks/{symbol}")
def get_symbol_stock(symbol: str):
    if symbol in database:
        return database[symbol]
    else:
        raise HTTPException(404, "Symbol not found")
