import threading


class AbsSoftware:
    __lock = threading.Lock()

    @property
    def installed(self) -> bool:
        """Completed Software installation.

        Returns:
            bool: _description_
        """
        ...

    def install(self) -> None:
        ...

    def uninstall(self) -> None:
        ...
