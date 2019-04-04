import logging

import aiopg

from control_tower import settings
from control_tower.db import sql

logger = logging.getLogger(__name__)


class Db:

    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await aiopg.create_pool(settings.DB_DSN)
        await self._execute(sql.INITIALIZE_DB)

    async def add_telegram_user(self, telegram_user_id, device_id):
        await self._execute(sql.INSERT_USER_SQL, (telegram_user_id, device_id))

    async def save_last_level(self, device_id, level):
        await self._execute(sql.SET_LEVEL_SQL, (device_id, level, level))

    async def get_last_level(self, device_id):
        last_level = await self._query(sql.SELECT_LEVEL_SQL, (device_id,))
        if not last_level:
            return None
        else:
            return last_level[0][0]

    async def query_telegram_users(self, device_id):
        return await self._query(sql.SELECT_USERS_SQL, (device_id,))

    async def query_user_devices(self, telegram_id):
        return await self._query(sql.SELECT_USER_DEVICES_SQL, (telegram_id, ))

    async def remove_device(self, device_id, telegram_id):
        return await self._execute(sql.DELETE_DEVIDE, (device_id, telegram_id))

    async def remove_all_devices(self, telegram_id):
        await self._execute(sql.DELETE_ALL_DEVIDES, (telegram_id,))

    async def _query(self, query, parameters=None):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, parameters)
                return [x async for x in cur]

    async def _execute(self, query, parameters=None):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, parameters)
