from typing import Dict

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class QueryableModel(models.Model):
    """
    Makes a model queryable by the agent and provides additional information about the model.

    Attributes:
        description (str): A description of the model.
        field_descriptions (Dict[str, str]): A dictionary of field descriptions
    """

    description: str = None
    field_descriptions: Dict[str, str] = None

    class Meta:
        abstract = True


class Chat(models.Model):
    """
    Model to store user chats.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chats")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not self.user.is_staff:
            raise ValidationError(_("Only admin users can create chats."))

    class Meta:
        verbose_name = _("chat")
        verbose_name_plural = _("chats")


class Message(models.Model):
    """
    Model to store chat messages.
    """

    class Sender(models.TextChoices):
        AGENT = "AGENT", _("Agent")
        USER = "USER", _("User")

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(max_length=5, choices=Sender)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.chat.updated_at = self.updated_at
        self.chat.save(update_fields=["updated_at"])
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("message")
        verbose_name_plural = _("messages")
