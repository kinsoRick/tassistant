import os
from typing import Optional, Dict
from dotenv import dotenv_values, load_dotenv
from logging import getLogger

from tassistant_bot.types import SingletonMeta

load_dotenv()
logger = getLogger(__name__)


class Config(metaclass=SingletonMeta):
    def __init__(self, env_file: str = ".env") -> None:
        self._env_file = env_file
        self._config: Dict[str, str] = dotenv_values(env_file)

        logger.debug(f"| Config | {self._env_file} | {self._config} |")

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Gets a value from the config file.

        :param key: The key to set.
        :param default: The value to return if the key is not found.
        :return: The value from the config file.
        """
        data = self._config.get(key, default)
        logger.debug(f"| config | get | {data} |")
        return data

    def set(self, key: str, value: str) -> None:
        """
        Sets the value for a given key in the configuration and updates the .env file.

        :param key: The key to set.
        :param value: The value to set.
        """
        self._config[key] = value

    def update(self, updates: Dict[str, str]) -> None:
        """
        Updates multiple key-value pairs in the configuration and updates the .env file.

        :param updates: A dictionary containing key-value pairs to update.
        """
        self._config.update(updates)

    def update_env_file(self) -> None:
        """
        Writes the current configuration back to the .env file.
        """
        with open(self._env_file, "w") as f:
            for key, value in self._config.items():
                f.write(f"{key}={value}\n")


config = Config(env_file=os.path.join(os.getcwd(), ".env"))
