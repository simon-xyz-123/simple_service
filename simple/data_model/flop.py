from pydantic import BaseModel


class FlopRequest(BaseModel):
    data: dict


from pydantic import BaseModel
from typing import List


class StreetAction(BaseModel):
    Bets: List[float]
    Raises: List[float]


class BetSizingObject(BaseModel):
    Around: float
    DeleteDonkBet: bool
    FisrsAllIn: bool
    Flop: StreetAction
    IsAround: bool
    LastAllIn: bool
    NumberOfBets: int
    OnlyPreflopFoldAllAfterCallAnd2Raise: bool
    Preflop: StreetAction
    PreflopWay: int
    River: StreetAction
    ThresholdAllIn: int
    Turn: StreetAction
    WithoutPreflopCall: bool
    WithoutPreflopColdCall: bool
    WithoutPreflopLimp: bool
    WithoutPreflopRaiseAfterCall: bool


class PlayerInfo(BaseModel):
    Name: str
    Bet: float
    Stack: float
    Range: str
    isFold: bool
    isOOP: bool
    BetSizingObject: BetSizingObject


class SimpleRoot(BaseModel):
    Board: str
    Version: int
    numPlayers: int
    PlayersInfo: List[PlayerInfo]


class DataModel(BaseModel):
    hand: str
    site: int
    simpleRoot: SimpleRoot
