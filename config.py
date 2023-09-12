import os.path
from configparser import ConfigParser

CONFIG_FILENAME = 'config.ini'


def get_telegram_token():
    return get_setting('telegram', 'token')


def get_db_params() -> dict:
    db_params = {
        'name': get_setting('database', 'name'),
        'host': get_setting('database', 'host'),
        'user': get_setting('database', 'user'),
        'password': get_setting('database', 'password')
    }

    return db_params


def get_setting(section, setting, path=CONFIG_FILENAME):
    config = get_config(path)
    if config is None:
        return None

    return config.get(section, setting)


def get_config(path):
    if not os.path.exists(path):
        return None

    config = ConfigParser()
    config.read(path)
    return config
