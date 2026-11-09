from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
from dataclasses import dataclass, asdict

load_dotenv()

DB_USER_NAME = os.getenv("MONGO_DB_USER_NAME")
DB_USER_PASS = os.getenv("MONGO_DB_USER_PASS")

client = MongoClient(
    f"mongodb://{DB_USER_NAME}:{DB_USER_PASS}@mongodb:27017/?authSource=admin",
    server_api=ServerApi('1')
)

db = client.chat

@dataclass
class UserMessage:
    username: str
    message: str

class DB:
    def add_message(self, message: UserMessage) -> None:
        db.messages.insert_one(asdict(message))

    def get_all_messages(self) -> list[UserMessage]:
        return list(db.messages.find({}))