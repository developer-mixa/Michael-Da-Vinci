from prometheus_client import Counter

TOTAL_BOT_SEND_MESSAGES = Counter(
    'bot_send_messages',
    'Counts how many messages came from the bot',
)

TOTAL_CONSUMERS_RECEIVE_MESSAGES = Counter(
    'consumers_received_messages', 
    'Counts how many messages consumers have received'
)