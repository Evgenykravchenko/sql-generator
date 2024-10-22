from typing import List
import os
import logging

# Получение логгера
logger = logging.getLogger(__name__)

def read_file(file_path: str) -> List[str]:
    if not os.path.isabs(file_path):
        # Преобразуем относительный путь в абсолютный для отладки
        file_path = os.path.abspath(file_path)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        logger.error(f"The file {file_path} could not be found.")
        return []
