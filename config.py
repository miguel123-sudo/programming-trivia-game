# ============================================
# CONFIGURACIÓN DEL VIDEOJUEGO
# ============================================

import os
from enum import Enum

# Dimensiones de pantalla
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Colores
COLOR_PRIMARY = (26, 35, 126)      # Azul oscuro
COLOR_SECONDARY = (255, 87, 34)    # Naranja
COLOR_SUCCESS = (76, 175, 80)      # Verde
COLOR_ERROR = (244, 67, 54)        # Rojo
COLOR_WARNING = (255, 193, 7)      # Amarillo
COLOR_TEXT = (255, 255, 255)       # Blanco
COLOR_DARK = (33, 33, 33)          # Gris oscuro

# Rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data', 'game.db')
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

# Categorías de preguntas
CATEGORIES = [
    {
        'id': 1,
        'name': 'Fundamentos',
        'description': 'Conceptos básicos de programación',
        'color': (66, 165, 245)
    },
    {
        'id': 2,
        'name': 'Variables y Tipos',
        'description': 'Tipos de datos y variables',
        'color': (102, 187, 106)
    },
    {
        'id': 3,
        'name': 'Funciones',
        'description': 'Funciones y métodos',
        'color': (255, 167, 38)
    },
    {
        'id': 4,
        'name': 'POO',
        'description': 'Programación Orientada a Objetos',
        'color': (171, 71, 188)
    },
    {
        'id': 5,
        'name': 'Algoritmos',
        'description': 'Algoritmos y estructuras de datos',
        'color': (229, 57, 53)
    }
]

# Configuración de batalla
BAT_LE_TIME_LIMIT = 15  # Segundos por pregunta
PLAYER_MAX_HEALTH = 100
Damage_ON_CORRECT = 15   # Daño al responder correctamente
Damage_ON_INCORRECT = 0  # Daño al responder incorrectamente
TIME_BONUS = 5           # Bonus de puntos por rapidez

# Configuración de sesión
SESSION_TIMEOUT = 3600  # 1 hora en segundos

class GameState(Enum):
    """Estados posibles del juego"""
    LOGIN = "login"
    REGISTER = "register"
    MENU = "menu"
    PROFILE = "profile"
    CATEGORY_SELECT = "category_select"
    BATTLE = "battle"
    BATTLE_END = "battle_end"
    PROGRESS = "progress"
    RANKING = "ranking"
    QUIT = "quit"
