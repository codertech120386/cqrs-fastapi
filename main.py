import json
from app.rabbitmq import receive_messages_from_queue
from app.cqrs import CommandHandler
import uvicorn

command_handler = CommandHandler()


def on_message_received(message: str):
    # Deserialize the message and handle it as a command
    command_data = json.loads(message)
    print(command_data)
    command_handler.handle_create_user(command_data['user_id'], command_data['name'])


if __name__ == "__main__":
    # Start FastAPI server
    uvicorn.run("app.api:app", host="127.0.0.1", port=8000, reload=True)

    # Start RabbitMQ consumer in background
    receive_messages_from_queue(on_message_received)
