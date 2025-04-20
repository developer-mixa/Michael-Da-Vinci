import io
from abc import ABC, abstractmethod


class BaseStorageClient(ABC):

    @abstractmethod
    def upload_file(self, object_name: str, file: io.BytesIO):
        pass

    @abstractmethod
    def get_file(self, object_name: str) -> bytes:
        pass
