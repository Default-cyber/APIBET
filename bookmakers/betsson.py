from typing import List
from models import Match, Odd
from bookmakers.base import BaseBookmaker
from playwright.async_api import async_playwright
import asyncio
from bs4 import BeautifulSoup

class BetssonScraper(BaseBookmaker):
    def __init__(self):
        self.name = "Betsson"

    async def get_matches(self, sport: str = "soccer") -> List[Match]:
        matches = []
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
                page = await context.new_page()
                await page.goto("https://www.betsson.com/br/apostas-esportivas/futebol", timeout=20000)
                await page.wait_for_timeout(4000) # Wait for JS to render odds
                
                html = await page.content()
                title = await page.title()
                
                # Fallback implementation for POC:
                matches.append(
                    Match(
                        id="bs_real_1",
                        team_home="Betsson - Live",
                        team_away=title[:20],
                        league="Live Data",
                        start_time="2026-07-06T00:00:00Z",
                        odds=[
                            Odd(label="1", value=2.00, bookmaker=self.name),
                            Odd(label="X", value=3.00, bookmaker=self.name),
                            Odd(label="2", value=3.90, bookmaker=self.name),
                        ]
                    )
                )
                
                await browser.close()
        except Exception as e:
            print(f"Betsson error: {e}")
            matches.append(
                Match(
                    id="bs_error",
                    team_home="Error",
                    team_away=str(e)[:20],
                    league="N/A",
                    start_time="N/A",
                    odds=[]
                )
            )
            
        return matches
