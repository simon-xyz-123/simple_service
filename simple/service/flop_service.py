import json

from common.flop import send_tcp_message_async


async def send_msg(json_str_data):
    return await send_tcp_message_async(json_str_data)
