import os
import sys
from pathlib import Path

import pytest


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


@pytest.fixture(autouse=True, scope="session")
def env_settings():
    """
    Minimal env so that config.settings.Settings can be constructed in tests.
    """
    os.environ.setdefault("BOT_TOKEN", "TEST_TOKEN")
    os.environ.setdefault("BOT_WEBHOOK_URL", "")
    os.environ.setdefault("PG_USER", "test")
    os.environ.setdefault("PG_PASSWORD", "test")
    os.environ.setdefault("PG_DBNAME", "testdb")
    os.environ.setdefault("PG_HOST", "localhost")
    os.environ.setdefault("PG_PORT", "5432")
    os.environ.setdefault("REDIS_PASSWORD", "test-password")
    os.environ.setdefault("REDIS_HOST", "localhost")
    os.environ.setdefault("REDIS_PORT", "6379")
    os.environ.setdefault("SERVER_PORT", "8000")
    os.environ.setdefault("MINIO_USER", "minio")
    os.environ.setdefault("MINIO_PASSWORD", "minio123")
    os.environ.setdefault("MINIO_HOST", "minio")

    yield
