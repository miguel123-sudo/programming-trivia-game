# ============================================
# GESTIÓN DE BASE DE DATOS
# ============================================

import sqlite3
import os
from datetime import datetime
from config import DB_PATH
import hashlib

class Database:
    def __init__(self):
        self.db_path = DB_PATH
        self.init_database()

    def get_connection(self):
        """Obtiene conexión a la base de datos"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        return sqlite3.connect(self.db_path)

    def init_database(self):
        """Inicializa la base de datos con tablas"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                phone TEXT,
                auth_method TEXT DEFAULT 'email',
                profile_picture TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                total_points INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                is_active BOOLEAN DEFAULT 1
            )
        ''')

        # Tabla de estadísticas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                category_id INTEGER,
                battles_played INTEGER DEFAULT 0,
                battles_won INTEGER DEFAULT 0,
                questions_answered INTEGER DEFAULT 0,
                correct_answers INTEGER DEFAULT 0,
                total_score INTEGER DEFAULT 0,
                last_played TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        # Tabla de partidas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS battles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player1_id INTEGER NOT NULL,
                player2_id INTEGER NOT NULL,
                category_id INTEGER,
                winner_id INTEGER,
                player1_score INTEGER DEFAULT 0,
                player2_score INTEGER DEFAULT 0,
                duration INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (player1_id) REFERENCES users(id),
                FOREIGN KEY (player2_id) REFERENCES users(id)
            )
        ''')

        # Tabla de preguntas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER NOT NULL,
                question TEXT NOT NULL,
                option_a TEXT NOT NULL,
                option_b TEXT NOT NULL,
                option_c TEXT NOT NULL,
                option_d TEXT NOT NULL,
                correct_answer TEXT NOT NULL,
                difficulty INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()
        self.insert_default_questions()

    def hash_password(self, password):
        """Hashea la contraseña"""
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, email, password, phone=None, auth_method='email'):
        """Registra un nuevo usuario"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            hashed_password = self.hash_password(password)
            
            cursor.execute('''
                INSERT INTO users (username, email, password, phone, auth_method)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, email, hashed_password, phone, auth_method))
            
            user_id = cursor.lastrowid
            
            # Crear estadísticas iniciales
            cursor.execute('''
                INSERT INTO stats (user_id, total_score)
                VALUES (?, 0)
            ''', (user_id,))
            
            conn.commit()
            conn.close()
            return {'success': True, 'user_id': user_id, 'message': 'Usuario registrado exitosamente'}
        except sqlite3.IntegrityError as e:
            return {'success': False, 'message': 'El usuario o email ya existe'}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    def login_user(self, email, password):
        """Valida credenciales de usuario"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            hashed_password = self.hash_password(password)
            
            cursor.execute('''
                SELECT id, username, email FROM users 
                WHERE email = ? AND password = ? AND is_active = 1
            ''', (email, hashed_password))
            
            user = cursor.fetchone()
            
            if user:
                # Actualizar último login
                cursor.execute('''
                    UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
                ''', (user[0],))
                conn.commit()
                conn.close()
                return {'success': True, 'user_id': user[0], 'username': user[1], 'email': user[2]}
            else:
                conn.close()
                return {'success': False, 'message': 'Email o contraseña incorrectos'}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    def get_user(self, user_id):
        """Obtiene información del usuario"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, email, total_points, level FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user

    def get_ranking(self, limit=10):
        """Obtiene el ranking mundial"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT username, total_points, level, id FROM users 
            ORDER BY total_points DESC LIMIT ?
        ''', (limit,))
        ranking = cursor.fetchall()
        conn.close()
        return ranking

    def insert_default_questions(self):
        """Inserta preguntas por defecto"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Verificar si ya existen preguntas
        cursor.execute('SELECT COUNT(*) FROM questions')
        if cursor.fetchone()[0] > 0:
            conn.close()
            return

        questions = [
            # Fundamentos (categoría 1)
            (1, '¿Qué es una variable en programación?', 'Un contenedor de datos', 'Una función', 'Un tipo de error', 'Un bucle', 'A', 1),
            (1, '¿Cuál es el propósito principal de un programa?', 'Procesar datos y producir resultados', 'Confundir al usuario', 'Ocupar espacio en memoria', 'Hacer ruido', 'A', 1),
            (1, '¿Qué es un algoritmo?', 'Una serie de pasos para resolver un problema', 'Un tipo de dato', 'Un error de compilación', 'Una red de computadoras', 'A', 1),
            (1, '¿Cuál es la diferencia entre un compilador e intérprete?', 'El compilador traduce todo antes, el intérprete línea por línea', 'No hay diferencia', 'Los intérpretes son más rápidos', 'Los compiladores son para Python', 'A', 2),
            (1, '¿Qué es debugging?', 'El proceso de encontrar y corregir errores', 'Crear nuevos programas', 'Eliminar archivos', 'Hacer backup', 'A', 1),
            
            # Variables y Tipos (categoría 2)
            (2, '¿Cuál es el tipo de dato para texto en Python?', 'string', 'text', 'str', 'char', 'A', 1),
            (2, '¿Qué es un entero en programación?', 'Un número sin decimales', 'Un número con decimales', 'Una letra', 'Un símbolo', 'A', 1),
            (2, '¿Cuál es la diferencia entre = y ==?', '= asigna, == compara', 'No hay diferencia', 'Son lo mismo en Python', 'Los dos comparan', 'A', 2),
            (2, '¿Qué tipo de dato es True o False?', 'boolean', 'integer', 'string', 'float', 'A', 1),
            (2, '¿Cuál es el rango de un número flotante?', 'Números con decimales', 'Números enteros', 'Solo negativos', 'Solo positivos', 'A', 1),
            
            # Funciones (categoría 3)
            (3, '¿Qué es una función?', 'Un bloque de código reutilizable', 'Un variable', 'Un tipo de error', 'Un bucle', 'A', 1),
            (3, '¿Cuál es el beneficio de usar funciones?', 'Reutilizar código y mejorar legibilidad', 'Lentificar el programa', 'Crear errores', 'Confundir', 'A', 1),
            (3, '¿Qué es un parámetro?', 'Una entrada a una función', 'Una salida de una función', 'Un tipo de error', 'Una variable global', 'A', 1),
            (3, '¿Qué es el retorno de una función?', 'El valor que devuelve', 'El inicio de la función', 'El nombre de la función', 'Los parámetros', 'A', 2),
            (3, '¿Cuántas veces puede retornar una función?', 'Una vez (en Python)', 'Infinitas', 'Dos veces', 'Nunca', 'A', 2),
            
            # POO (categoría 4)
            (4, '¿Qué es una clase?', 'Un molde para crear objetos', 'Un tipo de variable', 'Una función', 'Un error', 'A', 1),
            (4, '¿Qué es un objeto?', 'Una instancia de una clase', 'Un tipo de dato', 'Una variable', 'Una función', 'A', 1),
            (4, '¿Cuál es el método especial para inicializar un objeto en Python?', '__init__', 'init', 'start', 'begin', 'A', 2),
            (4, '¿Qué es la herencia en POO?', 'La capacidad de una clase heredar de otra', 'Copiar código', 'Crear variables', 'Hacer funciones', 'A', 2),
            (4, '¿Qué es el polimorfismo?', 'Múltiples formas del mismo método', 'Crear clases', 'Variables globales', 'Funciones recursivas', 'A', 3),
            
            # Algoritmos (categoría 5)
            (5, '¿Qué es un bucle while?', 'Repite código mientras una condición sea verdadera', 'Declara variables', 'Importa librerías', 'Define funciones', 'A', 1),
            (5, '¿Cuál es la complejidad de búsqueda binaria?', 'O(log n)', 'O(n)', 'O(n²)', 'O(1)', 'A', 3),
            (5, '¿Qué es la recursión?', 'Cuando una función se llama a sí misma', 'Un tipo de variable', 'Un error de compilación', 'Un bucle infinito', 'A', 2),
            (5, '¿Cuál es el mejor algoritmo de ordenamiento?', 'Depende del contexto', 'Bubble Sort', 'Insertion Sort', 'Selection Sort', 'A', 3),
            (5, '¿Qué es Big O?', 'Notación para analizar complejidad', 'Un operador', 'Una variable', 'Un tipo de dato', 'A', 3),
        ]

        cursor.executemany('''
            INSERT INTO questions (category_id, question, option_a, option_b, option_c, option_d, correct_answer, difficulty)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', questions)

        conn.commit()
        conn.close()

    def get_questions(self, category_id, limit=10):
        """Obtiene preguntas aleatorias de una categoría"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM questions WHERE category_id = ? ORDER BY RANDOM() LIMIT ?
        ''', (category_id, limit))
        questions = cursor.fetchall()
        conn.close()
        return questions

    def save_battle(self, player1_id, player2_id, category_id, winner_id, player1_score, player2_score, duration):
        """Guarda una batalla"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO battles (player1_id, player2_id, category_id, winner_id, player1_score, player2_score, duration)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (player1_id, player2_id, category_id, winner_id, player1_score, player2_score, duration))
            
            # Actualizar puntos totales
            cursor.execute('''
                UPDATE users SET total_points = total_points + ? WHERE id = ?
            ''', (player1_score + player2_score, player1_id))
            
            cursor.execute('''
                UPDATE users SET total_points = total_points + ? WHERE id = ?
            ''', (player2_score, player2_id))
            
            conn.commit()
            conn.close()
            return {'success': True, 'message': 'Batalla guardada'}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    def get_user_stats(self, user_id):
        """Obtiene estadísticas del usuario"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM stats WHERE user_id = ?', (user_id,))
        stats = cursor.fetchone()
        conn.close()
        return stats
