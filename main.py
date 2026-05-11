import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import google.generativeai as genai

api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Estructura del estado del juego
class PokerState(BaseModel):
    table_format: str
    hero_position: str
    villain_positions: List[str] # <--- Ahora es una lista de oponentes
    hero_hand: List[str]
    board: List[str]
    pot_size: float
    stack_size: float

# NUEVA ESTRUCTURA: Para cuando el usuario hace una pregunta extra
class ChatRequest(BaseModel):
    question: str
    game_context: PokerState

@app.post("/solve")
async def solve_poker(state: PokerState):
    # Dentro de la función solve_poker o chat:
    prompt = f"""
    Eres un coach experto. Analiza esta mano MULTI-WAY:
    Mesa de {state.table_format}.
    Hero ({state.hero_position}) tiene {state.hero_hand}.
    Se enfrenta a {len(state.villain_positions)} villanos en las posiciones: {', '.join(state.villain_positions)}.
    Tablero: {state.board}.
    
    Explica brevemente la dificultad de jugar este bote contra múltiples rangos y qué precauciones debe tomar Hero.
    """
    # Solver Matemático (Mock)
    strategy = {
        "check": 0.25,
        "bet_33": 0.50,
        "bet_66": 0.15,
        "fold": 0.10,
        "ev": 4.2
    }
    
    coach_explanation = "La IA no está configurada aún."
    
    if api_key:
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"Actúa como coach GTO. Mesa: {state.board}, Hero: {state.hero_hand} en {state.hero_position}. Explica brevemente por qué apostar tiene sentido aquí."
            response = model.generate_content(prompt)
            coach_explanation = response.text
        except Exception as e:
            coach_explanation = "Error al consultar al Coach IA."

    return {"status": "success", "data": strategy, "coach_explanation": coach_explanation}

# NUEVO ENDPOINT: Exclusivo para el chat interactivo
@app.post("/chat")
async def ask_coach(request: ChatRequest):
    answer = "Error de IA"
    if api_key:
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            # Le pasamos a la IA la pregunta Y el contexto de la mesa para que no se pierda
            prompt = f"""
            Eres un coach de póker GTO. El usuario te hace una pregunta sobre esta mano actual:
            Mesa: {request.game_context.board}
            Hero: {request.game_context.hero_hand} en {request.game_context.hero_position}
            Villano: {request.game_context.villain_position}
            Bote: {request.game_context.pot_size} BB. Stack: {request.game_context.stack_size} BB.
            
            Pregunta del usuario: "{request.question}"
            
            Responde de forma clara, directa y basándote en teoría de póker.
            """
            response = model.generate_content(prompt)
            answer = response.text
        except Exception as e:
            answer = "Lo siento, hubo un problema al procesar tu pregunta."
            
    return {"status": "success", "answer": answer}
