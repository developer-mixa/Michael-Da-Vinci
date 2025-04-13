from abc import ABC, abstractmethod
import io

class BaseStorageClient(ABC):

    @abstractmethod
    def upload_file(self, object_name: str, file: io.BytesIO):
        pass

    @abstractmethod
    def get_file(self):
        pass