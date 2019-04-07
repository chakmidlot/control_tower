import os

import pytest

from control_tower.db import Db
from control_tower.telegram.commands import Parser

test_user = -111
test_devices = (
    ("test_device_1", "device_1"),
    ("test_device_2", "device_2"),
    ("test_device_3", "device_3"),
    ("test_device_4", "device_4"),
)


@pytest.fixture()
async def db():
    assert os.getenv("ENV") == "test"

    test_db = Db()
    await test_db.connect()
    yield test_db


@pytest.fixture
async def parser(db):
    await db.remove_all_devices_from_telegram_user(test_user)
    for device_code, _ in test_devices:
        await db.remove_device(device_code)

    yield Parser(db)


@pytest.mark.asyncio
async def test_list_none_device(parser):
    devices = await parser.do(test_user, "/listdevices")
    assert "No devices registered" == devices


@pytest.mark.asyncio
async def test_list_one_device(db, parser):
    await db.insert_device(*test_devices[0])
    await parser.do(test_user, "/adddevice test_device_1")
    devices = await parser.do(test_user, "/listdevices")
    assert "Registered devices:\ndevice_1" == devices


@pytest.mark.asyncio
async def test_list_many_devices(db, parser):
    await db.insert_device(*test_devices[0])
    await db.insert_device(*test_devices[1])
    await db.insert_device(*test_devices[2])
    await db.insert_device(*test_devices[3])

    await parser.do(test_user, "/adddevice test_device_1")
    await parser.do(test_user, "/adddevice test_device_2")
    await parser.do(test_user, "/adddevice test_device_3")
    await parser.do(test_user, "/adddevice test_device_4")
    devices = await parser.do(test_user, "/listdevices")
    assert ["Registered devices:",
            "device_1",
            "device_2",
            "device_3",
            "device_4"] == sorted(devices.split('\n'))


@pytest.mark.asyncio
async def test_removing_device(db, parser):
    await db.insert_device(*test_devices[0])
    await db.insert_device(*test_devices[1])
    await db.insert_device(*test_devices[2])
    await db.insert_device(*test_devices[3])

    await parser.do(test_user, "/adddevice test_device_1")
    await parser.do(test_user, "/adddevice test_device_2")
    await parser.do(test_user, "/adddevice test_device_3")
    await parser.do(test_user, "/adddevice test_device_4")

    await parser.do(test_user, "/removedevice device_2")
    devices = await parser.do(test_user, "/listdevices")
    assert ["Registered devices:",
            "device_1",
            "device_3",
            "device_4"] == sorted(devices.split('\n'))


@pytest.mark.asyncio
async def test_get_last_level(parser):
    level = await parser.do(test_user, "/lastlevel test_devicee_1")
    assert "No previous battery data" == level


@pytest.mark.asyncio
async def test_get_last_level(db, parser):
    await db.insert_device(*test_devices[0])
    await db.save_last_level(test_devices[0][0], 55)
    await parser.do(test_user, "/adddevice test_device_1")
    level = await parser.do(test_user, "/lastlevel device_1")
    assert "Last level: 55" == level
