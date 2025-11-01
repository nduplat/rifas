from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseLoteriaService(ABC):
    @abstractmethod
    def get_results(self, date: str, loteria_id: str) -> Optional[Dict[str, Any]]:
        """Get lottery results for a specific date and lottery"""
        pass

    @abstractmethod
    def validate_loteria(self, loteria_id: str) -> bool:
        """Validate if lottery exists"""
        pass