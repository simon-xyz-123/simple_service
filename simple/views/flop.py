import json
import logging

from fastapi import APIRouter

from common.flop import send_tcp_message_async
from simple.data_model.flop import FlopRequest
router = APIRouter()
@router.post("/api/action")
async def send_tcp_async(request: FlopRequest):
    logging.info("comein simple")
    logging.info(request.data)
    result, response, msg = await send_tcp_message_async(request.data)
    return {"result": result,
            "data": response,
            "msg": msg}

@router.post("/")
async def hello(request: FlopRequest):
    logging.info("hello")
    return {"result": 123}