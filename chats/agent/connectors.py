from typing import Any, Dict, List, Optional

from django.conf import settings
from pandasai.connectors import (
    MySQLConnector,
    OracleConnector,
    PostgreSQLConnector,
    SQLConnector,
    SqliteConnector,
)

from ..models import QueryableModel


def create_connector(
    table: str, description: Optional[str] = None, field_descriptions: Optional[Dict[str, str]] = None
):
    """
    Creates and returns a connector instance based on Django's default database configuration.

    Args:
        table (str): Name of the database table.
        description (Optional[str]): Description of the connector instance.
        field_descriptions (Optional[Dict[str, str]]): Descriptions for fields in the table.

    Returns:
        connector_cls: An instance of the relevant database connector class.
    """
    db_conf = settings.DATABASES["default"]

    engine_to_connector = {
        "django.db.backends.sqlite3": (SqliteConnector, None),
        "django.db.backends.postgresql": (PostgreSQLConnector, 5432),
        "django.db.backends.mysql": (MySQLConnector, 3306),
        "django.db.backends.oracle": (OracleConnector, 1521),
    }

    connector_cls, default_port = engine_to_connector.get(db_conf["ENGINE"], (None, None))

    if connector_cls is None:
        raise ValueError(f"Unsupported database engine: {db_conf['ENGINE']}")

    config = build_db_config(db_conf, table, default_port)

    return connector_cls(
        config=config,
        description=description,
        field_descriptions=field_descriptions,
    )


def build_db_config(db_conf: Dict[str, Any], table: str, default_port: Optional[int] = None) -> Dict[str, Any]:
    """
    Builds a generalized database configuration based on common settings.

    Args:
        db_conf (Dict[str, Any]): Django database settings.
        table (Dict[str, Any]): Table name for the database engine.
        default_port (Optional[int]): Default port for the database engine.

    Returns:
        Dict[str, Any]: Final configuration for the connector.
    """
    if db_conf["ENGINE"] == "django.db.backends.sqlite3":
        return {"database": db_conf["NAME"], "table": table}

    return {
        "host": db_conf.get("HOST", "localhost"),
        "port": db_conf.get("PORT", default_port),
        "database": db_conf["NAME"],
        "username": db_conf.get("USER"),
        "password": db_conf.get("PASSWORD"),
        "table": table,
    }


def get_model_configs(models: List[QueryableModel]) -> Dict[str, Dict[str, Any]]:
    """
    Returns a dictionary of model configurations.

    Args:
        models (List[QueryableModel]): A list of QueryableModel subclasses.

    Returns:
        Dict[str, Dict[str, Any]]: A dictionary of model configurations.
    """
    configs = {}

    for model in models:
        model_name = model._meta.model_name
        table_name = model._meta.db_table

        configs[model_name] = {
            "table": table_name,
            "description": model.description,
            "field_descriptions": model.field_descriptions,
        }

    return configs


def get_many_to_many_configs(models: List[QueryableModel]) -> Dict[str, Dict[str, str]]:
    """
    Returns a dictionary of many-to-many table configurations.

    Args:
        models (List[QueryableModel]): A list of QueryableModel subclasses.

    Returns:
        Dict[str, Dict[str, str]]: A dictionary of many-to-many table configurations.
    """
    configs = {}

    for model in models:
        for many_to_many in model._meta.many_to_many:
            related_model = many_to_many.remote_field.model

            if issubclass(related_model, QueryableModel):
                model_name = related_model._meta.model_name
                table_name = related_model._meta.db_table

                configs[model_name] = {
                    "table": table_name,
                    "description": model.description,
                    "field_descriptions": model.field_descriptions,
                }

    return configs


def get_queryable_models() -> List[QueryableModel]:
    """
    Returns a list of QueryableModel subclasses.

    Returns:
        List[QueryableModel]: A list of QueryableModel subclasses.
    """
    return QueryableModel.__subclasses__()


def get_connectors() -> List[SQLConnector]:
    """
    Returns a list of SQLConnector instances based on Django's default database configuration.

    Returns:
        List[SQLConnector]: A list of SQLConnector instances.
    """
    queryable_models = get_queryable_models()
    configs = get_many_to_many_configs(queryable_models) | get_model_configs(queryable_models)
    return [create_connector(**config) for config in configs.values()]
