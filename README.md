# tateti

├── main.py          # Código principal con la clase Tablero y el flujo del juego. \n
├── mcts.py          # Implementación del algoritmo Monte Carlo Tree Search. \n
├── requirements.txt # Lista de dependencias necesarias. \n
└── README.md        # Instrucciones y descripción del proyecto. \n

Instalación
1. Clona este repositorio:
   git clone https://github.com/tu_usuario/tateti-mcts.git

3. Ejecuta el juego:
   python tateti.py

Definición de los Archivos
1. Archivo Principal (tateti.py): Este archivo contiene la implementación de la clase Tablero, que define el entorno del juego de Ta-Te-Ti y el flujo principal del juego, tanto para el jugador humano como para la IA. También incluye la integración con el algoritmo Monte Carlo Tree Search (MCTS). Principales funciones:
- Tablero: Representa el estado del juego, detecta victorias, empates, y genera posibles jugadas.
- loop_juego: Define el flujo del juego, alternando entre el jugador humano y la IA.
- __str__: Representa el tablero en un formato amigable para el usuario.

2. Archivo de Monte Carlo Tree Search (mcts.py): Este archivo contiene la implementación del algoritmo Monte Carlo Tree Search (MCTS). Es utilizado por la IA para tomar decisiones estratégicas basadas en simulaciones y búsqueda en árboles. Principales funciones:
- TreeNode: Representa un nodo en el árbol de búsqueda.
- MCTS:
	- buscar: Encuentra la mejor jugada mediante simulaciones.
	- rollout: Realiza simulaciones aleatorias para evaluar un estado.
	- heuristica: Prioriza jugadas ganadoras en las simulaciones.
	- backpropagate: Propaga las recompensas hacia los nodos padres.
	- get_mejor_jugada: Selecciona la mejor jugada según la fórmula de UCT.

