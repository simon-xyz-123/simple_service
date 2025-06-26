import logging
from fastapi import APIRouter
from common.flop import send_tcp_message_async
from simple.data_model.flop import FlopRequest
from simple.service.flop_service import FlopService

router = APIRouter()


@router.post("/api/action")
async def send_tcp_async(request: FlopRequest):
    logging.info("开始请求")
    # args_data = get_args()
    result, response, msg = await send_tcp_message_async(request.data)
    # if not result:
    #     return
    # seq = []
    # result, msg = set_args(response, seq)
    return {"result": result,
            "data": response,
            "msg": msg}


@router.post("/api/dealing_flop")
async def dealing_flop(request: FlopRequest):
    logging.info("raise")
    print("data",request)
    data = {
        "step": "dealing flop",
        "hand": "01746062515855485355395137",
        "bords": "9sQsKs",
        "players": [
            {"stack": 512.5, "Bet": 16, "action": "calls", "player_id": 0, "pot_bet": [], "is_opp": True,
             "type": "SB",
             "name": "P1", "is_fold": False},
            {"stack": 406.5, "Bet": 16, "action": "calls", "player_id": 1, "pot_bet": [], "is_opp": False,
             "type": "BB",
             "name": "P2", "is_fold": False}],
        "seq": ["SB Call 21.33"],
    }
    result, response, msg = await FlopService.flop(request.data)
    return {"result": result,
            "data": response,
            "msg": msg}
