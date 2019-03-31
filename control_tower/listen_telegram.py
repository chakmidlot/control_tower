import asyncio
import json
import traceback
from json import JSONDecodeError
import logging

import aiohttp

from control_tower import settings
from control_tower.db import Db

logger = logging.getLogger(__name__)


UPDATES_URL = "https://api.telegram.org/bot{}/getUpdates?offset={}&timeout=20"

SEND_MESSAGE_URL = "https://api.telegram.org/bot{}/sendMessage"


async def answer_requests():
    db = Db()
    await db.connect()

    update_id = 0

    async def parse_message(message):
        if message['chat']['type'] == 'private':
            try:
                request = json.loads(message['text'])
                if request['command'] == 'register_device':
                    device_id = request['device_id']
                    await db.add_telegram_user(message['from']['id'], device_id)
            except JSONDecodeError:
                logger.debug("Not a command")
            except KeyError:
                logger.debug("Wrong message")

    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(UPDATES_URL.format(settings.telegram_token, update_id)) as resp:
                    update = await resp.json()
                    if update['ok']:
                        for query in update['result']:
                            if 'message' in query:
                                await parse_message(query['message'])

                        if len(update['result']):
                            update_id = update['result'][-1]['update_id'] + 1

                    else:
                        logger.warning("Not ok. " + update['description'])
                        await asyncio.sleep(10)

            except Exception:
                logger.warning("Telegram error\n" + traceback.format_exc())
                await asyncio.sleep(5)
