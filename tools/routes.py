from enum import Enum


class Routes(str, Enum):
    DISK = "/"
    RESOURCES = "/resources"
    UPLOAD = "/resources/upload"
    FILES = "/resources/files"
    TRASH_RESOURCES = "/trash/resources"
    TRASH_RESTORE = "/trash/resources/restore"

    def __str__(self) -> str:
        return self.value
