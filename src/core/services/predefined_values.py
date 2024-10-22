from typing import List, Optional
import logging
from src.core.repositories.value_repository import IValueRepository

logger = logging.getLogger(__name__)

class PredefinedValues:
    def __init__(self, repository: IValueRepository):
        self.repository = repository

    def get_value(self, field_type: str, referenced_values: Optional[List[str]] = None) -> str:
        """
        Возвращает случайное значение для заданного типа поля.
        Если переданы referenced_values, используется для выбора значения внешнего ключа.
        """
        value = self.repository.get_random_value(field_type, referenced_values)
        logger.debug(f"Generated value '{value}' for field type '{field_type}' with referenced_values={referenced_values}")
        return value
