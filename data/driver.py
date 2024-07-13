from contextlib import asynccontextmanager, closing
from lib.logger import logger
import time
import sqlite3
import aiosqlite

class SqliteStore:
    def __init__(self, db_path):
        self.db_path = db_path

    @asynccontextmanager
    async def _get_connection(self):
        async with aiosqlite.connect(self.db_path) as conn:
            conn.row_factory = aiosqlite.Row
            yield conn

    def _get_sync_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

class CommonAccount(SqliteStore):
    def __init__(self, store_path):
        super().__init__(store_path)
        self.primary_key = 'id'
        self.table_name = 'account'
        self._create_table()

    def _create_table(self):
        with closing(self._get_sync_connection()) as conn, closing(conn.cursor()) as cursor:
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

    async def save(self, id: str, cookie: str, expired: int) -> bool:
        ct = ut = int(time.time())
        async with self._get_connection() as conn:
            try:
                sql = f'UPDATE {self.table_name} SET cookie = ?, expired = ?, ut = ? WHERE id = ?'
                await conn.execute(sql, (cookie, expired, ut, id))
                if conn.total_changes == 0:
                    sql = f'INSERT INTO {self.table_name} (cookie, expired, ct, ut, id) VALUES (?, ?, ?, ?, ?)'
                    await conn.execute(sql, (cookie, expired, ct, ut, id))
                await conn.commit()
                return True
            except Exception as e:
                logger.error(f'failed to save cookies, error: {e}')
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
                logger.error(f'failed to load cookies, error: {e}')
                await conn.rollback()
                return []

    async def expire(self, id: str) -> bool:
        ut = int(time.time())
        async with self._get_connection() as conn:
            try:
                sql = f'UPDATE {self.table_name} SET expired = ?, ut = ? WHERE id = ?'
                await conn.execute(sql, (1, ut, id))
                await conn.commit()
                return True
            except Exception as e:
                logger.error(f'failed to save cookies, error: {e}')
                await conn.rollback()
                return False
