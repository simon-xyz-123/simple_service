import logging

from fastapi import FastAPI
from dotenv import load_dotenv
from simple.views.flop import router as action_router
load_dotenv('.env')
from utils.log_config import setup_logger

app = FastAPI()
app.include_router(action_router)

# 放在事件钩子中
@app.on_event("startup")
async def startup_event():
    setup_logger()
    logging.info("项目启动，日志配置完成！")