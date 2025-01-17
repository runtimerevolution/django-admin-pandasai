import re

from django import template

from ..models import Message

register = template.Library()


@register.filter(name="format_message")
def format_message(message: Message):
    """
    Formats the message content.

    Args:
        message (Message): A Message instance.

    Returns:
        str: The formatted message content.
    """
    if re.match(r"<[^>]+>", message.content):
        return message.content
    return message.content.replace("\n", "<br>")
