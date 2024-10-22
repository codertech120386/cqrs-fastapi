from fastapi import FastAPI, BackgroundTasks
from app.cqrs import CommandHandler, QueryHandler
from app.schema import CreateUserCommand, UserResponse
from app.rabbitmq import send_message_to_queue, get_rabbitmq_connection, QUEUE_NAME
import json

app = FastAPI()

command_handler = CommandHandler()
query_handler = QueryHandler()


@app.get("/receive-messages/")
async def receive_messages(background_tasks: BackgroundTasks):
    """Endpoint to start background task to receive messages."""
    background_tasks.add_task(consume_messages)
    return {"message": "Started consuming messages"}


@app.post("/users/")
async def create_user(command: CreateUserCommand, background_tasks: BackgroundTasks):
    # Send CreateUserCommand to RabbitMQ queue
    message = command.json()
    background_tasks.add_task(send_message_to_queue, message)
    return {"message": "User creation command received."}


@app.get("/users/", response_model=list[UserResponse])
async def get_users():
    # Handle GetUsersQuery
    users = query_handler.handle_get_users()
    return [{"id": user[0], "name": user[1]} for user in users]


def consume_messages():
    """Consume messages from RabbitMQ queue."""
    connection, channel = get_rabbitmq_connection()

    # Start consuming messages from the queue
    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback,
        auto_ack=True
    )
    print("Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


def callback(ch, method, properties, body):
    """Process message from queue."""
    print(f"Received message: {body.decode()}")
    # Here you can add custom processing logic.
