from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List


@dataclass
class Message:
    sender: str
    receiver: str
    message: str
    timestamp: str


class Chat:
    def __init__(self) -> None:
        self.users: Dict[str, List[Message]] = {}

    def add_user(self, username: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = []
        return True

    def remove_user(self, username: str) -> bool:
        return self.users.pop(username, None) is not None

    def send_message(self, sender: str, receiver: str, message: str) -> bool:
        if sender not in self.users or receiver not in self.users:
            return False
        timestamp = self.get_current_time()
        msg = Message(sender, receiver, message, timestamp)
        self.users[sender].append(msg)
        self.users[receiver].append(msg)
        return True

    def get_messages(self, username: str) -> List[Message]:
        return self.users.get(username, []).copy()

    def get_users(self) -> Dict[str, List[Message]]:
        # Return a shallow copy to mimic C++ value return
        return {user: msgs.copy() for user, msgs in self.users.items()}

    @staticmethod
    def get_current_time() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
