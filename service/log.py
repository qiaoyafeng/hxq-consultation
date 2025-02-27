from loguru import logger
from datetime import datetime

from config import Config

LOG_PATH = Config.get_log_path()


class AutoLogger:
    """
    利用loguru封装接口自动化项目日志记录器
    """

    def __new__(cls, *args, **kwargs):
        log_name = datetime.now().strftime("%Y-%m-%d")  # 以时间命名日志文件，格式为"年-月-日"
        sink = f"{LOG_PATH}/{log_name}"  # 日志记录文件路径
        level = "INFO"  # 记录的最低日志级别为INFO
        encoding = "utf-8"  # 写入日志文件时编码格式为utf-8
        enqueue = True  # 多线程多进程时保证线程安全
        rotation = "500MB"  # 日志文件最大为500MB，超过则新建文件记录日志
        retention = "1 week"  # 日志保留时长为一星期，超时则清除
        logger.add(
            sink=sink,
            level=level,
            encoding=encoding,
            enqueue=enqueue,
            rotation=rotation,
            retention=retention,
        )
        return logger


logger = AutoLogger()
