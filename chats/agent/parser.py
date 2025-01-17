import base64
from typing import Any, Dict

import pandas as pd
from django.forms import URLField
from pandasai.responses.response_parser import ResponseParser


class HtmlResponseParser(ResponseParser):
    def parse(self, result: Dict[str, Any]) -> str:
        """
        Parses the result into an HTML format.

        Args:
            result (dict): The result dictionary.

        Returns:
            str: The HTML formatted result.
        """
        if not isinstance(result, dict) or any(key not in result for key in ["type", "value"]):
            raise ValueError("Unsupported result format")

        match result["type"]:
            case "plot":
                return self.format_plot(result)
            case "dataframe":
                return self.format_dataframe(result)
            case "string":
                return self.format_string(result)
            case _:
                return str(result["value"])

    def format_plot(self, result: Dict[str, Any]) -> str:
        """
        Formats the plot result into an HTML image tag.

        Args:
            result (dict): The result dictionary.

        Returns:
            str: The HTML formatted plot.
        """
        src = result["value"]

        if isinstance(result["value"], str) and "data:image/png;base64" not in result["value"]:
            with open(result["value"], "rb") as image_file:
                data = base64.b64encode(image_file.read()).decode("utf-8")
                src = f"data:image/png;base64, {data}"

        return f'<img class="plot" src="{src}">'

    def format_dataframe(self, result: Dict[str, Any]) -> str:
        """
        Formats the DataFrame result into an HTML table.

        Args:
            result (dict): The result dictionary.

        Returns:
            str: The HTML formatted DataFrame.
        """
        if isinstance(result["value"], dict):
            result["value"] = pd.DataFrame(result["value"])

        return result["value"].to_html(index=False, border=0)

    def format_string(self, result: Dict[str, Any]) -> str:
        """
        Formats the string result into an HTML link or image tag.

        Args:
            result (dict): The result dictionary.

        Returns:
            str: The HTML formatted string.
        """
        url_field = URLField()
        try:
            url = url_field.clean(result["value"])
            if url.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif", ".svg", ".webp", ".ico")):
                return f'<img class="image" src="{url}">'
            else:
                return f'<a class="link" href="{url}">{result["value"]}</a>'
        except:
            return result["value"]
