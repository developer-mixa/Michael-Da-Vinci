"""Port: File storage interface."""

import io
from abc import ABC, abstractmethod
from typing import Optional


class IFileStorage(ABC):

    @abstractmethod
    def upload_file(self, object_name: str, file: io.BytesIO) -> None:
        pass

    @abstractmethod
    def get_file(self, object_name: str) -> Optional[bytes]:
        pass

