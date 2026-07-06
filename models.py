from pydantic import BaseModel
from typing import List, Optional

class Odd(BaseModel):
    label: str  # e.g., '1', 'X', '2', 'Over 2.5'
    value: float
    bookmaker: str

class Match(BaseModel):
    id: str
    team_home: str
    team_away: str
    league: str
    start_time: str
    odds: List[Odd] = []
