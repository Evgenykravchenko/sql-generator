from abc import ABC, abstractmethod
from typing import List

class IValueRepository(ABC):
    @abstractmethod
    def get_values(self, field_type: str) -> List[str]:
        pass

    @abstractmethod
    def get_random_value(self, field_type: str, referenced_values: List[str] = None) -> str:
        pass
