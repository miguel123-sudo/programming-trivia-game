# ============================================
# GENERADOR DE PREGUNTAS
# ============================================

class QuestionBank:
    """Base de datos de preguntas en memoria"""
    
    QUESTIONS = {
        1: [  # Fundamentos
            {
                'question': '¿Qué es una variable en programación?',
                'options': {'A': 'Un contenedor de datos', 'B': 'Una función', 'C': 'Un tipo de error', 'D': 'Un bucle'},
                'answer': 'A',
                'difficulty': 1
            },
            {
                'question': '¿Cuál es el propósito principal de un programa?',
                'options': {'A': 'Procesar datos y producir resultados', 'B': 'Confundir al usuario', 'C': 'Ocupar espacio en memoria', 'D': 'Hacer ruido'},
                'answer': 'A',
                'difficulty': 1
            },
            {
                'question': '¿Qué es un algoritmo?',
                'options': {'A': 'Una serie de pasos para resolver un problema', 'B': 'Un tipo de dato', 'C': 'Un error de compilación', 'D': 'Una red de computadoras'},
                'answer': 'A',
                'difficulty': 1
            },
            {
                'question': '¿Cuál es la diferencia entre un compilador e intérprete?',
                'options': {'A': 'El compilador traduce todo antes, el intérprete línea por línea', 'B': 'No hay diferencia', 'C': 'Los intérpretes son más rápidos', 'D': 'Los compiladores son para Python'},
                'answer': 'A',
                'difficulty': 2
            },
            {
                'question': '¿Qué es debugging?',
                'options': {'A': 'El proceso de encontrar y corregir errores', 'B': 'Crear nuevos programas', 'C': 'Eliminar archivos', 'D': 'Hacer backup'},
                'answer': 'A',
                'difficulty': 1
            },
        ],
        2: [  # Variables y Tipos
            {
                'question': '¿Cuál es el tipo de dato para texto en Python?',
                'options': {'A': 'string', 'B': 'text', 'C': 'str', 'D': 'char'},
                'answer': 'A',
                'difficulty': 1
            },
            {
                'question': '¿Qué es un entero en programación?',
                'options': {'A': 'Un número sin decimales', 'B': 'Un número con decimales', 'C': 'Una letra', 'D': 'Un símbolo'},
                'answer': 'A',
                'difficulty': 1
            },
            {
                'question': '¿Cuál es la diferencia entre = y ==?',
                'options': {'A': '= asigna, == compara', 'B': 'No hay diferencia', 'C': 'Son lo mismo en Python', 'D': 'Los dos comparan'},
                'answer': 'A',
                'difficulty': 2
            },
            {
                'question': '¿Qué tipo de dato es True o False?',
                'options': {'A': 'boolean', 'B': 'integer', 'C': 'string', 'D': 'float'},
                'answer': 'A',
                'difficulty': 1
            },
            {
                'question': '¿Cuál es el rango de un número flotante?',
                'options': {'A': 'Números con decimales', 'B': 'Números enteros', 'C': 'Solo negativos', 'D': 'Solo positivos'},
                'answer': 'A',
                'difficulty': 1
            },
        ],
        3: [  # Funciones
            {
                'question': '¿Qué es una función?',
                'options': {'A': 'Un bloque de código reutilizable', 'B': 'Una variable', 'C': 'Un tipo de error', 'D': 'Un bucle'},
                'answer': 'A',
                'difficulty': 1
            },
            {
                'question': '¿Cuál es el beneficio de usar funciones?',
                'options': {'A': 'Reutilizar código y mejorar legibilidad', 'B': 'Lentificar el programa', 'C': 'Crear errores', 'D': 'Confundir'},
                'answer': 'A',
                'difficulty': 1
            },
            {
                'question': '¿Qué es un parámetro?',
                'options': {'A': 'Una entrada a una función', 'B': 'Una salida de una función', 'C': 'Un tipo de error', 'D': 'Una variable global'},
                'answer': 'A',
                'difficulty': 1
            },
            {
                'question': '¿Qué es el retorno de una función?',
                'options': {'A': 'El valor que devuelve', 'B': 'El inicio de la función', 'C': 'El nombre de la función', 'D': 'Los parámetros'},
                'answer': 'A',
                'difficulty': 2
            },
            {
                'question': '¿Cuántas veces puede retornar una función?',
                'options': {'A': 'Una vez (en Python)', 'B': 'Infinitas', 'C': 'Dos veces', 'D': 'Nunca'},
                'answer': 'A',
                'difficulty': 2
            },
        ],
        4: [  # POO
            {
                'question': '¿Qué es una clase?',
                'options': {'A': 'Un molde para crear objetos', 'B': 'Un tipo de variable', 'C': 'Una función', 'D': 'Un error'},
                'answer': 'A',
                'difficulty': 1
            },
            {
                'question': '¿Qué es un objeto?',
                'options': {'A': 'Una instancia de una clase', 'B': 'Un tipo de dato', 'C': 'Una variable', 'D': 'Una función'},
                'answer': 'A',
                'difficulty': 1
            },
            {
                'question': '¿Cuál es el método especial para inicializar un objeto en Python?',
                'options': {'A': '__init__', 'B': 'init', 'C': 'start', 'D': 'begin'},
                'answer': 'A',
                'difficulty': 2
            },
            {
                'question': '¿Qué es la herencia en POO?',
                'options': {'A': 'La capacidad de una clase heredar de otra', 'B': 'Copiar código', 'C': 'Crear variables', 'D': 'Hacer funciones'},
                'answer': 'A',
                'difficulty': 2
            },
            {
                'question': '¿Qué es el polimorfismo?',
                'options': {'A': 'Múltiples formas del mismo método', 'B': 'Crear clases', 'C': 'Variables globales', 'D': 'Funciones recursivas'},
                'answer': 'A',
                'difficulty': 3
            },
        ],
        5: [  # Algoritmos
            {
                'question': '¿Qué es un bucle while?',
                'options': {'A': 'Repite código mientras una condición sea verdadera', 'B': 'Declara variables', 'C': 'Importa librerías', 'D': 'Define funciones'},
                'answer': 'A',
                'difficulty': 1
            },
            {
                'question': '¿Cuál es la complejidad de búsqueda binaria?',
                'options': {'A': 'O(log n)', 'B': 'O(n)', 'C': 'O(n²)', 'D': 'O(1)'},
                'answer': 'A',
                'difficulty': 3
            },
            {
                'question': '¿Qué es la recursión?',
                'options': {'A': 'Cuando una función se llama a sí misma', 'B': 'Un tipo de variable', 'C': 'Un error de compilación', 'D': 'Un bucle infinito'},
                'answer': 'A',
                'difficulty': 2
            },
            {
                'question': '¿Cuál es el mejor algoritmo de ordenamiento?',
                'options': {'A': 'Depende del contexto', 'B': 'Bubble Sort', 'C': 'Insertion Sort', 'D': 'Selection Sort'},
                'answer': 'A',
                'difficulty': 3
            },
            {
                'question': '¿Qué es Big O?',
                'options': {'A': 'Notación para analizar complejidad', 'B': 'Un operador', 'C': 'Una variable', 'D': 'Un tipo de dato'},
                'answer': 'A',
                'difficulty': 3
            },
        ]
    }
    
    @staticmethod
    def get_questions(category_id, count=5):
        """Obtiene preguntas aleatorias de una categoría"""
        import random
        if category_id in QuestionBank.QUESTIONS:
            return random.sample(QuestionBank.QUESTIONS[category_id], min(count, len(QuestionBank.QUESTIONS[category_id])))
        return []
    
    @staticmethod
    def get_all_questions():
        """Obtiene todas las preguntas"""
        return QuestionBank.QUESTIONS
