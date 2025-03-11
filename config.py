import os
from pydantic_settings import BaseSettings
from functools import lru_cache

config_path = __file__


class Config:

    @classmethod
    def get_home_path(cls):
        return os.path.dirname(config_path)

    @classmethod
    def check_path(cls, dir_path):
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

    @classmethod
    def get_temp_path(cls):
        temp_path = os.path.join(cls.get_home_path(), "temp")
        cls.check_path(temp_path)
        return temp_path

    @classmethod
    def get_log_path(cls):
        log_path = os.path.join(cls.get_home_path(), "log")
        cls.check_path(log_path)
        return log_path


class Settings(BaseSettings):
    BASE_DOMAIN: str = "http://127.0.0.1:8000"
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    WORKERS: int = 1
    RELOAD: bool = False
    USE_HTTPS: bool = False

    # DB
    DB_IP: str = "127.0.0.1"
    DB_PORT: int = 3306
    DB_NAME: str = "hxq_consultation"
    DB_USERNAME: str = "root"
    DB_PASSWORD: str = "123456"

    DEEPSEEK_API_KEY: str = "sk-7f59ee78719d42a388d5ba67e9e30797"
    DASHSCOPE_API_KEY: str = "sk-9209213513d84ef4b2016aa2ec2935da"

    # 对话相关
    # 对话最小轮数
    CHAT_MIN_ROUNDS: int = 12
    CHAT_MAX_ROUNDS: int = 15

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
