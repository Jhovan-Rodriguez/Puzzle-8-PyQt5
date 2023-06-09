"""
Problema PUZZLE8

Integrantes:
CANALES PUGA JONATHAN,
CANTU SANCHEZ NUBIA ESMERALDA,
GARCIA CERVANTES VANESSA ITZAIANA∗,
MIRELES SENA YANEL AZUCENA and,
RODRIGUEZ MORENO JORGE JHOVAN

--Necesario para la ejecucion de este programa libreria collections: uso hacer diccionarios, colas y pilas
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from collections import deque

class PuzzleGrid(QWidget):
    def __init__(self):
        super().__init__()

        # Creamos un layout en cuadrícula para colocar los elementos de la interfaz
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        # Cambiar el estilo del widget
        #self.setStyleSheet("background-color: lightblue;")

        # Creamos los botones y los agregamos al layout en las posiciones correspondientes
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                button = QPushButton(str(i*3 + j + 1))
                button.setStyleSheet("width: 70px; height: 70px; border: 1px solid black; background-color: lightblue; color: black;  font-size: 18px;")
                button.clicked.connect(self.move_button)
                row.append(button)
                self.grid.addWidget(button, i, j)
            self.buttons.append(row)

        # Reemplazamos el último botón por un espacio vacío, y almacenamos su posición
        self.buttons[2][2].setText("")
        self.empty_space = (2, 2)

        
    def move_button(self):
        # Encuentra el botón que fue presionado
        button = self.sender()
        x, y = None, None
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j] == button:
                    x, y = i, j
        # Comprueba si el botón puede ser movido (si está al lado del espacio vacío)
        if abs(self.empty_space[0] - x) + abs(self.empty_space[1] - y) == 1:
             # Si puede, intercambia el texto del botón y el espacio vacío
            self.buttons[self.empty_space[0]][self.empty_space[1]].setText(button.text())
            button.setText("")
            button.setStyleSheet("width: 70px; height: 70px; border: 1px solid black; background-color: lightblue; color: black;  font-size: 18px;")
            self.empty_space = (x, y)

    def get_state(self):
        # Obtiene el estado actual del puzzle (el texto de todos los botones)
        state = []
        for i in range(3):
            for j in range(3):
                state.append(self.buttons[i][j].text())
        return state

    def set_state(self, state):
        # Establece el estado del puzzle (el texto de todos los botones)
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].setText(state[i*3+j])
                self.buttons[i][j].setStyleSheet("width: 70px; height: 70px; border: 1px solid black; background-color: lightblue; color: black;  font-size: 18px;")   
                if(state[i*3+j]==''):
                    self.buttons[i][j].setStyleSheet("width: 70px; height: 70px; border: 1px solid black; background-color: #E1BEE7; color: black;  font-size: 18px;  ")

       
                

    def reset(self):
        # Restablece el estado del puzzle a la posición inicial
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].setStyleSheet("width: 70px; height: 70px; border: 1px solid black; background-color: lightblue; color:black; font-size: 18px")

                if i == 2 and j == 2:
                    self.buttons[i][j].setText("")
                else:
                    self.buttons[i][j].setText(str(i*3 + j + 1))
        self.empty_space = (2, 2)

def a_star(start, goal):
    # Crea una cola de prioridad para almacenar los estados, ordenados por su costo estimado
    priority_queue = []
    priority_queue.append((0, start))

    # Crea un diccionario para almacenar los estados visitados y su predecesor
    visited = {tuple(start): None}

    while priority_queue:
        cost, state = priority_queue.pop(0)
        if state == goal:
            # Si hemos alcanzado el estado objetivo, reconstruir el camino desde el estado inicial al estado objetivo
            path = []
            while state:
                path.append(state)
                state = visited[tuple(state)]
            path.reverse()
            return path

        empty_index = state.index("")
        x, y = divmod(empty_index, 3)
        # Mover el espacio vacío en todas las direcciones posibles
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_state = state.copy()
                swap_index = nx * 3 + ny
                new_state[empty_index], new_state[swap_index] = new_state[swap_index], new_state[empty_index]
                if tuple(new_state) not in visited:
                    new_cost = cost + heuristic(new_state, goal)
                    priority_queue.append((new_cost, new_state))
                    visited[tuple(new_state)] = state

    return None


def heuristic(state, goal):
    # Calcula la distancia de Manhattan entre el estado actual y el estado objetivo
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i * 3 + j] != "":
                distance += abs(i - (goal.index(state[i * 3 + j]) // 3)) + abs(j - (goal.index(state[i * 3 + j]) % 3))
    return distance




def bfs(start, goal):
    # Crea un diccionario para almacenar los estados visitados y su predecesor
    visited = {tuple(start): None}
    queue = deque([start])

    while queue:
        state = queue.popleft()
        if state == goal:
            # Si hemos alcanzado el estado objetivo, reconstruir el camino desde el estado inicial al estado objetivo
            path = []
            while state:
                path.append(state)
                state = visited[tuple(state)]
            path.reverse()
            return path
        empty_index = state.index("")
        x, y = divmod(empty_index, 3)
        # Mover el espacio vacío en todas las direcciones posibles
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_state = state.copy()
                swap_index = nx * 3 + ny
                new_state[empty_index], new_state[swap_index] = new_state[swap_index], new_state[empty_index]
                if tuple(new_state) not in visited:
                    queue.append(new_state)
                    visited[tuple(new_state)] = state

def dfs(start, goal):
    # Crea una pila para almacenar los estados, ordenados por su profundidad
    stack = [(start, 0)]

    # Crea un diccionario para almacenar los estados visitados y su predecesor
    visited = {tuple(start): None}

    while stack:
        state, depth = stack.pop()
        if state == goal:
            # Si hemos alcanzado el estado objetivo, reconstruir el camino desde el estado inicial al estado objetivo
            path = []
            while state:
                path.append(state)
                state = visited[tuple(state)]
            path.reverse()
            return path

        empty_index = state.index("")
        x, y = divmod(empty_index, 3)
         # Mover el espacio vacío en todas las direcciones posibles
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_state = state.copy()
                swap_index = nx * 3 + ny
                new_state[empty_index], new_state[swap_index] = new_state[swap_index], new_state[empty_index]
                if tuple(new_state) not in visited:
                    stack.append((new_state, depth + 1))
                    visited[tuple(new_state)] = state

    return None

def iddfs(start, goal, max_depth):
        # Crea un diccionario para almacenar los estados visitados y su predecesor
        visited = {tuple(start): None}
        stack = [(start, 0)]

        while stack:
            state, depth = stack.pop()
            if state == goal:
                # Si hemos alcanzado el estado objetivo, reconstruir el camino desde el estado inicial al estado objetivo
                path = []
                while state:
                    path.append(state)
                    state = visited[tuple(state)]
                path.reverse()
                return path
            if depth < max_depth:
                empty_index = state.index("")
                x, y = divmod(empty_index, 3)
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 3 and 0 <= ny < 3:
                        new_state = state.copy()
                        swap_index = nx * 3 + ny
                        new_state[empty_index], new_state[swap_index] = new_state[swap_index], new_state[empty_index]
                        if tuple(new_state) not in visited:
                            stack.append((new_state, depth + 1))
                            visited[tuple(new_state)] = state

        return None

class Puzzle(QWidget):
    def __init__(self):
        super().__init__()

        # Crear un layout vertical
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        # Crear un botón para reiniciar el puzzle y agregarlo al layout
        self.restart_button = QPushButton("Reiniciar")
        self.restart_button.setStyleSheet('QPushButton { font-size: 16px; min-width: 100px; min-height: 30px; }')
        self.restart_button.clicked.connect(self.restart)
        self.restart_button.setDisabled(True)
        vbox.addWidget(self.restart_button)

        hbox1 = QHBoxLayout()
        vbox.addLayout(hbox1)
        label1=QLabel('Estado Inicial')
        label1.setStyleSheet('font-size:14px')
        label1.setAlignment(Qt.AlignCenter)

        label2=QLabel('Estado Objetivo')
        label2.setStyleSheet('font-size:14px')
        label2.setAlignment(Qt.AlignCenter)
        
        hbox1.addWidget(label1)
        hbox1.addWidget(label2)

        # Crea un layout horizontal para los puzzles
        hbox = QHBoxLayout()
        vbox.addLayout(hbox)


        # Crea dos widgets de cuadrícula de puzzle y agregarlos al layout
        self.grid1 = PuzzleGrid()
        self.grid2 = PuzzleGrid()
        hbox.addWidget(self.grid1)
        hbox.addWidget(self.grid2)

        # Crear un botón para resolver el puzzle y agregarlo al layout
        self.solve_bfs_button = QPushButton("Resolver por BFS")
        self.solve_bfs_button.setStyleSheet('QPushButton { font-size: 16px; min-width: 100px; min-height: 30px; }')
        self.solve_bfs_button.clicked.connect(self.solve_bfs)
        self.solve_bfs_button.setEnabled(True)
        vbox.addWidget(self.solve_bfs_button)

        # Crea un botón para resolver el puzzle por DFS y agregarlo al layout
        self.solve_dfs_button = QPushButton("Resolver por DFS")
        self.solve_dfs_button.setStyleSheet('QPushButton { font-size: 16px; min-width: 100px; min-height: 30px; }')
        self.solve_dfs_button.clicked.connect(self.solve_dfs)
        vbox.addWidget(self.solve_dfs_button)
        
        #Se crea un boton para usar el algorimto IDDFS # Create a new button and set its text to "Solve by IDDFS".
        self.solve_iddfs_button = QPushButton("Resolver por IDDFS")
        self.solve_iddfs_button.clicked.connect(self.solve_iddfs)
        self.solve_iddfs_button.setStyleSheet('QPushButton { font-size: 16px; min-width: 100px; min-height: 30px; }')
        vbox.addWidget(self.solve_iddfs_button)

        # #Se crea un boton para usar el algorimto A start.
        self.solve_a_star_button = QPushButton("Resolver por A-Star")
        self.solve_a_star_button.setStyleSheet('QPushButton { font-size: 16px; min-width: 100px; min-height: 30px; }')
        self.solve_a_star_button.clicked.connect(self.solve_a_star)
        vbox.addWidget(self.solve_a_star_button)

    def solve_a_star(self):
        self.solve_bfs_button.setDisabled(True)
        self.solve_dfs_button.setDisabled(True)
        self.solve_iddfs_button.setDisabled(True)
        self.solve_a_star_button.setDisabled(True)
        
        self.disable_buttons(self.grid1.buttons)
        self.disable_buttons(self.grid2.buttons)
        self.grid2.buttons[0][0].setDisabled(True
                                             )
        # se implementa el algoritmo A* aquí
        self.grid1.solving = True
        start_state = self.grid1.get_state()
        goal_state = self.grid2.get_state()
        self.solution = a_star(start_state, goal_state)
        self.step = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.show_step)
        self.timer.start(500)
        self.restart_button.setEnabled(True)


    def solve_iddfs(self):
        self.solve_bfs_button.setDisabled(True)
        self.solve_dfs_button.setDisabled(True)
        self.solve_iddfs_button.setDisabled(True)
        self.solve_a_star_button.setDisabled(True)
        self.disable_buttons(self.grid1.buttons)
        self.disable_buttons(self.grid2.buttons)
        # se implementa el algoritmo IDDFS aquí
        self.grid1.solving = True
        start_state = self.grid1.get_state()
        goal_state = self.grid2.get_state()
        max_depth = 9
        self.solution = iddfs(start_state, goal_state, max_depth)
        self.step = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.show_step)
        self.timer.start(500)
        self.restart_button.setEnabled(True)




    def solve_bfs(self):
        self.solve_bfs_button.setDisabled(True)
        self.solve_dfs_button.setDisabled(True)
        self.solve_iddfs_button.setDisabled(True)
        self.solve_a_star_button.setDisabled(True)
        self.disable_buttons(self.grid1.buttons)
        self.disable_buttons(self.grid2.buttons)
        # se implementa el algoritmo BFS aquí
        self.grid1.solving = True
        start_state = self.grid1.get_state()
        goal_state = self.grid2.get_state()
        self.solution = bfs(start_state, goal_state)
        self.step = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.show_step)
        self.timer.start(500)
        self.restart_button.setEnabled(True)

    def solve_dfs(self):
        self.solve_bfs_button.setDisabled(True)
        self.solve_dfs_button.setDisabled(True)
        self.solve_iddfs_button.setDisabled(True)
        self.solve_a_star_button.setDisabled(True)
        self.disable_buttons(self.grid1.buttons)
        self.disable_buttons(self.grid2.buttons)
        #se implementa el algoritmo DFS aquí
        self.grid1.solving = True
        start_state = self.grid1.get_state()
        goal_state = self.grid2.get_state()
        self.solution = dfs(start_state, goal_state)
        self.step = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.show_step)
        self.timer.start(500)
        self.restart_button.setEnabled(True)

    def enable_buttons(self,buttons):
        # Esta función habilita todos los botones en la lista proporcionada
        for row in buttons: 
            for button in row:
                button.setDisabled(False) # Habilitar el botón

    def disable_buttons(self,buttons):
        # Esta función deshabilita todos los botones en la lista proporcionada
        for row in buttons: 
            for button in row: 
                button.setDisabled(True) # Deshabilitar el botón
                # Establecer el estilo del botón para indicar que está deshabilitado
                button.setStyleSheet("width: 70px; height: 70px; border: 1px solid black; background-color: lightblue; color: black;  font-size: 18px;")    

    def show_step(self):
        # Esta función muestra cada paso de la solución en el grid
        if self.solution and self.step < len(self.solution): # Si hay una solución y el paso actual es menor que la longitud de la solución
            self.grid1.set_state(self.solution[self.step]) # Mostrar el estado actual de la solución en el grid
            self.step += 1 # Incrementar el paso
        else:
            self.timer.stop() # Detener el temporizador si no hay más pasos o si no hay solución
            self.grid1.solving = False  # Asegurarse de que los botones puedan ser movidos de nuevo
    def restart(self):
            # Detener el temporizador si está activo
        if self.timer.isActive():
            self.timer.stop()
            

        # Restablecer las cuadrículas
        self.grid1.reset()
        self.grid2.reset()

        # Restablecer las variables relacionadas con la resolución del rompecabezas
        self.solution = None
        self.step = 0
        self.grid1.solving = False
        
        
        self.restart_button.setDisabled(True)
        self.solve_bfs_button.setEnabled(True)
        self.solve_dfs_button.setEnabled(True)
        self.solve_iddfs_button.setEnabled(True)
        self.solve_a_star_button.setEnabled(True)
        self.enable_buttons(self.grid1.buttons)
        self.enable_buttons(self.grid2.buttons)


def main():
    app = QApplication(sys.argv)

    puzzle = Puzzle()
    puzzle.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
