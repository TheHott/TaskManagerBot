import os.path
from configparser import ConfigParser

CONFIG_FILENAME = 'config.ini'


def get_telegram_token():
    return get_setting('telegram', 'token')


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
