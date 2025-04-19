from prometheus_client import Counter, Gauge

TOTAL_BOT_SEND_MESSAGES = Counter(
    'bot_send_messages',
    'Counts how many messages came from the bot',
)

TOTAL_BOT_RPS = Gauge(
    'bot_rps',
    'Counts bot rps',
)