from prometheus_client import Counter, Gauge, Histogram

BUCKETS = [
    0.2,
    0.4,
    0.6,
    0.8,
    1.0,
    1.2,
    1.4,
    1.6,
    1.8,
    2.0,
    2.2,
    2.4,
    2.6,
    2.8,
    3,
    float('+inf'),
]

BOT_EXECUTION_LATENCY = Histogram(
    'bot_methods_execution_time',
    'Counts the execution time of telegram requests',
    buckets=BUCKETS
)

TOTAL_BOT_SEND_MESSAGES = Counter(
    'bot_send_messages',
    'Counts how many messages came from the bot',
)

TOTAL_BOT_RPS = Gauge(
    'bot_rps',
    'Counts bot rps',
)