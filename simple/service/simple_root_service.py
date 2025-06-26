import json

from common.commom import timeit
from simple.data_model.flop import DataModel, PlayerInfo, BetSizingObject, StreetAction, SimpleRoot
from simple.service.convert import Convert
from simple.service.range_service import Range
from utils.redis_connect import get_redis


class SimpleRootService:
    """root_simple from dealing flop or ['bet', 'raise']"""

    @staticmethod
    @timeit
    def get_hands_from_response(response, actions):
        if not actions:
            strategies = response.get("strategies", [])[0]
            return strategies.get("hands")

        current_action = actions[0]
        children = response.get("children", [])

        for child in children:
            if child.get("action") == current_action:
                return SimpleRootService.get_hands_from_response(child, actions[1:])
        return None  # 如果路径不存在

    @staticmethod
    @timeit
    def get_args(data) -> DataModel | None:
        if data.get("step") == "dealing flop":
            player_range_dict = Range.get_range(data)
            return SimpleRootService.args_from_preflop(data, player_range_dict)
        elif data.get("step") in ["first raise", "first bet"]:
            return SimpleRootService.args_from_redis_renew(data)
        else:
            return SimpleRootService.args_from_redis(data)

    @staticmethod
    def args_from_redis(data) -> DataModel:
        redis_client = get_redis()
        root_simple = redis_client.get(data["hand"])
        data_model = DataModel(**root_simple)
        return data_model

    @staticmethod
    def args_from_redis_renew(data) -> DataModel:
        # redis values need to be renew
        with open(f"returns/{data.get("hand")}") as f:
            file = json.loads(f.read())
        redis_client = get_redis()
        root_simple = redis_client.get(data["hand"])
        data_model = DataModel(**root_simple)
        actions = data.get("seq", [])
        hand_list = SimpleRootService.get_hands_from_response(file, actions)
        # 更新range
        for player in data_model.simpleRoot.PlayersInfo:
            range_list = player.Range.split(",")
            res = Convert.renew_range(range_list, hand_list)
            player.Range = res
        root_simple = redis_client.get(data["hand"])
        data_model = DataModel(**root_simple)
        return data_model

    @staticmethod
    def args_from_preflop(data, player_range_dict) -> DataModel:
        players_info_list = []
        for index, player in enumerate(data.get("players")):
            player_info = PlayerInfo(
                Name=player.get("name").replace("P", "Seat"),
                Range=player_range_dict.get(player.get("name")),
                Bet=player.get("Bet"),  # 你可以根据实际情况替换默认值
                Stack=player.get("stack"),
                isFold=player.get("is_fold"),
                isOOP=player.get("is_opp"),
                BetSizingObject=BetSizingObject(
                    Around=0.01,
                    DeleteDonkBet=False,
                    FisrsAllIn=False,
                    Flop=StreetAction(Bets=[0.666667], Raises=[1.0]),
                    IsAround=False,
                    LastAllIn=False,
                    NumberOfBets=4,
                    OnlyPreflopFoldAllAfterCallAnd2Raise=False,
                    Preflop=StreetAction(Bets=[0.666667], Raises=[1.0]),
                    PreflopWay=0,
                    River=StreetAction(Bets=[0.666667], Raises=[1.0]),
                    ThresholdAllIn=0,
                    Turn=StreetAction(Bets=[0.666667], Raises=[1.0]),
                    WithoutPreflopCall=False,
                    WithoutPreflopColdCall=False,
                    WithoutPreflopLimp=False,
                    WithoutPreflopRaiseAfterCall=False,
                )
            )
            players_info_list.append(player_info)
        simple_root = SimpleRoot(
            Board=data.get("bords"),
            Version=105,
            numPlayers=len(players_info_list),
            PlayersInfo=players_info_list
        )
        data_model = DataModel(
            hand=data.get("hand"),
            site=9,
            simpleRoot=simple_root
        )
        return data_model
