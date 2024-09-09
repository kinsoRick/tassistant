from typing import Dict, Type


class SingletonMeta(type):
    _instances: Dict[Type["SingletonMeta"], "SingletonMeta"] = {}

    def __call__(
        cls: Type["SingletonMeta"], *args: tuple, **kwargs: dict
    ) -> "SingletonMeta":
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
