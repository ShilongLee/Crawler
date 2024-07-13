import os
import logging
import inspect
from threading import Lock
from logging.handlers import TimedRotatingFileHandler

class SingletonLogger:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(SingletonLogger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        log_format = "[%(asctime)s][%(name)s][%(levelname)s]: %(message)s"
        level = "DEBUG"
        self.logger = logging.getLogger('SingletonLogger')
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(log_format)
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(getattr(logging, level))
        self.logger.addHandler(console_handler)

    def setup(self, config=None):
        """
        初始化日志配置
        :param config: 日志配置
        """
        type = config['logger']['type']
        level = config['logger']['level'].upper()

        if type == 'console':
            self.logger.setLevel(getattr(logging, level))
            return
        
        log_file = config['logger']['path']
        backup_count = config['logger']['backupcount']
        log_format = config['logger']['format']
        
        self.logger.setLevel(getattr(logging, level))  # 使用配置的日志级别
        
        # 检查并创建日志文件夹
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # 移除控制台处理器
        for handler in self.logger.handlers:
            self.logger.removeHandler(handler)

        # 文件Handler
        file_handler = TimedRotatingFileHandler(log_file, when='H', interval=1, backupCount=backup_count)
        file_formatter = logging.Formatter(log_format)
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(getattr(logging, level))

        # 添加Handler
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
    def info(self, msg, *args, **kwargs):
        caller = inspect.getframeinfo(inspect.stack()[1][0])
        self.logger.info(f"({caller.filename}:{caller.lineno}) {msg}", *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        caller = inspect.getframeinfo(inspect.stack()[1][0])
        self.logger.error(f"({caller.filename}:{caller.lineno}) {msg}", *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        caller = inspect.getframeinfo(inspect.stack()[1][0])
        self.logger.debug(f"({caller.filename}:{caller.lineno}) {msg}", *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        caller = inspect.getframeinfo(inspect.stack()[1][0])
        self.logger.warning(f"({caller.filename}:{caller.lineno}) {msg}", *args, **kwargs)

    def get_logger(self):
        return self.logger
    
logger = SingletonLogger()