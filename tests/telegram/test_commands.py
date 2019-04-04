import os

import pytest

from control_tower.db import Db
from control_tower.telegram.commands import Parser

test_user = -111


@pytest.fixture()
async def db():
    assert os.getenv("ENV") == "test"

    test_db = Db()
    await test_db.connect()
    yield test_db


@pytest.fixture
async def parser(db):
    await db.remove_all_devices(test_user)
    yield Parser(db)


@pytest.mark.asyncio
async def test_list_none_device(parser):
    devices = await parser.do(test_user, "/listdevices")
    assert "No devices registered" == devices


@pytest.mark.asyncio
async def test_list_one_device(parser):
    await parser.do(test_user, "/adddevice test_device_id_1")
    devices = await parser.do(test_user, "/listdevices")
    assert "Registered devices:\ntest_device_id_1" == devices


@pytest.mark.asyncio
async def test_list_many_devices(parser):
    await parser.do(test_user, "/adddevice test_device_id_1")
    await parser.do(test_user, "/adddevice test_device_id_2")
    await parser.do(test_user, "/adddevice test_device_id_3")
    await parser.do(test_user, "/adddevice test_device_id_4")
    devices = await parser.do(test_user, "/listdevices")
    assert ["Registered devices:",
            "test_device_id_1",
            "test_device_id_2",
            "test_device_id_3",
            "test_device_id_4"] == sorted(devices.split('\n'))


@pytest.mark.asyncio
async def test_removing_device(parser):
    await parser.do(test_user, "/adddevice test_device_id_1")
    await parser.do(test_user, "/adddevice test_device_id_2")
    await parser.do(test_user, "/adddevice test_device_id_3")
    await parser.do(test_user, "/adddevice test_device_id_4")

    await parser.do(test_user, "/removedevice test_device_id_2")
    devices = await parser.do(test_user, "/listdevices")
    assert ["Registered devices:",
            "test_device_id_1",
            "test_device_id_3",
            "test_device_id_4"] == sorted(devices.split('\n'))


@pytest.mark.asyncio
async def test_get_last_level(parser):
    level = await parser.do(test_user, "/lastlevel test_device_id_1")
    assert "No previous battery data" == level


@pytest.mark.asyncio
async def test_get_last_level(db, parser):
    await db.save_last_level("test_device_id_1", 55)
    await parser.do(test_user, "/adddevice test_device_id_1")
    level = await parser.do(test_user, "/lastlevel test_device_id_1")
    assert "Last level: 55" == level
