from fastapi import FastAPI
from typing import List
import asyncio
import json
import os
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

bookmakers = [
    BetnacionalScraper(), SportingbetScraper(), NovibetScraper(),
    BetssonScraper(), GalerabetScraper(), CasadeApostasScraper(),
    BetSulScraper(), BetFastScraper(), VBetScraper(), SeteGamesScraper(),
    ApostaGanhaScraper(), BrazinoSeteSeteSeteScraper(), ReidoPitacoScraper(),
    BrasilBetScraper(), LuvabetScraper(), F12betScraper(), SportyBetScraper(),
    RealsScraper(), HiperBetScraper(), SeuBetScraper(), H2betScraper(),
    CaesarsScraper(), BigScraper(), ApostarScraper(), BetBoomScraper()
]

# Flag para parar o loop quando o servidor desligar
keep_scraping = True

async def scraping_loop():
    print("Iniciando rotina de extração invisível (Background Task)...")
    while keep_scraping:
        try:
            print("====================================")
            print("Abrindo navegador Playwright...")
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
                
                all_matches = []
                
                # Executa uma por vez para gastar o mínimo de RAM possível
                for bm in bookmakers:
                    if not keep_scraping:
                        break
                    print(f"Extraindo: {bm.name}...")
                    try:
                        matches = await bm.get_matches(context)
                        if matches:
                            all_matches.extend(matches)
                    except Exception as e:
                        print(f"Falha ao extrair {bm.name}: {e}")
                
                # Desliga o navegador completamente para limpar a RAM do servidor
                await context.close()
                await browser.close()
            
            # Converte os resultados para Dicionários (para facilitar salvar em JSON)
            if all_matches:
                print(f"Extração concluída com sucesso. Salvando {len(all_matches)} itens no arquivo dados.json...")
                data_to_save = [match.model_dump() if hasattr(match, 'model_dump') else match.dict() for match in all_matches]
                
                # Salva o resultado num arquivo físico
                with open("dados.json", "w", encoding="utf-8") as f:
                    json.dump(data_to_save, f, ensure_ascii=False, indent=2)
            
            print("Dormindo por 60 segundos...")
            await asyncio.sleep(60)
            
        except Exception as main_e:
            print(f"Erro no loop principal: {main_e}")
            await asyncio.sleep(60) # Espera e tenta de novo

@asynccontextmanager
async def lifespan(app: FastAPI):
    global keep_scraping
    keep_scraping = True
    # Dispara a tarefa em loop silencioso no fundo da aplicação
    asyncio.create_task(scraping_loop())
    yield
    print("Desligando aplicação...")
    keep_scraping = False

app = FastAPI(
    title="Betting Odds Aggregator API",
    description="API Estática Leve (Fase 5)",
    version="5.0.0",
    lifespan=lifespan
)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Casas de Apostas (Fase 5: Leitura de Arquivo)"}

@app.get("/jogos")
async def get_all_matches():
    """
    Esta rota NÃO faz extração. Ela apenas lê o arquivo 'dados.json' super leve
    e cospe na tela imediatamente. 
    """
    file_path = "dados.json"
    
    if not os.path.exists(file_path):
        return {
            "status": "processing",
            "message": "O arquivo de dados ainda não foi criado. O robô está gerando agora no fundo. Volte em alguns segundos.",
            "matches": []
        }
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            dados = json.load(f)
        return dados
    except Exception as e:
        return {
            "status": "error",
            "message": f"Falha ao ler o arquivo json: {e}",
            "matches": []
        }
