import math
import random

class TreeNode():
    # constructor
    def __init__(self, tablero, parent):
        self.tablero = tablero
        
        if self.tablero.is_ganado() or self.tablero.is_empate():
            self.is_terminal = True
        else:
            self.is_terminal = False

        # 
        self.is_fully_expanded = self.is_terminal
        # inicializar parent node si está disponible
        self.parent = parent
        # inicializar número de visitas al nodo
        self.visitas = 0
        # inicializar puntaje total del nodo
        self.puntaje = 0
        # inicializar children del nodo actual
        self.children = {}

# MCTS class
class MCTS():
    # buscar la mejor jugada en la posición actual
    def buscar(self, estado_inicial):
        # crear root node
        self.root = TreeNode(estado_inicial, None)
        # 1000 iteraciones
        for iteration in range(1000):
            # seleccionar nodo (fase de selección)
            node = self.seleccionar(self.root)
            
            # puntaje del nodo actual (fase de simulación)
            puntaje = self.rollout(node.tablero)
            
            # backpropagate resultados
            self.backpropagate(node, puntaje)
            
        # Elegir la mejor jugada en la posición actual
        try:
            return self.get_mejor_jugada(self.root, 0)
        except:
            pass
            
    # elegir el nodo más prometedor
    def seleccionar(self, node):
        # confirmar que los nodos no son terminales
        while not node.is_terminal:
            # nodo si está fully expanded
            if node.is_fully_expanded:
                node = self.get_mejor_jugada(node, 2) 
            # nodo no está fully expanded
            else:
                # si no, expandir el nodo
                return self.expand(node)
        # devolver el nodo
        return node
    
    # expandir el nodo
    def expand(self, node):
        # generar estados legales para el nodo
        estados = node.tablero.generar_estados()

        # loop sobre los estados generados
        for estado in estados:
            # asegurar que el estado actual no está presente en un nodo hijo
            if str(estado.position) not in node.children:
                # crear nuevo nodo
                new_node = TreeNode(estado, node)
                
                # agregar nodo hijo al diccionario de hijos del nodo padre
                node.children[str(estado.position)] = new_node
                
                # revisar si el nodo actual (padre) está fully expanded o no 
                if len(estados) == len(node.children):
                    node.is_fully_expanded = True
                    
                # devolver el nodo creado
                return new_node
        
        # debugging
        print('Should not get here!!!')

    def rollout(self, tablero):

        while not tablero.is_ganado():
            try:
                # Generar estados legales
                posibles_jugadas = tablero.generar_estados()
                if not posibles_jugadas:  # Si no hay jugadas posibles, es empate

                    return 0

                # Priorizar jugadas defensivas/ofensivas
                mejor_jugada = self.heuristica(posibles_jugadas)
                tablero = mejor_jugada if mejor_jugada else random.choice(posibles_jugadas)
            except Exception as e:
                print(f"Error en rollout: {e}")
                return 0  # Empate
        # Recompensa según el jugador que gane

        return 1 if tablero.jugador_2 == " x " else -1

    def heuristica(self, jugadas):
        for jugada in jugadas:
            if jugada.is_ganado():  # Priorizar jugadas ganadoras
                return jugada
        return None

    # backpropagate el número de visitas y puntuar hasta el root node
    def backpropagate(self, node, puntaje):
        # actualizar el nodo al nodo root
        while node is not None:
            node.visitas += 1
        
            # actualizar el puntaje del nodo
            node.puntaje += puntaje
        
            # set nodo al nodo padre
            node = node.parent

    # elegir el mejor nodo 
    def get_mejor_jugada(self, node, constante_exploracion):
        # definir el mejor puntaje y las mejores jugadas
        mejor_puntaje = float('-inf')
        mejores_jugadas = []

        # loop child nodes
        for child_node in node.children.values():
            # definir jugador actual
            if child_node.tablero.jugador_2 == " x ": jugador_actual = 1
            elif child_node.tablero.jugador_2 == " o ": jugador_actual = -1

            # obtener el puntaje de la jugada con la formula UCT
            puntaje_jugada = (jugador_actual * (child_node.puntaje / (child_node.visitas or 1)) + constante_exploracion * math.sqrt(math.log(node.visitas or 1) / (child_node.visitas or 1)))

            # jugada mejor encontrada
            if puntaje_jugada > mejor_puntaje:
                mejor_puntaje = puntaje_jugada
                mejores_jugadas = [child_node]

            # jugada de tan buen puntaje como ya había disponible
            elif puntaje_jugada == mejor_puntaje:
                mejores_jugadas.append(child_node)

        # devolver una de las mejores jugadas random
        return random.choice(mejores_jugadas)

























            

        
        
    
