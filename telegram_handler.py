import asyncio
import logging

from control_tower.listen_telegram import answer_requests


app_logger = logging.getLogger("control_tower")
app_logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
app_logger.addHandler(ch)

root_logger = logging.getLogger()
root_logger.setLevel(logging.WARNING)
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root_logger.addHandler(ch)


if __name__ == '__main__':
    asyncio.run(answer_requests())
