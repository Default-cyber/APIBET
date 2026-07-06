from fastapi import FastAPI
from typing import List
import asyncio

from models import Match
from bookmakers.betnacional import BetnacionalScraper
from bookmakers.sportingbet import SportingbetScraper
from bookmakers.betsson import BetssonScraper

app = FastAPI(
    title="Betting Odds Aggregator API",
    description="API que agrega odds de diferentes casas de apostas",
    version="1.0.0"
)

# Registramos os scrapers das casas de apostas suportadas (Fase 1)
bookmakers = [
    BetnacionalScraper(),
    SportingbetScraper(),
    BetssonScraper(),
]

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Casas de Apostas"}

@app.get("/jogos", response_model=List[Match])
async def get_all_matches():
    """
    Busca os jogos em todas as casas de apostas registradas de forma simultânea.
    """
    tasks = [bookmaker.get_matches() for bookmaker in bookmakers]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    all_matches = []
    for result in results:
        if isinstance(result, list):
            all_matches.extend(result)
        else:
            print(f"Erro ao buscar dados de uma casa de aposta: {result}")
            
    return all_matches
