# src/core/models/table.py
from typing import List, Dict, Any
import logging

# Получение логгера
logger = logging.getLogger(__name__)

class Table:
    def __init__(self, name: str):
        self.name: str = name
        self.columns: Dict[str, str] = {}
        self.primary_keys: List[str] = []
        self.foreign_keys: List[Dict[str, Any]] = []
        self.unique_columns: List[str] = []
        self.generated_rows: List[Dict[str, Any]] = []

    def add_column(self, column_name: str, column_type: str) -> None:
        if column_name.lower() not in ("primary", "foreign"):
            self.columns[column_name] = column_type
            logger.debug(f"Added column '{column_name}' with type '{column_type}' to table '{self.name}'")

    def set_primary_keys(self, primary_keys: List[str]) -> None:
        self.primary_keys = primary_keys
        logger.debug(f"Set primary keys {primary_keys} for table '{self.name}'")

    def add_foreign_key(self, column_name: str, referenced_table: str, referenced_column: str) -> None:
        self.foreign_keys.append({
            'column': column_name,
            'referenced_table': referenced_table,
            'referenced_column': referenced_column
        })
        logger.debug(f"Added foreign key '{column_name}' referencing '{referenced_table}.{referenced_column}' to table '{self.name}'")

    def add_unique_column(self, column: str):
        if column not in self.unique_columns:
            self.unique_columns.append(column)

    def log_generated_rows(self):
        logger.debug(f"Generated rows for table '{self.name}': {self.generated_rows}")
