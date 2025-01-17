from pandasai import Agent as PandasAIAgent

from .config import get_config
from .connectors import get_connectors


class Agent(PandasAIAgent):
    """
    PandasAI Agent for chatting with the Django backend data.
    """

    def __init__(self):
        super().__init__(
            dfs=get_connectors(),
            config=get_config(),
        )
