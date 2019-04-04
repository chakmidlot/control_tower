from control_tower.db import Db


class Parser:

    def __init__(self, db):
        self.commands = Commands(db)

    async def do(self, telegram_id, text):
        if text.startswith("/") and not text.startswith("/_"):
            if " " in text:
                space = text.index(" ")
                action, options = text[1:space], text[space+1:]
            else:
                action, options = text[1:], None

            command = getattr(self.commands, action)
            return await command(telegram_id, options)


class Commands:
    def __init__(self, db: Db):
        self._db = db

    async def adddevice(self, telegram_id, options=None):
        await self._db.add_telegram_user(telegram_id, options)

    async def listdevices(self, telegram_id, options=None):
        devices = await self._db.query_user_devices(telegram_id)
        if devices:
            return "Registered devices:\n" + "\n".join([x[0] for x in devices])
        else:
            return "No devices registered"

    async def setname(self, telegram_id, options=None):
        return "Not implemented"

    async def removedevice(self, telegram_id, options=None):
        await self._db.remove_device(options, telegram_id)

    async def lastlevel(self, telegram_id, options=None):
        level = await self._db.get_last_level(options)
        if not level:
            return "No previous battery data"
        else:
            return f"Last level: {level}"
