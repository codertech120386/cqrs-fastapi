import pika

RABBITMQ_HOST = 'localhost'
QUEUE_NAME = 'commands_queue'


def get_rabbitmq_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)
    return connection, channel


def send_message_to_queue(message: str):
    connection, channel = get_rabbitmq_connection()
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=message)
    print(f"Sent message to queue: {message}")
    connection.close()


def receive_messages_from_queue(callback):
    connection, channel = get_rabbitmq_connection()

    def on_message(ch, method, properties, body):
        callback(body.decode())

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_message, auto_ack=True)
    print("Waiting for messages...")
    channel.start_consuming()
