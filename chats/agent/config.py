from django.conf import settings
from pandasai import llm

from .parser import HtmlResponseParser


def get_config() -> dict:
    """
    Returns the configuration for the PandasAI agent.

    Returns:
        Dict[str, Any]: The configuration for the PandasAI agent.
    """
    config = getattr(settings, "PANDASAI_CONFIG", {}).copy()

    if "llm" in config:
        options = config.get("llm_options", {})
        config["llm"] = getattr(llm, config["llm"])(**options)

    config.update(
        {
            "save_charts": False,
            "open_charts": False,
            "direct_sql": True,
            "response_parser": HtmlResponseParser,
        }
    )

    return config
