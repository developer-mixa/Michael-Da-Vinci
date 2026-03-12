"""Infrastructure: MinIO/S3 implementation of IFileStorage."""

import io
import logging
from typing import Optional

from minio import Minio

from src.domain.interfaces.file_storage import IFileStorage

logger = logging.getLogger(__name__)


class S3FileStorage(IFileStorage):

    def __init__(self, endpoint: str, access_key: str, secret_key: str, bucket_name: str) -> None:
        self._bucket_name = bucket_name
        self._client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=False,
        )

    def upload_file(self, object_name: str, file: io.BytesIO) -> None:
        self._ensure_bucket()
        self._client.put_object(self._bucket_name, object_name, file, file.getbuffer().nbytes)
        logger.info('File %s uploaded', object_name)

    def get_file(self, object_name: str) -> Optional[bytes]:
        if not self._client.bucket_exists(self._bucket_name):
            return None
        try:
            response = self._client.get_object(self._bucket_name, object_name)
            data = response.data
            response.close()
            response.release_conn()
            return data
        except Exception:
            logger.exception('Failed to get file %s', object_name)
            return None

    def _ensure_bucket(self) -> None:
        if not self._client.bucket_exists(self._bucket_name):
            self._client.make_bucket(self._bucket_name)
            logger.info('Created bucket: %s', self._bucket_name)

