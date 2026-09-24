from fastapi import FastAPI, Depends, Header, HTTPException, Request
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


load_dotenv()

class Stock(BaseModel):
    symbol : str
    name : str
    price : float

database : dict[str, Stock] = {}


API_KEY = os.getenv("API_KEY")

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


def verify_api_key(x_api_key : str = Header(...)):
    if x_api_key.strip() != API_KEY:
        raise HTTPException(401, "Api_Key is not corret")

    return {"message":"Welcome to Snoox Api!"}


@app.get("/secure")
@limiter.limit("5/minute")
def send_key(request: Request, result = Depends(verify_api_key)):
    return {"secure_data":"I like python"}



@app.get("/")
def health():
    return {"message":"Healthy"}

@app.post("/stocks")
@limiter.limit("1/minute")
def add_stock(request : Request, stock: Stock, response = Depends(verify_api_key)):
    database[stock.symbol] = stock

    return {"stock": f"Added {stock.name}"}

@app.get("/stocks")
@limiter.limit("5/minute")
def get_all_stocks(request : Request, response = Depends(verify_api_key)):
    return database

@app.get("/stocks/{symbol}")
@limiter.limit("5/minute")
def get_symbol_stock(request : Request, symbol: str, response = Depends(verify_api_key)):
    if symbol in database:
        return database[symbol]
    else:
        raise HTTPException(404, "Symbol not found")
