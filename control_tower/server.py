import logging
import traceback

from aiohttp import web

from control_tower.db import Db
from control_tower.save_level import save
from control_tower.telegram.client import TelegramClient


logger = logging.getLogger(__name__)

routes = web.RouteTableDef()


@routes.get('/save_level')
async def save_level(request):
    try:
        device_id = request.rel_url.query['device_id']
        level = int(request.rel_url.query['level'])
        charging = request.rel_url.query['charging']
    except KeyError as e:
        logger.warning(traceback.format_exc())
        return web.Response(text=f'{{"message": "Missing key: \"{e}\""}}', status=400)

    try:
        await save(request.app['telegram'], request.app['db'], device_id, level)
    except Exception:
        logger.error(traceback.format_exc())
        return web.Response(text=f'{{"status": "error"}}', status=500)

    logger.info("Level saved. Device: {}, level: {}".format("*****" + device_id[-4:], level))
    return web.Response(text='{"status": "ok"}')


@routes.get('/get_last_level')
async def get_last_level(request):
    params = request.rel_url.query.get('device_id')
    if not params:
        return web.Response(text=f'{{"message": "\"device_id\" parameter is not provided"}}', status=400)

    return web.Response(text=str(params))


async def init_app():
    db = Db()
    await db.connect()

    app = web.Application()
    app.add_routes(routes)
    app['db'] = db
    app['telegram'] = TelegramClient()
    return app
