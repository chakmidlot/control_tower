import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

DB_DSN = 'dbname=postgres user=control_tower password=tower_mayday host=db port=5432'


class NOTIFICATION_LEVEL:
    WARNING = 40
    CRITICAL = 15

    RESET = 80


try:
    from control_tower.settings_local import *
except ImportError:
    pass
