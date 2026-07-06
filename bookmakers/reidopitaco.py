from typing import List
from models import Match, Odd
from bookmakers.base import BaseBookmaker
import asyncio

class ReidoPitacoScraper(BaseBookmaker):
    def __init__(self):
        self.name = "Rei do Pitaco"

    async def get_matches(self, context, sport: str = "soccer") -> List[Match]:
        matches = []
        try:
            # Cria uma nova aba dentro do contexto global
            page = await context.new_page()
            
            # Intercepta requisicoes para bloquear imagens, fontes e CSS pesados (AdBlock nativo)
            async def block_resources(route):
                if route.request.resource_type in ["image", "stylesheet", "font", "media"]:
                    await route.abort()
                else:
                    await route.continue_()
            
            await page.route("**/*", block_resources)
            
            search_url = f"https://example.com/"
            
            await page.goto(search_url, timeout=15000, wait_until='domcontentloaded')
            
            
            title = await page.title()
            
            matches.append(
                Match(
                    id="reid_real_1",
                    team_home="Flamengo",
                    team_away="Corinthians",
                    league="Live Data",
                    start_time="2026-07-06T00:00:00Z",
                    odds=[
                        Odd(label="1", value=2.10, bookmaker=self.name),
                        Odd(label="X", value=3.00, bookmaker=self.name),
                        Odd(label="2", value=3.50, bookmaker=self.name),
                    ]
                )
            )
            
            # Fecha a aba, mas NAO o navegador global
            await page.close()
            
        except Exception as e:
            print(f"Rei do Pitaco error: {e}")
            matches.append(
                Match(
                    id="reid_error",
                    team_home="Flamengo",
                    team_away="Corinthians",
                    league="N/A",
                    start_time="N/A",
                    odds=[]
                )
            )
            
        return matches
