import os

bookmakers = [
    "Betnacional", "Sportingbet", "Novibet", "Betsson", "Galera.bet", 
    "Casa de Apostas", "BetSul", "BetFast", "VBet", "7Games", 
    "Aposta Ganha", "Brazino777", "Rei do Pitaco", "BrasilBet", 
    "Luva.bet", "F12.bet", "SportyBet", "Reals", "HiperBet", 
    "SeuBet", "H2.bet", "Caesars", "Big", "Apostar", "BetBoom"
]

template = """from typing import List
from models import Match, Odd
from bookmakers.base import BaseBookmaker
import asyncio

class {class_name}Scraper(BaseBookmaker):
    def __init__(self):
        self.name = "{name}"

    async def get_matches(self, sport: str = "soccer") -> List[Match]:
        await asyncio.sleep(0.5) # Simula o tempo de rede
        
        matches = [
            Match(
                id="{id_prefix}_1",
                team_home="Flamengo",
                team_away="Vasco",
                league="Brasileirão Serie A",
                start_time="2026-07-05T16:00:00Z",
                odds=[
                    Odd(label="1", value=1.85, bookmaker=self.name),
                    Odd(label="X", value=3.20, bookmaker=self.name),
                    Odd(label="2", value=4.10, bookmaker=self.name),
                ]
            )
        ]
        return matches
"""

imports = []
registrations = []

for bm in bookmakers:
    # Format the name for class and file
    safe_name = bm.replace(".", "").replace(" ", "").replace("7", "Sete") # remove dots and spaces, handle numbers for class names if needed
    class_name = safe_name
    file_name = bm.lower().replace(".", "").replace(" ", "")
    id_prefix = file_name[:4]
    
    # generate file
    file_path = os.path.join("bookmakers", f"{file_name}.py")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(template.format(class_name=class_name, name=bm, id_prefix=id_prefix))
    
    # For main.py
    imports.append(f"from bookmakers.{file_name} import {class_name}Scraper")
    registrations.append(f"    {class_name}Scraper(),")

main_content = f"""from fastapi import FastAPI
from typing import List
import asyncio

from models import Match
{chr(10).join(imports)}

app = FastAPI(
    title="Betting Odds Aggregator API",
    description="API que agrega odds de diferentes casas de apostas",
    version="1.0.0"
)

# Registramos os scrapers das casas de apostas suportadas
bookmakers = [
{chr(10).join(registrations)}
]

@app.get("/")
def read_root():
    return {{"message": "Bem-vindo à API de Casas de Apostas"}}

@app.get("/jogos", response_model=List[Match])
async def get_all_matches():
    \"\"\"
    Busca os jogos em todas as casas de apostas registradas de forma simultânea.
    \"\"\"
    tasks = [bookmaker.get_matches() for bookmaker in bookmakers]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    all_matches = []
    for result in results:
        if isinstance(result, list):
            all_matches.extend(result)
        else:
            print(f"Erro ao buscar dados de uma casa de aposta: {{result}}")
            
    return all_matches
"""

with open("main.py", "w", encoding="utf-8") as f:
    f.write(main_content)

print("Gerados todos os mocks e main.py atualizado!")
