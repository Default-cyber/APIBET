from fastapi import FastAPI
from typing import List
import asyncio

from models import Match
from bookmakers.betnacional import BetnacionalScraper
from bookmakers.sportingbet import SportingbetScraper
from bookmakers.novibet import NovibetScraper
from bookmakers.betsson import BetssonScraper
from bookmakers.galerabet import GalerabetScraper
from bookmakers.casadeapostas import CasadeApostasScraper
from bookmakers.betsul import BetSulScraper
from bookmakers.betfast import BetFastScraper
from bookmakers.vbet import VBetScraper
from bookmakers.7games import SeteGamesScraper
from bookmakers.apostaganha import ApostaGanhaScraper
from bookmakers.brazino777 import BrazinoSeteSeteSeteScraper
from bookmakers.reidopitaco import ReidoPitacoScraper
from bookmakers.brasilbet import BrasilBetScraper
from bookmakers.luvabet import LuvabetScraper
from bookmakers.f12bet import F12betScraper
from bookmakers.sportybet import SportyBetScraper
from bookmakers.reals import RealsScraper
from bookmakers.hiperbet import HiperBetScraper
from bookmakers.seubet import SeuBetScraper
from bookmakers.h2bet import H2betScraper
from bookmakers.caesars import CaesarsScraper
from bookmakers.big import BigScraper
from bookmakers.apostar import ApostarScraper
from bookmakers.betboom import BetBoomScraper

app = FastAPI(
    title="Betting Odds Aggregator API",
    description="API que agrega odds de diferentes casas de apostas em tempo real",
    version="2.0.0"
)

# Registramos TODOS os 25 scrapers das casas de apostas suportadas (Fase 2)
bookmakers = [
    BetnacionalScraper(),
    SportingbetScraper(),
    NovibetScraper(),
    BetssonScraper(),
    GalerabetScraper(),
    CasadeApostasScraper(),
    BetSulScraper(),
    BetFastScraper(),
    VBetScraper(),
    SeteGamesScraper(),
    ApostaGanhaScraper(),
    BrazinoSeteSeteSeteScraper(),
    ReidoPitacoScraper(),
    BrasilBetScraper(),
    LuvabetScraper(),
    F12betScraper(),
    SportyBetScraper(),
    RealsScraper(),
    HiperBetScraper(),
    SeuBetScraper(),
    H2betScraper(),
    CaesarsScraper(),
    BigScraper(),
    ApostarScraper(),
    BetBoomScraper(),
]

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Casas de Apostas (Fase 2 - 25 sites)"}

@app.get("/jogos", response_model=List[Match])
async def get_all_matches():
    """
    Busca os jogos em todas as 25 casas de apostas registradas de forma simultânea via Playwright.
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
