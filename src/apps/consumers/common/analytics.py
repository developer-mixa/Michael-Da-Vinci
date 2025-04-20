from prometheus_client import Counter, Histogram

DECLARE_QUEUE_BUCKETS = [
    0.1,
    0.2,
    0.3,
    0.4,
    0.5,
    float('+inf'),
]

PRODUCE_MESSAGE_BUSKETS = DECLARE_QUEUE_BUCKETS

PROCESSING_MESSAGE_BUCKETS = [
    0.4,
    0.6,
    0.8,
    1.0,
    float('+inf'),
]


DECLARE_QUEUE_LATENCY = Histogram(
    'declare_queue_execution_time',
    'Counts the execution time of declaring queue',
    buckets=DECLARE_QUEUE_BUCKETS
)

PRODUCE_MESSAGE_LATENCY = Histogram(
    'produce_message_execution_time',
    'Counts the execution time of producing messages',
    buckets=PROCESSING_MESSAGE_BUCKETS
)

PROCESSING_MESSAGE_LATENCY = Histogram(
    'processing_message_execution_time',
    'Counts the execution time of processing messages',
    buckets=PROCESSING_MESSAGE_BUCKETS
)

TOTAL_CONSUMER_RECEIVE_MESSAGES = Counter(
    'consumers_received_messages', 
    'Counts how many messages consumers have received'
)