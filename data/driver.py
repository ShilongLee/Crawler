import sqlite3
from sqlalchemy.pool import QueuePool

class SqliteStore:
    def __init__(self, db_path, pool_size=5):
        self.db_path = db_path
        self._connection_pool = QueuePool(self._connect, max_overflow=0, pool_size=pool_size)

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 结果以字典形式返回
        return conn

    def _get_connection(self):
        return self._connection_pool.connect()
