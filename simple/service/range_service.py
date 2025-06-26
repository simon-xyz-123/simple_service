from common.commom import timeit
from simple.service.preflop_service import PreflopService


class Range:
    """获取range,dealingflop range from preflop and flop rang from redis"""

    @staticmethod
    @timeit
    def get_range(data):
        return PreflopService.get_range()