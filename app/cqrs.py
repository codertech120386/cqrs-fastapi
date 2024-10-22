from app.db import add_user_to_db, get_users_from_db


class CommandHandler:
    def handle_create_user(self, user_id: int, name: str):
        print(f"Handling CreateUserCommand: {user_id}, {name}")
        add_user_to_db(user_id, name)


class QueryHandler:
    def handle_get_users(self):
        print("Handling GetUsersQuery")
        return get_users_from_db()
