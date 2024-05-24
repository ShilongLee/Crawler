from data.driver import SqliteStore
from contextlib import closing
from lib.logger import logger
import time

class KsAccount(SqliteStore):
    def __init__(self, store_path='kuaishou.db', pool_size=5):
        super().__init__(store_path, pool_size)
        self.primary_key = 'id'
        self.table_name = 'account'
        self._create_table()

    def _create_table(self):
        with closing(self._get_connection()) as conn, closing(conn.cursor()) as cursor:
            try:
                sql = f'''
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    {self.primary_key} VARCHAR(2048) PRIMARY KEY NOT NULL,
                    cookie VARCHAR(2048) NOT NULL,
                    expired INTEGER NOT NULL,
                    ct INTEGER NOT NULL,
                    ut INTEGER NOT NULL
                )
                '''
                cursor.execute(sql)
                conn.commit()
            except Exception as e:
                logger.error(f'failed to create table, error: {e}')

    def save(self, id: str, cookie: str, expired: int) -> bool:
        ct = ut = int(time.time())
        with closing(self._get_connection()) as conn, closing(conn.cursor()) as cursor:
            try:
                sql = f'UPDATE {self.table_name} SET cookie = ?, expired = ?, ut = ? WHERE id = ?'
                cursor.execute(sql, (cookie, expired, ut, id))
                if cursor.rowcount == 0:
                    sql = f'INSERT INTO {self.table_name} (cookie, expired, ct, ut, id) VALUES (?, ?, ?, ?, ?)'
                    cursor.execute(sql, (cookie, expired, ct, ut, id))
                conn.commit()
                return True
            except Exception as e:
                logger.error(f'failed to save cookies, error: {e}')
                conn.rollback()
                return False

    def load(self, offset: int = 0, limit: int = 0) -> list:
        with closing(self._get_connection()) as conn, closing(conn.cursor()) as cursor:
            try:
                if limit == 0:
                    sql = f'SELECT * FROM {self.table_name}'
                    cursor.execute(sql)
                else:
                    sql = f'SELECT * FROM {self.table_name} LIMIT ? OFFSET ?'
                    cursor.execute(sql, (limit, offset))
                results = cursor.fetchall()
                return [dict(row) for row in results]
            except Exception as e:
                logger.error(f'failed to load cookies, error: {e}')
                conn.rollback()
                return []
            
    def expire(self, id: str) -> bool:
        ut = int(time.time())
        with closing(self._get_connection()) as conn, closing(conn.cursor()) as cursor:
            try:
                sql = f'UPDATE {self.table_name} SET expired = ?, ut = ? WHERE id = ?'
                cursor.execute(sql, (1, ut, id))
                conn.commit()
                return True
            except Exception as e:
                logger.error(f'failed to save cookies, error: {e}')
                conn.rollback()
                return False

accounts = KsAccount("data/kuaishou/kuaishou.db")