from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import random
from .base import BaseLoteriaService


class MockLoteriaService(BaseLoteriaService):
    def __init__(self):
        # Mock data for different lotteries
        self.mock_loterias = {
            "loteria-nacional": {
                "name": "Lotería Nacional",
                "prizes": ["Primer Premio", "Segundo Premio", "Tercer Premio"],
                "numbers": 5
            },
            "baloto": {
                "name": "Baloto",
                "prizes": ["Baloto Match 5", "Baloto Match 4", "Baloto Match 3"],
                "numbers": 6
            },
            "chance": {
                "name": "Chance",
                "prizes": ["Chance Match 4", "Chance Match 3", "Chance Match 2"],
                "numbers": 4
            }
        }

        # Pre-configured results for specific dates
        self.mock_results = {
            "2023-10-01": {
                "loteria-nacional": {
                    "date": "2023-10-01",
                    "results": {
                        "Primer Premio": "12345",
                        "Segundo Premio": "67890",
                        "Tercer Premio": "54321"
                    }
                },
                "baloto": {
                    "date": "2023-10-01",
                    "results": {
                        "Baloto Match 5": "12-34-56-78-90-11",
                        "Baloto Match 4": "22-33-44-55-66-77",
                        "Baloto Match 3": "88-99-10-20-30-40"
                    }
                }
            },
            "2023-10-02": {
                "chance": {
                    "date": "2023-10-02",
                    "results": {
                        "Chance Match 4": "1111",
                        "Chance Match 3": "2222",
                        "Chance Match 2": "3333"
                    }
                }
            }
        }

    def get_results(self, date: str, loteria_id: str) -> Optional[Dict[str, Any]]:
        """Get lottery results for a specific date and lottery"""
        if not self.validate_loteria(loteria_id):
            return None

        # Check if we have pre-configured results for this date
        if date in self.mock_results and loteria_id in self.mock_results[date]:
            return self.mock_results[date][loteria_id]

        # Generate mock results for the date
        return self._generate_mock_results(date, loteria_id)

    def validate_loteria(self, loteria_id: str) -> bool:
        """Validate if lottery exists"""
        return loteria_id in self.mock_loterias

    def _generate_mock_results(self, date: str, loteria_id: str) -> Dict[str, Any]:
        """Generate mock results for a given date and lottery"""
        loteria_config = self.mock_loterias[loteria_id]

        results = {}
        for prize in loteria_config["prizes"]:
            if loteria_config["numbers"] == 1:
                # Single number lotteries
                results[prize] = str(random.randint(0, 9))
            else:
                # Multi-number lotteries
                numbers = []
                for _ in range(loteria_config["numbers"]):
                    numbers.append(str(random.randint(0, 99)).zfill(2))
                results[prize] = "-".join(numbers)

        return {
            "date": date,
            "results": results
        }