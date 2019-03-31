import os

telegram_token = os.getenv("TELEGRAM_TOKEN")

dsn = 'dbname=postgres user=control_tower password=tower_mayday host=db port=5432'


class notification_level:
    warning = 40
    critical = 15

    reset = 80
