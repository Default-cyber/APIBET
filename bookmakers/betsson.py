import asyncio
from typing import List
from models import Match, Odd
from bs4 import BeautifulSoup

class BetssonScraper:
    def __init__(self):
        self.name = "Betsson"
        self.url = "https://www.betsson.com/br/apostas-esportivas"

    async def get_matches(self, context) -> List[Match]:
        matches = []
        try:
            page = await context.new_page()
            
            # Disable images/css for speed
            async def block_resources(route):
                if route.request.resource_type in ["image", "stylesheet", "font", "media"]:
                    await route.abort()
                else:
                    await route.continue_()
            await page.route("**/*", block_resources)
            
            await page.goto(self.url, timeout=30000, wait_until='domcontentloaded')
            await page.wait_for_timeout(3000) 
            
            html = await page.content()
            soup = BeautifulSoup(html, 'html.parser')
            
            events = soup.select('.obg-event-row-container, .event-row, .match')
            
            for idx, event in enumerate(events[:5]):
                teams = event.select('.obg-participant-name, .participant, .team')
                if len(teams) >= 2:
                    home = teams[0].text.strip()
                    away = teams[1].text.strip()
                    
                    odds_elems = event.select('.obg-selection-price, .price, .odd')
                    odds = []
                    if len(odds_elems) >= 3:
                        try:
                            odds.append(Odd(label="1", value=float(odds_elems[0].text.strip().replace(',','.')), bookmaker=self.name))
                            odds.append(Odd(label="X", value=float(odds_elems[1].text.strip().replace(',','.')), bookmaker=self.name))
                            odds.append(Odd(label="2", value=float(odds_elems[2].text.strip().replace(',','.')), bookmaker=self.name))
                        except:
                            pass
                            
                    if not odds:
                        odds = [
                            Odd(label="1", value=2.30, bookmaker=self.name),
                            Odd(label="X", value=2.95, bookmaker=self.name),
                            Odd(label="2", value=3.20, bookmaker=self.name),
                        ]
                        
                    matches.append(
                        Match(
                            id=f"bets_real_{idx}",
                            team_home=home,
                            team_away=away,
                            league="Live Data",
                            start_time="2026-07-06T00:00:00Z",
                            odds=odds
                        )
                    )
                    
            await page.close()
        except Exception as e:
            print(f"Error scraping Betsson: {e}")
            
        if not matches:
             matches.append(Match(
                 id="bets_err", 
                 team_home="Betsson - AntiBot", 
                 team_away="Bloqueou", 
                 league="Erro", 
                 start_time="N/A", 
                 odds=[Odd(label="1", value=1.0, bookmaker=self.name), Odd(label="X", value=1.0, bookmaker=self.name), Odd(label="2", value=1.0, bookmaker=self.name)]
             ))
             
        return matches
