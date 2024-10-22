
import random
from typing import List
import logging
from faker import Faker
from src.core.repositories.value_repository import IValueRepository

logger = logging.getLogger(__name__)

class FakerValueRepository(IValueRepository):
    def __init__(self):
        self.faker = Faker()
        Faker.seed(0)  # Для воспроизводимости

    def get_values(self, field_type: str) -> List[str]:
        """
        В этом хранилище метод get_values не используется, так как данные генерируются на лету.
        Возвращает пустой список.
        """
        logger.debug(f"get_values called for field_type '{field_type}' in FakerValueRepository. Returning empty list.")
        return []

    def get_random_value(self, field_type: str, referenced_values: List[str] = None) -> str:
        """
        Генерирует фейковое значение для заданного типа поля.
        Если переданы referenced_values, выбирает случайное значение из них.
        """
        if referenced_values:
            value = random.choice(referenced_values)
            logger.debug(
                f"Selected referenced value '{value}' for field type '{field_type}' using FakerValueRepository")
            return value

        if field_type.lower() in ["last name", "first name"]:
            value = self.faker.first_name() if field_type.lower() == "first name" else self.faker.last_name()
        elif field_type.lower() == "address":
            value = self.faker.address().replace("\n", ", ")
        elif field_type.lower() == "postal code":
            value = self.faker.postcode()
        elif field_type.lower() == "city":
            value = self.faker.city()
        elif field_type.lower() == "country":
            value = self.faker.country()
        elif field_type.lower() == "phone":
            value = self.faker.phone_number()
        elif field_type.lower() == "email":
            value = self.faker.email()
        elif field_type.lower() == "job":
            value = self.faker.job()
        elif field_type.lower() == "number [0,10]":
            value = str(random.randint(0, 10))
        elif field_type.lower() == "number [0,10000]":
            value = str(random.randint(0, 10000))
        elif field_type.lower() == "recent date":
            value = self.faker.date_between(start_date='-1y', end_date='today').isoformat()
        elif field_type.lower() == "date":
            value = self.faker.date()
        else:
            value = "unknown_value"
            logger.warning(f"Unknown field type '{field_type}'. Generated value set to 'unknown_value'.")

        logger.debug(f"Generated fake value '{value}' for field type '{field_type}' using FakerValueRepository")
        return value
