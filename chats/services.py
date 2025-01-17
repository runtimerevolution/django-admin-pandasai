from django.contrib.auth.models import User
from django.db import transaction

from .agent import Agent
from .models import Chat, Message


class ChatService:
    def __init__(self, chat: Chat):
        self.chat = chat
        self.agent = Agent()

    def send_message(self, content: str) -> Message:
        """
        Creates a user message and a agent response message.

        Args:
            chat_id (int): The chat ID.
            content (str): The message content.

        Returns:
            Message: The agent response message.
        """
        with transaction.atomic():
            Message.objects.create(chat=self.chat, content=content, sender=Message.Sender.USER)

            try:
                output = self.agent.chat(content)
            except Exception as e:
                output = f"There was problem generating an answer: {str(e)}"

            return Message.objects.create(chat=self.chat, content=output, sender=Message.Sender.AGENT)


class UserService:
    def __init__(self, user: User):
        self.user = user

    def get_latest_or_create_chat(self) -> Chat:
        """
        Returns the latest chat or creates a new one if the latest chat has messages.

        Args:
            user (User): A User instance.

        Returns:
            Chat: A Chat instance
        """
        latest_chat = Chat.objects.filter(user=self.user).order_by("-created_at").first()

        if latest_chat is None or latest_chat.messages.exists():
            return Chat.objects.create(user=self.user)

        return latest_chat
