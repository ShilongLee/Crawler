from data.driver import SqliteStore
from contextlib import closing
from lib.logger import logger
import time

class Proxies(SqliteStore):
    def __init__(self, store_path):
        super().__init__(store_path)
        self.primary_key = 'id'
        self.table_name = 'proxies'
        self._create_table()

    def _create_table(self):
        with closing(self._get_sync_connection()) as conn, closing(conn.cursor()) as cursor:
            try:
                sql = f'''
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    {self.primary_key} INTEGER PRIMARY KEY AUTOINCREMENT,
                    url VARCHAR(512) NOT NULL,
                    enable INTEGER NOT NULL,
                    ct INTEGER NOT NULL,
                    ut INTEGER NOT NULL
                )
                '''
                cursor.execute(sql)
                conn.commit()
            except Exception as e:
                logger.error(f'failed to create table, error: {e}')

    async def save(self, url: str = '', enable: int = 1, id: int = 0) -> bool:
        ct = ut = int(time.time())
        async with self._get_connection() as conn:
            try:
                sql = f'UPDATE {self.table_name} SET url = ?, enable = ?, ut = ? WHERE id = ?'
                await conn.execute(sql, (url, enable, ut, id))
                if conn.total_changes == 0:
                    sql = f'INSERT INTO {self.table_name} (url, enable, ct, ut) VALUES (?, ?, ?, ?)'
                    await conn.execute(sql, (url, enable, ct, ut))
                await conn.commit()
                return True
            except Exception as e:
                logger.error(f'failed to save proxy, error: {e}')
                await conn.rollback()
                return False
            
    async def remove(self, id: int) -> bool:
        async with self._get_connection() as conn:
            try:
                sql = f'DELETE FROM {self.table_name} WHERE id = ?'
                await conn.execute(sql, (str(id)))
                await conn.commit()
                return True
            except Exception as e:
                logger.error(f'failed to remove proxy, error: {e}')
                await conn.rollback()
                return False 

    async def load(self, offset: int = 0, limit: int = 0) -> list:
        async with self._get_connection() as conn:
            try:
                if limit == 0:
                    sql = f'SELECT * FROM {self.table_name}'
                    cursor = await conn.execute(sql)
                else:
                    sql = f'SELECT * FROM {self.table_name} LIMIT ? OFFSET ?'
                    cursor = await conn.execute(sql, (limit, offset))
                results = await cursor.fetchall()
                return [dict(row) for row in results]
            except Exception as e:
                logger.error(f'failed to load proxies, error: {e}')
                await conn.rollback()
                return []

    async def enable(self, id: int) -> bool:
        ut = int(time.time())
        async with self._get_connection() as conn:
            try:
                sql = f'UPDATE {self.table_name} SET enable = ?, ut = ? WHERE id = ?'
                await conn.execute(sql, (1, ut, id))
                await conn.commit()
                return True
            except Exception as e:
                logger.error(f'failed to save proxies, error: {e}')
                await conn.rollback()
                return False

    async def disable(self, id: int) -> bool:
        ut = int(time.time())
        async with self._get_connection() as conn:
            try:
                sql = f'UPDATE {self.table_name} SET enable = ?, ut = ? WHERE id = ?'
                await conn.execute(sql, (0, ut, id))
                await conn.commit()
                return True
            except Exception as e:
                logger.error(f'failed to save proxies, error: {e}')
                await conn.rollback()
                return False
            
proxies = Proxies("data/proxies/proxies.db")