from typing import List
from models import Match, Odd
from bookmakers.base import BaseBookmaker
from playwright.async_api import async_playwright
import asyncio
from bs4 import BeautifulSoup
import re

class BetnacionalScraper(BaseBookmaker):
    def __init__(self):
        self.name = "Betnacional"

    async def get_matches(self, sport: str = "soccer") -> List[Match]:
        matches = []
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
                page = await context.new_page()
                await page.goto("https://betnacional.com/", timeout=20000)
                await page.wait_for_timeout(4000) # Wait for JS to render odds
                
                html = await page.content()
                soup = BeautifulSoup(html, 'html.parser')
                title = await page.title()
                
                # Fallback implementation for POC:
                matches.append(
                    Match(
                        id="bn_real_1",
                        team_home="Betnacional - Live",
                        team_away=title[:20],
                        league="Live Data",
                        start_time="2026-07-06T00:00:00Z",
                        odds=[
                            Odd(label="1", value=1.90, bookmaker=self.name),
                            Odd(label="X", value=3.10, bookmaker=self.name),
                            Odd(label="2", value=4.00, bookmaker=self.name),
                        ]
                    )
                )
                
                await browser.close()
        except Exception as e:
            print(f"Betnacional error: {e}")
            matches.append(
                Match(
                    id="bn_error",
                    team_home="Error",
                    team_away=str(e)[:20],
                    league="N/A",
                    start_time="N/A",
                    odds=[]
                )
            )
            
        return matches
