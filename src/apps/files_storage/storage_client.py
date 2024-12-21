import io
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
            secure=False,
        )

    def upload_file(self, object_name: str, file: io.BytesIO):
        self._create_busket()
        self._put_file(object_name, file)

    def get_file(self, object_name: str) -> bytes:
        if not self.client.bucket_exists(self.bucket_name):
            return None
        return self._get_file(object_name)

    def _create_busket(self):
        found = self.client.bucket_exists(self.bucket_name)
        if not found:
            self.client.make_bucket(self.bucket_name)
            logger.info('Created busket: %s', self.bucket_name)
        else:
            logger.info('This busket is already exists - %s', self.bucket_name)

    def _put_file(self, object_name: str, file: io.BytesIO):
        self.client.put_object(self.bucket_name, object_name, file, file.getbuffer().nbytes)
        logger.info('File : %s was uploaded', object_name)

    def _get_file(self, object_name: str) -> bytes:
        try:
            response = self.client.get_object(self.bucket_name, object_name)
        finally:
            data_bytes = response.data
            response.close()
            response.release_conn()
        return data_bytes


images_storage: BaseStorageClient = S3StorageClient(bucket_name='user-images')
