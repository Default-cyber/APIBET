from typing import List
from models import Match, Odd
from bookmakers.base import BaseBookmaker
import asyncio

class BigScraper(BaseBookmaker):
    def __init__(self):
        self.name = "Big"

    async def get_matches(self, sport: str = "soccer") -> List[Match]:
        await asyncio.sleep(0.5) # Simula o tempo de rede
        
        matches = [
            Match(
                id="big_1",
                team_home="Flamengo",
                team_away="Vasco",
                league="Brasileirão Serie A",
                start_time="2026-07-05T16:00:00Z",
                odds=[
                    Odd(label="1", value=1.85, bookmaker=self.name),
                    Odd(label="X", value=3.20, bookmaker=self.name),
                    Odd(label="2", value=4.10, bookmaker=self.name),
                ]
            )
        ]
        return matches
