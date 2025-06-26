import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from dotenv import load_dotenv
from simple.views.flop import router as action_router
from utils.redis_connect import init_redis

load_dotenv('.env')
from utils.log_config import setup_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 应用启动中，初始化 Redis...")
    # 初始化 Redis 实例
    init_redis()  # 此时 _redis_client 被设置
    print("✅ Redis 初始化完成")
    setup_logger()
    logging.info("项目启动，日志配置完成！")
    yield
    print("🔚 应用关闭中")

app = FastAPI(lifespan=lifespan)
app.include_router(action_router)