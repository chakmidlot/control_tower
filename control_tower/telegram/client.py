import logging

import aiohttp

from control_tower import settings


logger = logging.getLogger(__name__)

SEND_MESSAGE_URI = "https://api.telegram.org/bot{}/sendMessage".format(settings.TELEGRAM_TOKEN)


class TelegramClient:

    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def send(self, chat_id, message):
        data = {
            "chat_id": chat_id,
            "text": message
        }

        await self.session.post(SEND_MESSAGE_URI.format(settings.TELEGRAM_TOKEN), data=data)
