import logging

from control_tower.settings import NOTIFICATION_LEVEL

logger = logging.getLogger(__name__)


MESSAGE = "{}. Battery level is {}"


async def save(telegram, db, device_id, level):
    last_level = await db.get_last_level_by_device_id(device_id) or 100
    user_ids = await db.query_telegram_users(device_id)

    if level < NOTIFICATION_LEVEL.CRITICAL <= last_level:
        for user_id in user_ids:
            await telegram.send(user_id[0], MESSAGE.format("CRITICAL", level))
    elif level < NOTIFICATION_LEVEL.WARNING <= last_level:
        for user_id in user_ids:
            await telegram.send(user_id[0], MESSAGE.format("Warning", level))

    await db.save_last_level(device_id, level)
