import logging
from minio import Minio

from config.settings import settings
from src.apps.files_storage.base import BaseStorageClient

logger = logging.getLogger(__name__)

class S3StorageClient(BaseStorageClient):

    MINIO_ENDPOINT = f'{settings.MINIO_HOST}:9000'

    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name

        self.client = Minio(
            endpoint=self.MINIO_ENDPOINT,
            
            access_key=settings.MINIO_USER,
            secret_key=settings.MINIO_PASSWORD,
            secure=False
        )

    def upload_file(self, file_path: str):
        self._create_busket()
        self._put_file(file_path)

    def get_file(self):
        pass
    
    def _create_busket(self):
        found = self.client.bucket_exists(self.bucket_name)
        if not found:
            self.client.make_bucket(self.bucket_name)
            logger.info("Created busket: %s", self.bucket_name)
        else:
            logger.info("This busket is already exists - %s", self.bucket_name)

    def _put_file(self, file_path: str):
        object_name = file_path.split('/')[-1]
        self.client.fput_object(self.bucket_name, object_name, file_path,)
        logger.info('File : %s was uploaded', file_path)

images_storage: BaseStorageClient = S3StorageClient(bucket_name='user-images') 