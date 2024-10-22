import re
from typing import List
import logging
from src.core.models.table import Table

# Получение логгера
logger = logging.getLogger(__name__)

class DDLParser:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read_file(self) -> List[Table]:
        with open(self.file_path, "r", encoding='utf-8') as f:
            lines = f.readlines()

        tables: List[Table] = []
        current_table: Table = None

        for line in lines:
            line = line.strip()

            # Пропускаем пустые строки
            if not line:
                continue

            # Обнаружение создания таблицы
            match_table = re.match(r"CREATE TABLE (\w+)", line, re.IGNORECASE)
            if match_table:
                table_name = match_table.group(1)
                current_table = Table(table_name)
                tables.append(current_table)
                logger.debug(f"Обнаружено создание таблицы: {table_name}")
                continue

            if current_table:
                # Обнаружение первичного ключа
                match_primary = re.match(r"PRIMARY KEY\s*\(([\w, ]+)\)", line, re.IGNORECASE)
                if match_primary:
                    primary_keys = [key.strip() for key in match_primary.group(1).split(",")]
                    current_table.set_primary_keys(primary_keys)
                    logger.debug(f"Установлены первичные ключи {primary_keys} для таблицы '{current_table.name}'")
                    continue

                # Обнаружение внешнего ключа
                match_foreign = re.match(r"FOREIGN KEY\s*\((\w+)\)\s+REFERENCES\s+(\w+)\s*\((\w+)\)", line, re.IGNORECASE)
                if match_foreign:
                    column_name = match_foreign.group(1)
                    referenced_table = match_foreign.group(2)
                    referenced_column = match_foreign.group(3)
                    current_table.add_foreign_key(column_name, referenced_table, referenced_column)
                    logger.debug(f"Добавлен внешний ключ '{column_name}' ссылающийся на '{referenced_table}.{referenced_column}' для таблицы '{current_table.name}'")
                    continue

                # Обнаружение определения столбца с возможными ограничениями
                # Пример: column_name INT UNIQUE NOT NULL
                match_column = re.match(
                    r"(\w+)\s+(\w+)(?:\s+(UNIQUE|NOT NULL|AUTO_INCREMENT|PRIMARY KEY))?,?",
                    line,
                    re.IGNORECASE
                )
                if match_column:
                    column_name = match_column.group(1)
                    column_type = match_column.group(2)
                    constraints = match_column.group(3)

                    current_table.add_column(column_name, column_type)
                    logger.debug(f"Добавлен столбец '{column_name}' с типом '{column_type}' в таблицу '{current_table.name}'")

                    if constraints:
                        constraint_upper = constraints.upper()
                        if constraint_upper == "UNIQUE":
                            current_table.add_unique_column(column_name)
                            logger.debug(f"Столбец '{column_name}' помечен как UNIQUE в таблице '{current_table.name}'")
                        elif constraint_upper == "PRIMARY KEY":
                            current_table.set_primary_keys([column_name])
                            logger.debug(f"Столбец '{column_name}' помечен как PRIMARY KEY в таблице '{current_table.name}'")
                    continue

                # Обнаружение отдельного ограничения UNIQUE
                # Пример: UNIQUE (column1, column2)
                match_unique = re.match(r"UNIQUE\s*\(([\w, ]+)\)", line, re.IGNORECASE)
                if match_unique:
                    unique_columns = [col.strip() for col in match_unique.group(1).split(",")]
                    for col in unique_columns:
                        current_table.add_unique_column(col)
                        logger.debug(f"Столбец '{col}' помечен как UNIQUE в таблице '{current_table.name}'")
                    continue

                # Конец определения таблицы
                if line.endswith(");"):
                    logger.debug(f"Конец определения таблицы '{current_table.name}'")
                    current_table = None
                    continue

        return tables

    def sort_tables_by_dependencies(self, tables: List[Table]) -> List[Table]:
        sorted_tables: List[Table] = []
        tables_with_dependencies = {table.name: table for table in tables if table.foreign_keys}

        # Таблицы без зависимостей
        for table in tables:
            if not table.foreign_keys:
                sorted_tables.append(table)
                logger.debug(f"Добавлена таблица '{table.name}' в отсортированный список (без зависимостей)")

        # Разрешение зависимостей
        while tables_with_dependencies:
            added = False
            for table_name in list(tables_with_dependencies):
                table = tables_with_dependencies[table_name]
                if all(fk['referenced_table'] in [t.name for t in sorted_tables] for fk in table.foreign_keys):
                    sorted_tables.append(table)
                    del tables_with_dependencies[table_name]
                    logger.debug(f"Добавлена таблица '{table.name}' в отсортированный список (зависимости разрешены)")
                    added = True
            if not added:
                logger.error("Обнаружена циклическая зависимость или отсутствуют ссылки на таблицы.")
                break  # Предотвращаем бесконечный цикл в случае циклических зависимостей
        return sorted_tables
