import time

import redis
import json
from typing import Optional, Union, Any


class RedisClient:
    def __init__(
        self,
        host: str = "localhost",       # Redis 服务器地址
        port: int = 6379,              # Redis 端口
        db: int = 0,                   # Redis 数据库索引
        password: Optional[str] = "fTEF8df3AL3THKtP",# Redis 密码（如有）
        decode_responses: bool = True  # 设置为 True 表示返回字符串而不是字节
    ):
        # 创建连接池，提高性能
        self.pool = redis.ConnectionPool(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=decode_responses
        )
        # 创建 Redis 客户端实例
        self.client = redis.Redis(connection_pool=self.pool)

    def set(self, key: str, value: Union[str, dict, list], ex: Optional[int] = None) -> bool:
        """
        设置键值，支持字符串、字典、列表，自动转换为 JSON 字符串。
        ex: 过期时间（秒）
        """
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        return self.client.set(name=key, value=value, ex=ex)

    def get(self, key: str) -> Optional[Union[str, dict, list]]:
        """
        获取指定 key 的值，自动反序列化 JSON（如能）
        """
        value = self.client.get(name=key)
        try:
            return json.loads(value)
        except (TypeError, json.JSONDecodeError):
            return value

    def delete(self, key: str) -> int:
        """
        删除指定 key
        """
        return self.client.delete(key)

    def hset(self, name: str, key: str, value: Union[str, dict, list]) -> int:
        """
        设置哈希类型的字段值
        name: Redis 的 hash key（类似一张表）
        key: 字段名
        value: 字段值（支持字典、列表）
        """
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        return self.client.hset(name, key, value)

    def hget(self, name: str, key: str) -> Optional[Any]:
        """
        获取哈希字段值，自动尝试 JSON 反序列化
        """
        value = self.client.hget(name, key)
        try:
            return json.loads(value)
        except (TypeError, json.JSONDecodeError):
            return value

    def hdel(self, name: str, *keys: str) -> int:
        """
        删除哈希表中的一个或多个字段
        """
        return self.client.hdel(name, *keys)

    def exists(self, key: str) -> bool:
        """
        判断 key 是否存在
        """
        return self.client.exists(key) == 1

    def expire(self, key: str, time: int) -> bool:
        """
        设置 key 的过期时间（秒）
        """
        return self.client.expire(key, time)

    def keys(self, pattern: str = '*') -> list:
        """
        获取所有匹配指定 pattern 的 key 列表
        """
        return self.client.keys(pattern)

def init_redis():
    global _redis_client
    _redis_client = RedisClient()

def get_redis() -> RedisClient:
    print(_redis_client)
    if _redis_client is None:
        raise RuntimeError("Redis 未初始化，请确保在 lifespan 中调用 init_redis()")
    return _redis_client
# ✅ 使用示例（建议仅测试时运行）
if __name__ == "__main__":
    start_time = time.time()
    redis_client = RedisClient()
    connect_time = time.time()
    print(f"final:{connect_time-start_time}")

    # 设置键值（自动序列化字典）
    redis_client.set("user:1001", {"name": "Alice", "age": 30}, ex=3600)
    print(f"final:{time.time()-start_time}")
    print(redis_client.get("user:1001"))

    # 设置哈希字段
    redis_client.hset("session:abc", "token", "xyz123")
    print(redis_client.hget("session:abc", "token"))

    # 删除键
    # redis_client.delete("user:1001")
