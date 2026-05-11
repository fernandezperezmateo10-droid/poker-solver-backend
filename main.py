import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import google.generativeai as genai

# Configuración de la IA (Gemini)
# Render inyectará la clave de forma segura sin tener que escribirla en el código
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

app = FastAPI()

# Permisos CORS para Base44
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# La nueva estructura que envía Base44
class PokerState(BaseModel):
    table_format: str
    hero_position: str
    villain_position: str
    hero_hand: List[str]
    board: List[str]
    pot_size: float
    stack_size: float

@app.post("/solve")
async def solve_poker(state: PokerState):
    # 1. EL SOLVER MATEMÁTICO (Mock GTO numbers por ahora)
    strategy = {
        "check": 0.25,
        "bet_33": 0.50,
        "bet_66": 0.15,
        "fold": 0.10,
        "ev": 4.2
    }
    
    # 2. EL COACH DE IA (Gemini)
    coach_explanation = "La IA no está configurada aún."
    
    if api_key:
        try:
            # Elegimos el modelo rápido de Gemini
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Le damos contexto de teoría de póker a la IA
            prompt = f"""
            Actúa como un coach profesional de póker GTO. Analiza esta situación:
            Mesa: {state.table_format}
            Hero está en: {state.hero_position} con las cartas {state.hero_hand}
            Villano está en: {state.villain_position}
            Cartas comunitarias (Board): {state.board}
            Bote: {state.pot_size} BB. Stack efectivo: {state.stack_size} BB.
            
            El solver sugiere esta estrategia: Apostar pequeño 50%, Pasar 25%, Apostar grande 15%.
            
            En un solo párrafo corto (máximo 3 frases), explícale al jugador por qué esta estrategia 
            tiene sentido teórico basándote en la ventaja de rango o de nuts en esta textura de mesa. 
            Sé directo y técnico.
            """
            
            response = model.generate_content(prompt)
            coach_explanation = response.text
        except Exception as e:
            coach_explanation = "Error al consultar al Coach IA: Vuelve a intentarlo."

    # 3. EMPAQUETAR Y ENVIAR A BASE44
    return {
        "status": "success", 
        "data": strategy,
        "coach_explanation": coach_explanation
    }
