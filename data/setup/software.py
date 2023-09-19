import threading


class AbstractSoftware:
    __lock = threading.Lock()

    @property
    def installed(self) -> bool:
        """Completed Software installation.

        Returns:
            bool: _description_
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
