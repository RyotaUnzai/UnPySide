import threading


class Singleton(type):
    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class AbstractSoftware:
    __lock = threading.Lock()

    @property
    def installed(self):
        """Completed Software installation.
        """
        ...

    def install(self) -> None:
        """Install Software
        """
        ...

    def uninstall(self) -> None:
        """Uninstall Software
        """
        ...
