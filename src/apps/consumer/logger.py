import logging.config
from contextvars import ContextVar

import yaml


with open('config/logging.conf.yml', 'r') as f:
    LOGGING_CONFIG = yaml.full_load(f)


class ConsoleFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        corr_id = correlation_id_ctx.get(None)

        if corr_id is not None:
            return '[%s] %s' % (corr_id, super().format(record))

        return super().format(record)


correlation_id_ctx: ContextVar[str] = ContextVar('correlation_id')

logger = logging.getLogger('consumer_logger')