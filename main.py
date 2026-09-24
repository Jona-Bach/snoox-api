from fastapi import FastAPI, Depends, Header, HTTPException
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

app = FastAPI()


def verify_api_key(x_api_key : str = Header(...)):
    if x_api_key.strip() != API_KEY:
        raise HTTPException(401, "Api_KEy is not corret")

    return {"message":"Welcome to Snoox Api!"}


@app.get("/secure")
def send_key(result = Depends(verify_api_key)):
    return {"secure_data":"I like python"}



@app.get("/")
def read_root():
    return {"message":"Hello from Snoox API"}

