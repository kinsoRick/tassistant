import os
from typing import Optional, Dict, Type
from dotenv import dotenv_values, load_dotenv

load_dotenv()


class SingletonMeta(type):
    """
    A metaclass for implementing the Singleton pattern.

    This metaclass ensures that only one instance of a class is created. If
    an instance already exists, it returns the existing instance.
    """

    _instances: Dict[Type["SingletonMeta"], "SingletonMeta"] = {}

    def __call__(
        cls: Type["SingletonMeta"], *args: tuple, **kwargs: dict
    ) -> "SingletonMeta":
        """
        Creates a new instance of the class if it does not exist, otherwise returns the existing instance.

        :param cls: The class being instantiated.
        :param args: Positional arguments passed to the class constructor.
        :param kwargs: Keyword arguments passed to the class constructor.
        :return: The single instance of the class.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Config(metaclass=SingletonMeta):
    """
    A configuration class that uses the Singleton pattern

    This class loads configuration from an environment file and provides
    a method to retrieve configuration values.

    :param env_file: Path to the environment file. Defaults to ".env".
    """

    def __init__(self, env_file: str = ".env") -> None:
        """
        :param env_file: Path to the environment file. Defaults to ".env".
        """
        self._config: Dict[str, str] = dotenv_values(env_file)

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Retrieves the value for the given key from the configuration.

        :param key: The key for which to retrieve the value.
        :param default: The default value to return if the key is not found. Defaults to None.
        :return: The value associated with the key, or the default value if the key is not found.
        """
        return self._config.get(key, default)


config = Config(env_file=os.path.join(os.getcwd(), ".env"))
