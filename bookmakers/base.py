from typing import List
from models import Match
from abc import ABC, abstractmethod

class BaseBookmaker(ABC):
    def __init__(self):
        self.name = "Base"

    @abstractmethod
    async def get_matches(self, context, sport: str = "soccer") -> List[Match]:
        """
        Método assíncrono para buscar jogos e odds.
        Deve ser implementado por cada casa de aposta.
        """
        pass
