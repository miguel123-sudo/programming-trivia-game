# ============================================
# VIDEOJUEGO DE TRIVIA DE PROGRAMACIÓN
# APLICACIÓN PRINCIPAL
# ============================================

import pygame
import sys
import random
from datetime import datetime, timedelta
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    COLOR_PRIMARY, COLOR_SECONDARY, COLOR_SUCCESS,
    COLOR_ERROR, COLOR_TEXT, COLOR_DARK, CATEGORIES,
    GameState, BATTLE_TIME_LIMIT
)
from database import Database
from ui import UI
from game import Battle, Player, GuestPlayer
from questions import QuestionBank

class GameApp:
    """Aplicación principal del videojuego"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Programming Trivia Game - Educación en Programación')
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = GameState.LOGIN
        self.ui = UI()
        self.db = Database()
        self.current_user = None
        self.animation_time = 0
        self.battle = None
        self.input_active = False
        self.input_text = ""
        self.input_type = "email"  # email, password, username, phone
        self.login_email = ""
        self.login_password = ""
        self.register_username = ""
        self.register_email = ""
        self.register_password = ""
        self.register_phone = ""
        self.selected_category = None
        self.opponent_player = None
        self.buttons = {}
        self.question_start_time = None
        self.show_game_over = False
        self.game_over_message = ""

    def run(self):
        """Loop principal del juego"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

    def handle_events(self):
        """Maneja eventos"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == GameState.BATTLE:
                        self.game_state = GameState.CATEGORY_SELECT
                    elif self.game_state != GameState.LOGIN:
                        self.game_state = GameState.MENU
                        self.current_user = None
                else:
                    self.handle_text_input(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos)

    def handle_text_input(self, event):
        """Maneja entrada de texto"""
        if self.game_state == GameState.LOGIN or self.game_state == GameState.REGISTER:
            if event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.unicode.isprintable():
                self.input_text += event.unicode

    def handle_mouse_click(self, pos):
        """Maneja clics del ratón"""
        for button_name, button_rect in self.buttons.items():
            if button_rect.collidepoint(pos):
                self.on_button_click(button_name)

    def on_button_click(self, button_name):
        """Maneja clics de botones"""
        if self.game_state == GameState.LOGIN:
            if button_name == "login":
                result = self.db.login_user(self.login_email, self.login_password)
                if result['success']:
                    self.current_user = result['user_id']
                    self.game_state = GameState.MENU
                else:
                    self.show_message("Error: " + result['message'])
            elif button_name == "register_button":
                self.game_state = GameState.REGISTER
            elif button_name == "guest":
                self.current_user = None
                self.game_state = GameState.MENU
            elif button_name == "email_input":
                self.input_type = "email"
            elif button_name == "password_input":
                self.input_type = "password"
        
        elif self.game_state == GameState.REGISTER:
            if button_name == "register_confirm":
                if self.register_email and self.register_password:
                    result = self.db.register_user(
                        self.register_username or f"user_{random.randint(1000, 9999)}",
                        self.register_email,
                        self.register_password,
                        self.register_phone
                    )
                    if result['success']:
                        self.game_state = GameState.LOGIN
                        self.show_message("Registro exitoso")
                    else:
                        self.show_message("Error: " + result['message'])
            elif button_name == "back":
                self.game_state = GameState.LOGIN
        
        elif self.game_state == GameState.MENU:
            if button_name == "play":
                self.game_state = GameState.CATEGORY_SELECT
            elif button_name == "progress":
                self.game_state = GameState.PROGRESS
            elif button_name == "ranking":
                self.game_state = GameState.RANKING
            elif button_name == "logout":
                self.current_user = None
                self.game_state = GameState.LOGIN
        
        elif self.game_state == GameState.CATEGORY_SELECT:
            if button_name.startswith("category_"):
                category_id = int(button_name.split("_")[1])
                self.selected_category = category_id
                self.start_battle()
            elif button_name == "back":
                self.game_state = GameState.MENU
        
        elif self.game_state == GameState.BATTLE:
            if button_name in ["A", "B", "C", "D"]:
                self.process_battle_answer(button_name)
        
        elif self.game_state == GameState.RANKING or self.game_state == GameState.PROGRESS:
            if button_name == "back":
                self.game_state = GameState.MENU

    def start_battle(self):
        """Inicia una batalla"""
        if not self.current_user:
            player1_name = f"Invitado_{random.randint(1000, 9999)}"
            player1_id = random.randint(10000, 99999)
        else:
            user = self.db.get_user(self.current_user)
            player1_name = user[1]
            player1_id = user[0]
        
        # Crear oponente IA
        opponent_names = ['Alex', 'Jordan', 'Casey', 'Morgan', 'Riley', 'Taylor']
        player2_name = random.choice(opponent_names)
        player2_id = random.randint(10000, 99999)
        
        self.battle = Battle(player1_id, player1_name, player2_id, player2_name, self.selected_category)
        self.game_state = GameState.BATTLE
        self.question_start_time = datetime.now()

    def process_battle_answer(self, answer):
        """Procesa una respuesta en batalla"""
        if not self.battle:
            return
        
        response_time = (datetime.now() - self.question_start_time).total_seconds()
        result = self.battle.process_answer(answer, response_time)
        
        if not self.battle.battle_active:
            self.show_game_over = True
            self.game_over_message = f"¡{self.battle.winner} ganó la batalla!"
        
        self.question_start_time = datetime.now()

    def update(self):
        """Actualiza el estado del juego"""
        self.animation_time += 1
        
        if self.game_state == GameState.BATTLE and self.battle:
            current_time = (datetime.now() - self.question_start_time).total_seconds()
            if current_time > BATTLE_TIME_LIMIT:
                # Tiempo agotado, siguiente pregunta
                self.battle.current_player_turn = 2 if self.battle.current_player_turn == 1 else 1
                self.question_start_time = datetime.now()

    def show_message(self, message):
        """Muestra un mensaje temporal"""
        print(f"[MENSAJE] {message}")

    def render(self):
        """Renderiza el juego"""
        self.screen.fill(COLOR_DARK)
        
        if self.game_state == GameState.LOGIN:
            self.render_login()
        elif self.game_state == GameState.REGISTER:
            self.render_register()
        elif self.game_state == GameState.MENU:
            self.render_menu()
        elif self.game_state == GameState.CATEGORY_SELECT:
            self.render_category_select()
        elif self.game_state == GameState.BATTLE:
            self.render_battle()
        elif self.game_state == GameState.RANKING:
            self.render_ranking()
        elif self.game_state == GameState.PROGRESS:
            self.render_progress()
        
        pygame.display.flip()

    def render_login(self):
        """Renderiza la pantalla de login"""
        self.ui.draw_animated_background(self.screen, self.animation_time // 10, COLOR_PRIMARY, COLOR_SECONDARY)
        
        # Título
        title = self.ui.font_large.render('Programming Trivia', True, COLOR_TEXT)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - 200, 50))
        
        # Campos de entrada
        email_rect = pygame.Rect(300, 200, 600, 50)
        password_rect = pygame.Rect(300, 300, 600, 50)
        
        self.ui.draw_text_input(self.screen, email_rect, self.login_email, "Email")
        self.ui.draw_text_input(self.screen, password_rect, "*" * len(self.login_password), "Contraseña")
        
        self.buttons['email_input'] = email_rect
        self.buttons['password_input'] = password_rect
        
        # Botones
        login_btn = pygame.Rect(350, 400, 200, 50)
        register_btn = pygame.Rect(650, 400, 200, 50)
        guest_btn = pygame.Rect(475, 500, 250, 50)
        
        self.ui.draw_button(self.screen, login_btn, 'Iniciar Sesión', COLOR_SUCCESS)
        self.ui.draw_button(self.screen, register_btn, 'Registrarse', COLOR_SECONDARY)
        self.ui.draw_button(self.screen, guest_btn, 'Jugar como Invitado', COLOR_TEXT)
        
        self.buttons['login'] = login_btn
        self.buttons['register_button'] = register_btn
        self.buttons['guest'] = guest_btn
        
        # Opciones de login social
        google_btn = pygame.Rect(150, 600, 300, 40)
        facebook_btn = pygame.Rect(550, 600, 300, 40)
        phone_btn = pygame.Rect(950, 600, 150, 40)
        
        self.ui.draw_button(self.screen, google_btn, 'Google', (66, 133, 244))
        self.ui.draw_button(self.screen, facebook_btn, 'Facebook', (59, 89, 152))
        self.ui.draw_button(self.screen, phone_btn, 'Teléfono', (76, 175, 80))

    def render_register(self):
        """Renderiza la pantalla de registro"""
        self.ui.draw_background_gradient(self.screen, COLOR_PRIMARY, COLOR_SECONDARY)
        
        title = self.ui.font_large.render('Registro', True, COLOR_TEXT)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - 100, 50))
        
        # Campos
        username_rect = pygame.Rect(300, 150, 600, 40)
        email_rect = pygame.Rect(300, 220, 600, 40)
        password_rect = pygame.Rect(300, 290, 600, 40)
        phone_rect = pygame.Rect(300, 360, 600, 40)
        
        self.ui.draw_text_input(self.screen, username_rect, self.register_username, "Usuario (opcional)")
        self.ui.draw_text_input(self.screen, email_rect, self.register_email, "Email")
        self.ui.draw_text_input(self.screen, password_rect, "*" * len(self.register_password), "Contraseña")
        self.ui.draw_text_input(self.screen, phone_rect, self.register_phone, "Teléfono (opcional)")
        
        # Botones
        confirm_btn = pygame.Rect(350, 480, 200, 50)
        back_btn = pygame.Rect(650, 480, 200, 50)
        
        self.ui.draw_button(self.screen, confirm_btn, 'Registrarse', COLOR_SUCCESS)
        self.ui.draw_button(self.screen, back_btn, 'Volver', COLOR_ERROR)
        
        self.buttons['register_confirm'] = confirm_btn
        self.buttons['back'] = back_btn

    def render_menu(self):
        """Renderiza el menú principal"""
        self.ui.draw_animated_background(self.screen, self.animation_time // 10, COLOR_PRIMARY, COLOR_SECONDARY)
        
        # Bienvenida
        welcome = self.ui.font_large.render(f'¡Bienvenido!', True, COLOR_TEXT)
        self.screen.blit(welcome, (SCREEN_WIDTH // 2 - 150, 50))
        
        # Botones del menú
        play_btn = pygame.Rect(350, 200, 500, 70)
        progress_btn = pygame.Rect(350, 300, 500, 70)
        ranking_btn = pygame.Rect(350, 400, 500, 70)
        logout_btn = pygame.Rect(350, 500, 500, 70)
        
        self.ui.draw_button(self.screen, play_btn, '🎮 JUGAR')
        self.ui.draw_button(self.screen, progress_btn, '📊 Mi Progreso')
        self.ui.draw_button(self.screen, ranking_btn, '🏆 Ranking Mundial')
        self.ui.draw_button(self.screen, logout_btn, '🚪 Cerrar Sesión')
        
        self.buttons['play'] = play_btn
        self.buttons['progress'] = progress_btn
        self.buttons['ranking'] = ranking_btn
        self.buttons['logout'] = logout_btn

    def render_category_select(self):
        """Renderiza selección de categorías"""
        self.ui.draw_background_gradient(self.screen, COLOR_PRIMARY, COLOR_SECONDARY)
        
        title = self.ui.font_large.render('Selecciona una Categoría', True, COLOR_TEXT)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - 250, 30))
        
        # Mostrar categorías
        y_pos = 120
        for category in CATEGORIES:
            cat_rect = pygame.Rect(150, y_pos, 900, 100)
            self.ui.draw_button(self.screen, cat_rect, f"{category['name']} - {category['description']}", category['color'])
            self.buttons[f"category_{category['id']}"] = cat_rect
            y_pos += 120
        
        # Botón volver
        back_btn = pygame.Rect(450, 700, 300, 50)
        self.ui.draw_button(self.screen, back_btn, 'Volver', COLOR_ERROR)
        self.buttons['back'] = back_btn

    def render_battle(self):
        """Renderiza la pantalla de batalla"""
        if not self.battle:
            self.game_state = GameState.MENU
            return
        
        # Fondo animado
        self.ui.draw_background_gradient(self.screen, (50, 50, 100), (100, 50, 150))
        
        battle_state = self.battle.get_battle_state()
        
        # HUD de batalla
        self.ui.draw_battle_hud(
            self.screen,
            battle_state['player1'],
            battle_state['player2'],
            BATTLE_TIME_LIMIT - (datetime.now() - self.question_start_time).total_seconds()
        )
        
        # Pregunta
        if battle_state['current_question']:
            self.ui.draw_question(
                self.screen,
                battle_state['current_question'],
                battle_state['question_number'],
                battle_state['total_questions']
            )
            
            # Botones de respuesta
            options = battle_state['current_question']['options']
            y_pos = 450
            for i, (key, option_text) in enumerate(options.items()):
                x_pos = 150 if i < 2 else SCREEN_WIDTH // 2 + 100
                y_pos_actual = 450 + (i % 2) * 120
                
                btn_rect = pygame.Rect(x_pos, y_pos_actual, 400, 100)
                self.ui.draw_button(self.screen, btn_rect, f'{key}', COLOR_SUCCESS if i % 2 == 0 else COLOR_SECONDARY)
                self.buttons[key] = btn_rect
        
        # Mostrar game over si aplica
        if self.show_game_over:
            game_over_text = self.ui.font_large.render(self.game_over_message, True, COLOR_SUCCESS)
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 300, 300))
            
            back_btn = pygame.Rect(450, 500, 300, 50)
            self.ui.draw_button(self.screen, back_btn, 'Volver al Menú', COLOR_ERROR)
            self.buttons['back'] = back_btn

    def render_ranking(self):
        """Renderiza el ranking mundial"""
        self.ui.draw_background_gradient(self.screen, COLOR_PRIMARY, COLOR_SECONDARY)
        
        ranking_data = self.db.get_ranking()
        self.ui.draw_ranking(self.screen, ranking_data)
        
        # Botón volver
        back_btn = pygame.Rect(450, 700, 300, 50)
        self.ui.draw_button(self.screen, back_btn, 'Volver', COLOR_ERROR)
        self.buttons['back'] = back_btn

    def render_progress(self):
        """Renderiza el progreso del usuario"""
        self.ui.draw_background_gradient(self.screen, COLOR_PRIMARY, COLOR_SECONDARY)
        
        title = self.ui.font_large.render('Mi Progreso', True, COLOR_TEXT)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - 150, 50))
        
        if self.current_user:
            user = self.db.get_user(self.current_user)
            stats_text = self.ui.font_medium.render(
                f'Puntos Totales: {user[3]} | Nivel: {user[4]}',
                True, COLOR_SECONDARY
            )
            self.screen.blit(stats_text, (200, 200))
        
        # Botón volver
        back_btn = pygame.Rect(450, 700, 300, 50)
        self.ui.draw_button(self.screen, back_btn, 'Volver', COLOR_ERROR)
        self.buttons['back'] = back_btn

if __name__ == "__main__":
    app = GameApp()
    app.run()
