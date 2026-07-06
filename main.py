from fastapi import FastAPI
from typing import List
import asyncio
from contextlib import asynccontextmanager
from playwright.async_api import async_playwright

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
from bookmakers.setegames import SeteGamesScraper
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

# Globals for Playwright
playwright_instance = None
browser = None
global_context = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global playwright_instance, browser, global_context
    print("Iniciando Playwright Global...")
    playwright_instance = await async_playwright().start()
    browser = await playwright_instance.chromium.launch(headless=True)
    global_context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    yield
    print("Desligando Playwright Global...")
    if global_context:
        await global_context.close()
    if browser:
        await browser.close()
    if playwright_instance:
        await playwright_instance.stop()

app = FastAPI(
    title="Betting Odds Aggregator API",
    description="API que agrega odds de 25 casas de apostas (Otimizada e Leve)",
    version="3.0.0",
    lifespan=lifespan
)

bookmakers = [
    BetnacionalScraper(), SportingbetScraper(), NovibetScraper(),
    BetssonScraper(), GalerabetScraper(), CasadeApostasScraper(),
    BetSulScraper(), BetFastScraper(), VBetScraper(), SeteGamesScraper(),
    ApostaGanhaScraper(), BrazinoSeteSeteSeteScraper(), ReidoPitacoScraper(),
    BrasilBetScraper(), LuvabetScraper(), F12betScraper(), SportyBetScraper(),
    RealsScraper(), HiperBetScraper(), SeuBetScraper(), H2betScraper(),
    CaesarsScraper(), BigScraper(), ApostarScraper(), BetBoomScraper()
]

# Semáforo limitando a 5 execuções simultâneas
semaphore = asyncio.Semaphore(5)

async def fetch_with_semaphore(bm):
    async with semaphore:
        return await bm.get_matches(global_context)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Casas de Apostas (Fase 3 Otimizada)"}

@app.get("/jogos", response_model=List[Match])
async def get_all_matches():
    tasks = [fetch_with_semaphore(bm) for bm in bookmakers]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    all_matches = []
    for result in results:
        if isinstance(result, list):
            all_matches.extend(result)
        else:
            print(f"Erro na extração: {result}")
            
    return all_matches
