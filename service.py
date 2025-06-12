import json

from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv('.env')
app = FastAPI()

class DataRequest(BaseModel):
    data: dict

@app.post("/api/action")
async def send_tcp_async(request: DataRequest):
    return {"result": True,
            "data": {},
            "msg": ""}