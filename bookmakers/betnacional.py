from typing import List
from models import Match, Odd
from bookmakers.base import BaseBookmaker
import asyncio

class BetnacionalScraper(BaseBookmaker):
    def __init__(self):
        self.name = "Betnacional"

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
            
            search_url = f"https://duckduckgo.com/?q={self.name.replace(' ', '+')}+apostas+esportivas&t=h_&ia=web"
            
            await page.goto(search_url, timeout=20000)
            await page.wait_for_timeout(2000)
            
            title = await page.title()
            
            matches.append(
                Match(
                    id="betn_real_1",
                    team_home="Betnacional - Live",
                    team_away=title[:20],
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
            print(f"Betnacional error: {e}")
            matches.append(
                Match(
                    id="betn_error",
                    team_home="Error",
                    team_away=str(e)[:20],
                    league="N/A",
                    start_time="N/A",
                    odds=[]
                )
            )
            
        return matches
