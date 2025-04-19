from prometheus_client import Counter


TOTAL_CONSUMER_RECEIVE_MESSAGES = Counter(
    'consumers_received_messages', 
    'Counts how many messages consumers have received'
)