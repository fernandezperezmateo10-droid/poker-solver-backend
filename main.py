from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI() # <--- ESTA ES LA LÍNEA QUE RENDER NO ENCUENTRA

# Definimos qué datos esperamos recibir de Base44
class PokerState(BaseModel):
    hero_hand: List[str]
    board: List[str]
    position: str
    pot_size: float
    stack_size: float

@app.post("/solve")
async def solve_poker(state: PokerState):
    # AQUÍ IRÁ LA LÓGICA DEL SOLVER (CFR Algorithm)
    # Por ahora, simulamos una respuesta lógica:
    strategy = {
        "check": 0.25,
        "bet_33": 0.50,
        "bet_66": 0.15,
        "fold": 0.10,
        "ev": 4.2
    }
    return {"status": "success", "data": strategy}
