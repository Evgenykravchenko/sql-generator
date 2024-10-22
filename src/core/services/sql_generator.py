# src/core/services/sql_generator.py
from typing import Dict
import logging
from src.core.models.table import Table
from src.core.services.predefined_values import PredefinedValues

# Получение логгера
logger = logging.getLogger(__name__)

class SQLGenerator:
    def __init__(self, predefined_values: PredefinedValues):
        self.predefined_values = predefined_values
        self.unique_values: Dict[str, set] = {}  # Для хранения уникальных значений по столбцам

    def is_numeric_field(self, field_type: str) -> bool:
        """
        Определяет, является ли тип поля числовым.
        """
        numeric_keywords = ['INT', 'LONG', 'NUMBER', 'DECIMAL', 'FLOAT', 'DOUBLE', 'SMALLINT', 'BIGINT']
        field_type_upper = field_type.upper()
        return any(keyword in field_type_upper for keyword in numeric_keywords)

    def is_date_field(self, field_type: str) -> bool:
        """
        Определяет, является ли тип поля датой.
        """
        date_keywords = ['DATE', 'DATETIME', 'TIMESTAMP', 'TIME', 'YEAR']
        field_type_upper = field_type.upper()
        return any(keyword in field_type_upper for keyword in date_keywords)

    def format_value(self, field_type: str, value: str) -> str:
        """
        Форматирует значение на основе типа поля.
        - Числовые типы: Без кавычек.
        - Даты: Использовать to_date('value', 'YYYY-MM-DD').
        - Другие типы: Обрамлять в кавычки.
        """
        if self.is_numeric_field(field_type):
            logger.debug(f"Поле '{field_type}' является числовым. Значение: {value}")
            return value.strip("'")  # Без кавычек
        elif self.is_date_field(field_type):
            logger.debug(f"Поле '{field_type}' является датой. Значение: {value}")
            stripped_value = value.strip("'")
            return f"to_date('{stripped_value}', 'YYYY-MM-DD')"
        else:
            logger.debug(f"Поле '{field_type}' является строковым. Значение: {value}")
            stripped_value = value.strip("'")
            return f"'{stripped_value}'"

    def generate_insert_query(self, table: Table, referenced_tables: Dict[str, Table]) -> str:
        insert_columns = []
        values = []

        for col_name, col_type in table.columns.items():
            # Проверка, является ли столбец внешним ключом
            fk = next((fk for fk in table.foreign_keys if fk['column'] == col_name), None)
            if fk:
                referenced_table = referenced_tables.get(fk['referenced_table'])
                if referenced_table and referenced_table.generated_rows:
                    # Извлекаем значения из столбца, на который ссылается внешний ключ
                    referenced_values = [row[fk['referenced_column']] for row in referenced_table.generated_rows]
                    logger.debug(f"Генерация значения внешнего ключа для '{col_name}' из '{fk['referenced_table']}.{fk['referenced_column']}' с доступными значениями: {referenced_values}")
                    value = self.predefined_values.get_value(col_type, referenced_values)
                else:
                    # Обработка отсутствия сгенерированных значений для внешнего ключа
                    logger.error(f"Нет сгенерированных значений для внешнего ключа '{col_name}', ссылающегося на таблицу '{fk['referenced_table']}'")
                    raise ValueError(f"Нет сгенерированных значений для внешнего ключа '{col_name}', ссылающегося на таблицу '{fk['referenced_table']}'")
            else:
                # Для обычных полей используем предопределенные значения
                logger.debug(f"Генерация значения для '{col_name}' с типом поля '{col_type}'")
                value = self.predefined_values.get_value(col_type)

            # Форматирование значения
            formatted_value = self.format_value(col_type, value)

            # Проверка уникальности, если столбец уникален или является первичным ключом
            if col_name in table.unique_columns or col_name in table.primary_keys:
                if col_name not in self.unique_values:
                    self.unique_values[col_name] = set()
                attempts = 0
                max_attempts = 1000
                original_value = formatted_value
                while formatted_value in self.unique_values[col_name]:
                    value = self.predefined_values.get_value(col_type)
                    formatted_value = self.format_value(col_type, value)
                    attempts += 1
                    if attempts > max_attempts:
                        logger.error(f"Невозможно сгенерировать уникальное значение для столбца '{col_name}' после {max_attempts} попыток.")
                        raise ValueError(f"Невозможно сгенерировать уникальное значение для столбца '{col_name}'.")
                self.unique_values[col_name].add(formatted_value)
                if attempts > 0:
                    logger.debug(f"Сгенерировано новое уникальное значение для '{col_name}': {formatted_value}")

            insert_columns.append(col_name)
            values.append(formatted_value)

        columns_str = ", ".join(insert_columns)
        values_str = ", ".join(values)

        query = f"INSERT INTO {table.name} ({columns_str}) VALUES ({values_str});"
        logger.info(f"Сгенерированный SQL-запрос: {query}")

        # Сохраняем сгенерированные значения для использования в других таблицах
        table.generated_rows.append(dict(zip(insert_columns, values)))

        return query

    def generate_insert_query_manual(self, table: Table) -> str:
        insert_columns = []
        values = []

        for col_name, col_type in table.columns.items():
            value = self.predefined_values.get_value(col_type)
            formatted_value = self.format_value(col_type, value)

            # Проверка уникальности, если столбец уникален или является первичным ключом
            if col_name in table.unique_columns or col_name in table.primary_keys:
                if col_name not in self.unique_values:
                    self.unique_values[col_name] = set()
                attempts = 0
                max_attempts = 1000
                original_value = formatted_value
                while formatted_value in self.unique_values[col_name]:
                    value = self.predefined_values.get_value(col_type)
                    formatted_value = self.format_value(col_type, value)
                    attempts += 1
                    if attempts > max_attempts:
                        logger.error(f"Невозможно сгенерировать уникальное значение для столбца '{col_name}' после {max_attempts} попыток.")
                        raise ValueError(f"Невозможно сгенерировать уникальное значение для столбца '{col_name}'.")
                self.unique_values[col_name].add(formatted_value)
                if attempts > 0:
                    logger.debug(f"Сгенерировано новое уникальное значение для '{col_name}': {formatted_value}")

            insert_columns.append(col_name)
            values.append(formatted_value)

        columns_str = ", ".join(insert_columns)
        values_str = ", ".join(values)

        query = f"INSERT INTO {table.name} ({columns_str}) VALUES ({values_str});"
        logger.info(f"Сгенерированный SQL-запрос: {query}")

        table.generated_rows.append(dict(zip(insert_columns, values)))

        return query
