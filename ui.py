# ============================================
# INTERFAZ DE USUARIO
# ============================================

import pygame
import math
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    COLOR_PRIMARY, COLOR_SECONDARY, COLOR_SUCCESS,
    COLOR_ERROR, COLOR_TEXT, CATEGORIES
)

class UI:
    """Gestiona la interfaz de usuario"""
    
    def __init__(self):
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        self.font_tiny = pygame.font.Font(None, 18)

    def draw_background_gradient(self, surface, color1, color2):
        """Dibuja un fondo con gradiente"""
        for y in range(SCREEN_HEIGHT):
            progress = y / SCREEN_HEIGHT
            r = int(color1[0] * (1 - progress) + color2[0] * progress)
            g = int(color1[1] * (1 - progress) + color2[1] * progress)
            b = int(color1[2] * (1 - progress) + color2[2] * progress)
            pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    def draw_animated_background(self, surface, time, color1, color2):
        """Dibuja un fondo animado"""
        self.draw_background_gradient(surface, color1, color2)
        
        # Añadir partículas animadas
        for i in range(5):
            offset = (time * (i + 1) * 20) % SCREEN_HEIGHT
            pygame.draw.circle(surface, (*color1, 50), (SCREEN_WIDTH // (i + 2), offset), 20)

    def draw_button(self, surface, rect, text, color=COLOR_SECONDARY, text_color=COLOR_TEXT, hover=False):
        """Dibuja un botón"""
        if hover:
            pygame.draw.rect(surface, tuple(min(c + 40, 255) for c in color), rect)
        else:
            pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, COLOR_TEXT, rect, 2)
        
        text_surface = self.font_medium.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)

    def draw_text_input(self, surface, rect, text, placeholder="", active=False):
        """Dibuja un campo de entrada de texto"""
        color = COLOR_SECONDARY if active else (100, 100, 100)
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, COLOR_TEXT, rect, 2)
        
        if text:
            text_surface = self.font_small.render(text, True, COLOR_TEXT)
        else:
            text_surface = self.font_small.render(placeholder, True, (150, 150, 150))
        
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)

    def draw_health_bar(self, surface, x, y, width, height, health, max_health):
        """Dibuja una barra de salud"""
        # Fondo
        pygame.draw.rect(surface, COLOR_ERROR, (x, y, width, height))
        
        # Salud actual
        health_width = (health / max_health) * width
        pygame.draw.rect(surface, COLOR_SUCCESS, (x, y, health_width, height))
        
        # Borde
        pygame.draw.rect(surface, COLOR_TEXT, (x, y, width, height), 2)
        
        # Texto
        text = self.font_tiny.render(f'{int(health)}/{int(max_health)}', True, COLOR_TEXT)
        text_rect = text.get_rect(center=(x + width // 2, y + height // 2))
        surface.blit(text, text_rect)

    def draw_score_display(self, surface, x, y, score):
        """Dibuja un marcador de puntos"""
        text = self.font_large.render(f'Puntos: {score}', True, COLOR_SECONDARY)
        surface.blit(text, (x, y))

    def draw_timer(self, surface, x, y, seconds):
        """Dibuja un temporizador"""
        color = COLOR_ERROR if seconds <= 5 else COLOR_TEXT
        text = self.font_large.render(f'{int(seconds)}s', True, color)
        text_rect = text.get_rect(center=(x, y))
        surface.blit(text, text_rect)

    def draw_battle_hud(self, surface, player1_data, player2_data, time_remaining):
        """Dibuja el HUD de batalla"""
        # Información del jugador 1 (izquierda)
        self.draw_health_bar(surface, 20, 20, 250, 30, player1_data['health'], player1_data['max_health'])
        name_text = self.font_small.render(player1_data['username'], True, COLOR_TEXT)
        surface.blit(name_text, (20, 60))
        score_text = self.font_small.render(f'Puntos: {player1_data["score"]}', True, COLOR_SECONDARY)
        surface.blit(score_text, (20, 90))
        
        # Información del jugador 2 (derecha)
        self.draw_health_bar(surface, SCREEN_WIDTH - 270, 20, 250, 30, player2_data['health'], player2_data['max_health'])
        name_text2 = self.font_small.render(player2_data['username'], True, COLOR_TEXT)
        surface.blit(name_text2, (SCREEN_WIDTH - 270, 60))
        score_text2 = self.font_small.render(f'Puntos: {player2_data["score"]}', True, COLOR_SECONDARY)
        surface.blit(score_text2, (SCREEN_WIDTH - 270, 90))
        
        # Temporizador en el centro
        self.draw_timer(surface, SCREEN_WIDTH // 2, 50, time_remaining)

    def draw_question(self, surface, question, question_number, total_questions):
        """Dibuja una pregunta y sus opciones"""
        # Número de pregunta
        question_num_text = self.font_small.render(f'Pregunta {question_number}/{total_questions}', True, COLOR_TEXT)
        surface.blit(question_num_text, (SCREEN_WIDTH // 2 - 100, 150))
        
        # Pregunta
        question_text = self.font_medium.render(question['question'], True, COLOR_TEXT)
        question_rect = question_text.get_rect(center=(SCREEN_WIDTH // 2, 220))
        surface.blit(question_text, question_rect)
        
        # Opciones
        options_y = 320
        for i, (key, option_text) in enumerate(question['options'].items()):
            option_color = COLOR_SUCCESS if i % 2 == 0 else COLOR_SECONDARY
            y_pos = options_y + (i // 2) * 100
            x_pos = 150 if i % 2 == 0 else SCREEN_WIDTH // 2 + 100
            
            rect = pygame.Rect(x_pos, y_pos, 400, 80)
            self.draw_button(surface, rect, f'{key}. {option_text}', option_color)

    def draw_ranking(self, surface, ranking_data):
        """Dibuja el ranking mundial"""
        title = self.font_large.render('🏆 Ranking Mundial', True, COLOR_SECONDARY)
        surface.blit(title, (SCREEN_WIDTH // 2 - 200, 50))
        
        y_pos = 150
        for position, (username, points, level, user_id) in enumerate(ranking_data, 1):
            medal = '🥇' if position == 1 else ('🥈' if position == 2 else ('🥉' if position == 3 else f'{position}.'))
            rank_text = self.font_small.render(
                f'{medal} {username} - {points} pts (Nivel {level})',
                True,
                COLOR_TEXT
            )
            surface.blit(rank_text, (100, y_pos))
            y_pos += 50
