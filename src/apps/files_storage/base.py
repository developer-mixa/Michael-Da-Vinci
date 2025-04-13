from abc import ABC, abstractmethod

class BaseStorageClient(ABC):

    @abstractmethod
    def upload_file(self, file_path: str):
        pass

    @abstractmethod
    def get_file(self):
        pass