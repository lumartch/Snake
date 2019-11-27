import pygame
import random
import time

# Clase para pintar el cuerpo de la serpiente en el mapa
class Snake:
    MIN_VALUE = 1
    MAX_VALUE = 3
    def __init__(self, size = 600, rows = 21, colorHead = (255,255,255), colorBody = (47,79,79), colorFood = (255,0,0)):
        # Variables para el manejo del cuerpo de la serpiente
        self.body = []
        self.size = size
        self.rows = rows
        self.head = (int(self.rows/2), int(self.rows/2))
        self.body.append(self.head)
        # Variable para la distancia restante que quedá entre el Snake y la comida
        self.distancia = 0
        # Variables para el apartado gráfico de la serpiente y la comida
        self.colorHead = colorHead
        self.colorBody = colorBody
        self.colorFood = colorFood
        # Variables para agrear de forma continua el movimiento del Snake
        self.x = 1      # El Snake comenzará siempre su movimiento por la derecha
        self.y = 0      # El Snake no se movera de forma vertical
        # Variable para la posición de la comida
        self.food_position = 0
        self.new_food_pos()
        # Variables para definir el tamaño de la pantalla y sus subdivisiones
        self.width = size
        self.height = size
        # Variables para mostrar la pantalla
        self.window = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
    
    # Función para actualizar el estado de la pantalla
    def updateWindow(self):
        self.window.fill((0,0,0))       # Define el color de la pantalla en NEGRO
        self.draw_food()
        self.draw()                     # Dibuja la serpiente en pantalla
        self.drawGrid()                 # Dibuja el cuadriculado en pantalla
        pygame.display.update()         # Muestra lo previamente dibujado en la ventana a modo de Update

    # Función para desplegar la subdivisión de la pantalla
    def drawGrid(self):
        square_size = self.size / self.rows
        x = 0
        y = 0
        for l in range(self.rows):
            x = x + square_size
            y = y + square_size
            pygame.draw.line(self.window, (255,255,255), (x,0), (x, self.width))
            pygame.draw.line(self.window, (255,255,255), (0,y), (self.width, y))

    # Función para el movimiento de la serpiente dentro del mapa
    def move(self, individuo):
        f = 10*(individuo.fitness - int(individuo.fitness))
        x_y = self.random_x_y(f)
        print(f)
        print(x_y)
        self.x = x_y[0]
        self.y = x_y[1]
        if x_y == self.food_position:
            self.draw_food()
        # Se actualiza la nueva posición del Head del Snake y se bota la última posición que ya no es necesaria
        self.head = [self.head[0] + self.x, self.head[1] + self.y]
        self.body.insert(0, self.head)
        self.body.pop()
    
    # Función para verificar si el Snake no ha chocado contra las paredes
    def collition(self, x_y):
        # Verifica si no se ha salido del eje X o Y positivo/negativo en caso de hacerlo, se termina el juego
        if x_y[0] > self.rows - 1 or x_y[1] > self.rows - 1 or x_y[0] < 0 or x_y[1] < 0:
            return 0
        # Verifica que la colisión haya llegado con la posición de la comida
        elif x_y == self.food_position:
            return 2
        else:
            # Verifica si la posición del Head colisiona con alguna parte del Body
            for i in range(len(self.body)):
                if i != 0:      # Se salta el Head para solo evaluar el resto del cuerpo
                    if x_y == self.body[i]:
                        return 0
            return 1

    # Dibuja el cuerpo de la serpiente en pantalla
    def draw(self):
        is_head = True
        # Por cada elemento guardado en la variable "Body" se tomaran los ejex X y Y para pintarlos en pantalla
        for b in self.body: 
            x = b[0]
            y = b[1]
            dis = self.size / self.rows
            if is_head:
                pygame.draw.rect(self.window, self.colorHead, (x * dis + 1, y * dis + 1, dis, dis))
                is_head = False
            else:
                pygame.draw.rect(self.window, self.colorBody, (x * dis + 1, y * dis + 1, dis, dis))
    
    # Dibuja la comida en el mapa
    def draw_food(self):
        # Se toma la posición de la comida para colocarse en pantalla
        x = self.food_position[0]
        y = self.food_position[1]
        dis = self.size / self.rows
        pygame.draw.rect(self.window, self.colorFood, (x * dis + 1, y * dis + 1, dis, dis))

    # Asigna una nueva posición aleatoria al alimento, que no se encuentre en colisión con el cuerpo del Snake
    def new_food_pos(self):
        #self.food_position = [10, 9]
        self.food_position = (random.randint(0, self.rows -1), random.randint(0,self.rows - 1))
        for i in range(len(self.body)):
            if self.food_position == self.body[i]:
                i = 0
                self.food_position = (random.randint(0, self.rows - 1), random.randint(0,self.rows - 1))
    
    # Función que cálcula la distancia restante entre el Snake y la comida
    def dis_food_snake(self, x_y):
        print(x_y)
        x = self.food_position[0] - x_y[0]
        y = self.food_position[1] - x_y[1]
        distancia = abs(x) + abs(y)
        if distancia == 0:
            distancia = 0.1
        return distancia

    def fitness(self, cromosoma):
        f = 0
        # Suma del cromosoma
        for c in cromosoma:
            f += c
        f = int(f%3)
        # Asigna de forma aleatoria el
        x_y = self.random_x_y(f)
        x_y = [x_y[0] + self.head[0], x_y[1] + self.head[1]]
        # Cálculo de la colisión
        mul = self.collition(x_y)
        # Cálculo de la distancia
        distancia = self.dis_food_snake(x_y)
        distancia = 100*(1/distancia)
        distancia *= mul
        # Unión del fitness con el código para el cálculo de las posiciones en X_Y
        f = f/10
        f += int(distancia)
        return f

    def random_x_y(self, f):
        aux_x = 0
        aux_y = 0
        if self.x:
            if f == 0:
                aux_x = 0
                aux_y = 1
            elif f == 1:
                aux_x = 0
                aux_y = -1
            else:
                aux_x = self.x
                aux_y = self.y
        else:
            if f == 0:
                aux_x = 1
                aux_y = 0
            elif f == 1:
                aux_x = -1
                aux_y = 0
            else:
                aux_x = self.x
                aux_y = self.y
        return ([aux_x, aux_y])
