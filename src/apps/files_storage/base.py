import io
from abc import ABC, abstractmethod


class BaseStorageClient(ABC):

    @abstractmethod
    def upload_file(self, object_name: str, file: io.BytesIO) -> None:
        pass

    @abstractmethod
    def get_file(self, object_name: str) -> bytes | None:
        pass
