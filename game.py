# ============================================
# LÓGICA DEL JUEGO
# ============================================

import random
from datetime import datetime
from config import (
    BATTLE_TIME_LIMIT, PLAYER_MAX_HEALTH, 
    DAMAGE_ON_CORRECT, TIME_BONUS
)
from questions import QuestionBank

class Player:
    """Representa a un jugador en batalla"""
    def __init__(self, user_id, username, health=PLAYER_MAX_HEALTH):
        self.user_id = user_id
        self.username = username
        self.health = health
        self.max_health = health
        self.score = 0
        self.correct_answers = 0
        self.total_answers = 0
        self.response_time = 0

    def take_damage(self, damage):
        """Recibe daño"""
        self.health = max(0, self.health - damage)

    def add_score(self, points):
        """Añade puntos"""
        self.score += points

    def is_alive(self):
        """Verifica si el jugador sigue vivo"""
        return self.health > 0

    def get_health_percentage(self):
        """Obtiene el porcentaje de salud"""
        return (self.health / self.max_health) * 100

    def to_dict(self):
        """Convierte a diccionario"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'health': self.health,
            'max_health': self.max_health,
            'score': self.score,
            'correct_answers': self.correct_answers,
            'total_answers': self.total_answers,
            'accuracy': (self.correct_answers / self.total_answers * 100) if self.total_answers > 0 else 0
        }

class Battle:
    """Gestiona una batalla entre dos jugadores"""
    def __init__(self, player1_id, player1_name, player2_id, player2_name, category_id):
        self.player1 = Player(player1_id, player1_name)
        self.player2 = Player(player2_id, player2_name)
        self.category_id = category_id
        self.current_question_index = 0
        self.questions = QuestionBank.get_questions(category_id)
        self.battle_start_time = datetime.now()
        self.current_player_turn = 1  # Jugador 1 comienza
        self.question_start_time = None
        self.battle_active = True
        self.winner = None

    def get_current_question(self):
        """Obtiene la pregunta actual"""
        if self.current_question_index < len(self.questions):
            return self.questions[self.current_question_index]
        return None

    def process_answer(self, answer, response_time):
        """Procesa una respuesta"""
        current_question = self.get_current_question()
        if not current_question:
            return {'correct': False, 'message': 'No hay más preguntas'}

        current_player = self.player1 if self.current_player_turn == 1 else self.player2
        opponent = self.player2 if self.current_player_turn == 1 else self.player1

        is_correct = answer == current_question['answer']
        current_player.total_answers += 1

        if is_correct:
            current_player.correct_answers += 1
            # Calcular puntos basados en velocidad
            points = max(10, BATTLE_TIME_LIMIT - int(response_time))
            current_player.add_score(points)
            # Infligir daño al oponente
            opponent.take_damage(DAMAGE_ON_CORRECT)
            message = f'¡Correcto! +{points} puntos. {opponent.username} recibe {DAMAGE_ON_CORRECT} de daño'
        else:
            message = f'Incorrecto. La respuesta era: {current_question["answer"]}'

        # Cambiar turno
        self.current_player_turn = 2 if self.current_player_turn == 1 else 1
        self.current_question_index += 1

        # Verificar si la batalla terminó
        self.check_battle_end()

        return {
            'correct': is_correct,
            'message': message,
            'points': points if is_correct else 0,
            'battle_active': self.battle_active,
            'winner': self.winner
        }

    def check_battle_end(self):
        """Verifica si la batalla ha terminado"""
        if not self.player1.is_alive() or not self.player2.is_alive():
            self.battle_active = False
            if self.player1.health > self.player2.health:
                self.winner = self.player1.username
            else:
                self.winner = self.player2.username
        elif self.current_question_index >= len(self.questions):
            self.battle_active = False
            if self.player1.score > self.player2.score:
                self.winner = self.player1.username
            else:
                self.winner = self.player2.username

    def get_battle_state(self):
        """Obtiene el estado actual de la batalla"""
        return {
            'player1': self.player1.to_dict(),
            'player2': self.player2.to_dict(),
            'current_question': self.get_current_question(),
            'current_player_turn': self.current_player_turn,
            'question_number': self.current_question_index + 1,
            'total_questions': len(self.questions),
            'battle_active': self.battle_active,
            'winner': self.winner
        }

    def get_duration(self):
        """Obtiene la duración de la batalla"""
        return int((datetime.now() - self.battle_start_time).total_seconds())

class GuestPlayer:
    """Representa un jugador invitado sin cuenta"""
    def __init__(self, session_id):
        self.user_id = None
        self.session_id = session_id
        self.username = f'Invitado_{random.randint(1000, 9999)}'
        self.score = 0
        self.battles_played = 0
