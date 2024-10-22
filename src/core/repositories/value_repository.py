import os
import random
from typing import List
import logging

from core.repositories.value_repository_interface import IValueRepository
from src.utils.file_reader import read_file

# Получение логгера
logger = logging.getLogger(__name__)

class ValueRepository(IValueRepository):
    RESOURCES_FOLDER = os.getenv('RESOURCES_PATH', 'resources/files/')

    data_files = {
        "Last name": "lastname.txt",
        "First name": "firstname.txt",
        "Address": "address.txt",
        "Postal code": "postal_code.txt",
        "City": "city.txt",
        "Country": "country.txt",
        "Phone": "phone.txt",
        "Email": "email.txt",
        "Job": "job.txt",
        "Number [0,10]": "number_0_10.txt",
        "Number [0,10000]": "number_0_10000.txt",
        "Recent date": "recent_date.txt",
        "Date": "date.txt"
    }

    def get_values(self, field_type: str) -> List[str]:
        """
        Возвращает список всех значений для заданного типа поля.
        """
        file = self.data_files.get(field_type)
        if file:
            file_path = os.path.join(self.RESOURCES_FOLDER, file)
            logger.debug(f"Reading values from {file_path} for field type '{field_type}'")
            return read_file(file_path)
        logger.warning(f"No data file found for field type '{field_type}'")
        return []

    def get_random_value(self, field_type: str, referenced_values: List[str] = None) -> str:
        """
        Возвращает случайное значение для заданного типа поля.
        Если переданы referenced_values, выбирает случайное значение из них.
        """
        if referenced_values:
            value = random.choice(referenced_values)
            logger.debug(f"Selected referenced value '{value}' for field type '{field_type}'")
            return value
        values = self.get_values(field_type)
        if values:
            value = random.choice(values)
            logger.debug(f"Selected random value '{value}' from '{field_type}'")
            return value
        logger.error(f"No values available for field type '{field_type}'")
        return "unknown_value"