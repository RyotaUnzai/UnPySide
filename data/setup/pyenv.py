import threading
from typing import Self

from software import AbstractSoftware


class Pyenv(AbstractSoftware):
    """A Singleton class that represents a Pyenv instance.
    """
    __lock = threading.Lock()

    def __new__(cls, *args, **kwargs) -> Self:
        if not hasattr(cls, "_instance"):
            with cls.__lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(Pyenv, cls).__new__(cls)
        return cls._instance
