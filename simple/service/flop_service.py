import json
import logging
import os

from common.commom import timeit
from common.flop import send_tcp_message_async
from simple.service.simple_root_service import SimpleRootService
from utils.redis_connect import get_redis


class FlopService:
    @staticmethod
    def write_response(hand, data):
        folder_path = "results"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        with open(f"{folder_path}/{hand}.json", "w") as f:
            f.write(json.dumps(data))

    @staticmethod
    def write_args_into_redis(simple_data):
        redis_client = get_redis()
        redis_client.set(simple_data.get("hand"), simple_data)

    @staticmethod
    @timeit
    async def flop(data):
        data_model = SimpleRootService.get_args(data)
        simple_data = data_model.model_dump()
        FlopService.write_args_into_redis(simple_data)
        result, response, msg = await send_tcp_message_async(simple_data)
        if result:
            FlopService.write_response(data_model.hand, response)
        logging.info("response")
        return result, response, msg
