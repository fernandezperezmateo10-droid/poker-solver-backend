from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# --- MAGIA DEL CORS AQUÍ ---
# Esto le dice al servidor: "Acepta peticiones de cualquier página web (Base44)"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ---------------------------

class PokerState(BaseModel):
    hero_hand: List[str]
    board: List[str]
    position: str
    pot_size: float
    stack_size: float

@app.post("/solve")
async def solve_poker(state: PokerState):
    strategy = {
        "check": 0.25,
        "bet_33": 0.50,
        "bet_66": 0.15,
        "fold": 0.10,
        "ev": 4.2
    }
    return {"status": "success", "data": strategy}
