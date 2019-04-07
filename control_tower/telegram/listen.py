import asyncio
import json
import traceback
from json import JSONDecodeError
import logging

import aiohttp

from control_tower import settings
from control_tower.db import Db

logger = logging.getLogger(__name__)


UPDATES_URL = "{}/bot{}/getUpdates?offset={}&timeout=20"

SEND_MESSAGE_URL = "https://api.telegram.org/bot{}/sendMessage"


class TelegramListener:

    def __init__(self):
        self.db = Db()
        self.update_id = 0

    async def listen(self):
        await self.db.connect()

        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    await self.get_updates(session)
                except Exception:
                    logger.warning("Telegram error\n" + traceback.format_exc())
                    await asyncio.sleep(5)

    async def get_updates(self, session):
        async with session.get(UPDATES_URL.format(settings.TELEGRAM_HOST, settings.TELEGRAM_TOKEN, self.update_id)) as resp:
            update = await resp.json()
            if update['ok']:
                for query in update['result']:
                    if 'message' in query:
                        await self.parse_message(query['message'])

                if len(update['result']):
                    self.update_id = update['result'][-1]['update_id'] + 1
            else:
                logger.warning("Not ok. " + update['description'])
                await asyncio.sleep(10)

    async def parse_message(self, message):
        if message['chat']['type'] == 'private':
            try:
                request = json.loads(message['text'])
                if request['command'] == 'register_device':
                    device_id = request['device_id']
                    await self.db.add_telegram_user(message['from']['id'], device_id)
            except JSONDecodeError:
                logger.debug("Not a command")
            except KeyError:
                logger.debug("Wrong message")
