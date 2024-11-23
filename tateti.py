from copy import deepcopy
from mcts import *

# clase tablero
class Tablero():
    # método constructor
    def __init__(self, tablero=None):
        # definir jugadores
        self.jugador_1 = " x "
        self.jugador_2 = " o "
        self.casillero_vacio = " . "

        # definir posición en el tablero
        self.position = {}

        # inicio (reset) del tablero
        self.init_tablero()
        
        # crear una copia de un estado previo del tablero si se encuentra disponible
        if tablero is not None:
            self.__dict__ = deepcopy(tablero.__dict__)

    # inicio (reset) del tablero
    def init_tablero(self):
        # loop en las filas
        for row in range(3):
            # loop en las columnas
            for col in range(3):
                # definir cada casillero del tablero a "vacio"
                self.position[row, col] = self.casillero_vacio

    # método para que el jugador efectue su jugada
    def hacer_jugada(self, row, col):
        # crear nueva instancia de tablero que hereda del estado actual
        tablero = Tablero(self)

        # hacer jugada
        tablero.position[row, col] = self.jugador_1

        # cambiar jugadores
        (tablero.jugador_1, tablero.jugador_2) = (tablero.jugador_2, tablero.jugador_1)

        # devolver un nuevo estado de tablero
        return tablero

    # ¿empate?
    def is_empate(self):
        # loop en los casilleros
        for row, col in self.position:
            # casillero vacío está disponible
            if self.position[row, col] == self.casillero_vacio:
                # no hay empate
                return False
            
        # devuelve Empate por defecto
        return True

    # ¿hay ganador?
    def is_ganado(self):
        ##########################################
        # detección de secuencia vertical ganadora
        for col in range(3):
            # defiir lista de secuencia ganadora 
            secuencia_ganadora = []
            
            # loop filas
            for row in range(3):
                # si se encuentra el mismo elemento siguiente en la fila 
                if self.position[row, col] == self.jugador_2:
                    # actualizar sequencia ganadora
                    secuencia_ganadora.append((row, col))
                    
                # si hay 3 elementos
                if len(secuencia_ganadora) == 3:
                    # devolver estado de juego: hay ganador
                    return True
                    
        ##########################################
        # detección de secuencia horizontal ganadora
        for row in range(3):
            # defiir lista de secuencia ganadora 
            secuencia_ganadora = []
            
            # loop columnas
            for col in range(3):
                # si se encuentra el mismo elemento siguiente en la columna 
                if self.position[row, col] == self.jugador_2:
                    # actualizar sequencia ganadora
                    secuencia_ganadora.append((row, col))
                    
                # si hay 3 elementos 
                if len(secuencia_ganadora) == 3:
                    # devolver estado de juego: hay ganador
                    return True

        ##########################################
        # detección de secuencia diagonal 1 ganadora
        # defiir lista de secuencia ganadora 
        secuencia_ganadora = []
        # loop filas
        for row in range(3):
            # iniciat columna
            col = row
        
            # si se encuentra el mismo elemento siguiente en la fila 
            if self.position[row, col] == self.jugador_2:
                # actualizar sequencia ganadora
                secuencia_ganadora.append((row, col))
                
            # si hay 3 elementos 
            if len(secuencia_ganadora) == 3:
                # devolver estado de juego: hay ganador
                return True

        ##########################################
        # detección de secuencia diagonal 2 ganadora
        # defiir lista de secuencia ganadora 
        secuencia_ganadora = []
        # loop filas
        for row in range(3):
            # iniciat columna
            col = 3 - row - 1
        
            # si se encuentra el mismo elemento siguiente en la fila 
            if self.position[row, col] == self.jugador_2:
                # actualizar sequencia ganadora
                secuencia_ganadora.append((row, col))
                
            # si hay 3 elementos 
            if len(secuencia_ganadora) == 3:
                # devolver estado de juego: hay ganador
                return True
                
        ##########################################
        # default: devolver estado: no hay ganador
        return False

    # generar jugadas legales en la posición actual
    def generar_estados(self):
        # definir lista de estados
        acciones = []

        # loop filas
        for row in range(3):
            # loop columnas
            for col in range(3):
                # ¿casillero vacio?
                if self.position[row, col] == self.casillero_vacio:
                    # append acciones disponibles/estado a la lista de estados
                    acciones.append(self.hacer_jugada(row, col))

        # devolver la lista de estados disponibles (instancias de clase tablero)
        return acciones

    # loop principal de juego
    def loop_juego(self):
        print("Ta te ti")
        print("Escriba 'exit' para salir del juego")
        print("Formato de jugada: [x,y]: 1,2 donde 1 es columna y 2 es fila")
        print("\n")

        # imprimir tablero
        print(self)

        # crear MCTS instancia
        mcts = MCTS()
                
        # loop
        while True:
            # input del usuario
            user_input = input('> ')
        
            # escape
            if user_input == 'exit': break
            
            # saltear input vacio
            if user_input == '': continue
            
            try:
                # parse input del usuario (formato [col, row]: 1,2) 
                row = int(user_input.split(',')[1]) - 1
                col = int(user_input.split(',')[0]) - 1

                # legalidad de la jugada
                if self.position[row, col] != self.casillero_vacio:
                    print('Jugada ilegal!')
                    continue

                # hacer jugada en el tablero
                self = self.hacer_jugada(row, col)
                
                # imprimir tablero
                print(self)
                
                # buscar la mejor jugada
                mejor_jugada = mcts.buscar(self)

                # jugadas legales disponibles
                try:
                    # jugada IA
                    self = mejor_jugada.tablero
                
                # game over!
                except Exception as mcts_error:
                    pass
                
                # imprimir tablero
                print(self)
                
                # revisar si hay ganador
                if self.is_ganado():
                    print('¡jugador "%s" ganó el juego!\n' % self.jugador_2)
                    break
                
                # revisar si hay empate
                elif self.is_empate():
                    print('¡Hay empate!\n')
                    break
            
            except Exception as e:
                print(f"Error inesperado: {e}")
                print('Formato de jugada: [x,y]: 1,2 donde 1 es columna y 2 es fila')

    # imprimir tablero
    def __str__(self):
        tablero_string = ""
        # loop en las filas
        for row in range(3):
            # loop en las columnas
            for col in range(3):
                tablero_string += '%s' % self.position[row, col]

            tablero_string += "\n"

        if self.jugador_1 == " x ":
            tablero_string = '\n ---------- \n "x" to move: \n ---------- \n\n' + tablero_string
        elif self.jugador_1 == " o ":
            tablero_string = '\n ---------- \n "o" to move: \n ---------- \n\n' + tablero_string
        
        return tablero_string


# main driver
if __name__ == "__main__":
    # crear instancia de tablero
    tablero = Tablero()
    tablero.loop_juego()
    




