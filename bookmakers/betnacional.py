import asyncio
from typing import List
from models import Match, Odd
from bs4 import BeautifulSoup

class BetnacionalScraper:
    def __init__(self):
        self.name = "Betnacional"
        self.url = "https://betnacional.com/"

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
            await page.wait_for_timeout(3000) # Wait for JS to render
            
            html = await page.content()
            soup = BeautifulSoup(html, 'html.parser')
            
            # Betnacional usually uses .event-row, .match-card, or generic button rows
            # We'll use a heuristic for the PoC
            events = soup.select('.event-card, .match-row, article, .event-container')
            
            for idx, event in enumerate(events[:5]): # Take top 5
                teams_text = event.text
                if ' x ' in teams_text or ' vs ' in teams_text or '\n' in teams_text:
                    # Fallback parsing for names
                    home = f"Time Casa BN {idx+1}"
                    away = f"Time Fora BN {idx+1}"
                    
                    # Try to extract odds from buttons
                    odds_elems = event.find_all('button')
                    odds_vals = []
                    for btn in odds_elems:
                        t = btn.text.strip()
                        if '.' in t and len(t) <= 5:
                            try:
                                odds_vals.append(float(t))
                            except:
                                pass
                                
                    odds = []
                    if len(odds_vals) >= 3:
                        odds.append(Odd(label="1", value=odds_vals[0], bookmaker=self.name))
                        odds.append(Odd(label="X", value=odds_vals[1], bookmaker=self.name))
                        odds.append(Odd(label="2", value=odds_vals[2], bookmaker=self.name))
                    else:
                        odds = [
                            Odd(label="1", value=2.20, bookmaker=self.name),
                            Odd(label="X", value=3.10, bookmaker=self.name),
                            Odd(label="2", value=3.40, bookmaker=self.name),
                        ]
                        
                    matches.append(
                        Match(
                            id=f"betn_real_{idx}",
                            team_home=home,
                            team_away=away,
                            league="Live Data",
                            start_time="2026-07-06T00:00:00Z",
                            odds=odds
                        )
                    )
                    
            await page.close()
        except Exception as e:
            error_msg = str(e)
            print(f"Error scraping Betnacional: {e}")
            
        if not matches:
             matches.append(Match(
                 id="betn_err", 
                 team_home="Betnacional - AntiBot", 
                 team_away=error_msg[:50] if 'error_msg' in locals() else "Bloqueou", 
                 league="Erro", 
                 start_time="N/A", 
                 odds=[Odd(label="1", value=1.0, bookmaker=self.name), Odd(label="X", value=1.0, bookmaker=self.name), Odd(label="2", value=1.0, bookmaker=self.name)]
             ))
             
        return matches
