import sys

sys.path.append("..")
from redis import Redis


class RedisControl(object):
    def __init__(self):
        # self.redis = Redis(host='47.98.108.37', port=6379, decode_responses=True)
        # self.redis = Redis(host='r-bp1c6da5c8eda144.redis.rds.aliyuncs.com', port=6379, decode_responses=True,username="r-bp1c6da5c8eda144",password="011926Yhw")
        self.redis = Redis(host='r-bp1c6da5c8eda144pd.redis.rds.aliyuncs.com', port=6379, decode_responses=True,username="r-bp1c6da5c8eda144",password="011926Yhw")

    def setData(self, Config, ValueConfig):
        return self.redis.set(Config, ValueConfig)

    def getData(self, Config):
        return self.redis.get(Config)

