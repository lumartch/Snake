import pygame
import random

# Clase para pintar el cuerpo de la serpiente en el mapa
class Snake:
    MIN_VALUE = 0
    MAX_VALUE = 3
    def __init__(self, size = 600, rows = 21, colorHead = (255,255,255), colorBody = (47,79,79), colorFood = (255,0,0)):
        # Variables para el manejo del cuerpo de la serpiente
        self.body = []
        self.size = size
        self.rows = rows
        self.head = (int(self.rows/2), int(self.rows/2))
        self.body.append(self.head)
        # Variable que castiga la cantidad de pasos dados
        self.pasos_restantes = 100
        # Variable para la distancia restante que quedá entre el Snake y la comida
        self.distancia = 0
        # Variables para el apartado gráfico de la serpiente y la comida
        self.colorHead = colorHead
        self.colorBody = colorBody
        self.colorFood = colorFood
        # Variables para agrear de forma continua el movimiento del Snake
        self.x = 0      # El Snake comenzará siempre su movimiento por la derecha
        self.y = 0      # El Snake no se movera de forma vertical
        # Variable para la posición de la comida
        self.food_position = 0
        self.new_food_pos()
        self.dis_food_snake()
        # Variables para definir el tamaño de la pantalla y sus subdivisiones
        self.width = size
        self.height = size
        # Bandera para terminar el juego
        self.flag = True
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
    def move(self, mejor_historico):
        # Se crea el ciclo donde será evaluado el listener
        for event in pygame.event.get():
            # Se crea el listener para el teclado
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT]:
                    if(self.x != 1):
                        self.x = -1
                        self.y = 0
                elif keys[pygame.K_RIGHT]:
                    if(self.x != -1):
                        self.x = 1
                        self.y = 0
                elif keys[pygame.K_UP]:
                    if(self.y != 1):
                        self.y = -1
                        self.x = 0
                elif keys[pygame.K_DOWN]:
                    if(self.y != -1):
                        self.y = 1
                        self.x = 0

        # Resta de forma indiferente el valor absoluto de X o Y a los pasos restantes
        self.pasos_restantes -= abs(self.x)
        self.pasos_restantes -= abs(self.y)
        # Se actualiza la nueva posición del Head del Snake y se bota la última posición que ya no es necesaria
        self.head = (self.head[0] + self.x, self.head[1] + self.y)
        self.body.insert(0, self.head)
        self.body.pop()
        # Se actualiza la distancia entre el Snake y la comida
        self.dis_food_snake()
    
    # Función para verificar si el Snake no ha chocado contra las paredes
    def collition(self):
        # Condicionante que corrobora que el Snake aún tiene pasos disponibles para dar
        if self.pasos_restantes > 1:
            # Verifica si no se ha salido del eje X o Y positivo/negativo en caso de hacerlo, se termina el juego
            if self.head[0] > self.rows - 1 or self.head[1] > self.rows - 1 or self.head[0] < 0 or self.head[1] < 0:
                return False
            # Verifica que la colisión haya llegado con la posición de la comida
            elif self.head == self.food_position:
                # Premio de pasos para que el Snake siga caminando
                self.pasos_restantes += 100
                # Crea una nueva posición para la comida del Snake
                self.new_food_pos()
                # Crea un nuevo cuerpo para el Snake agregando la comida que se comió
                self.body.insert(0, self.head)
                return True
            else:
                # Verifica si la posición del Head colisiona con alguna parte del Body
                for i in range(len(self.body)):
                    if i != 0:      # Se salta el Head para solo evaluar el resto del cuerpo
                        if self.head == self.body[i]:
                            return False
                return True
        else:
            return False

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
        self.food_position = (random.randint(0, self.rows -1), random.randint(0,self.rows - 1))
        for i in range(len(self.body)):
            if self.food_position == self.body[i]:
                i = 0
                self.food_position = (random.randint(0, self.rows - 1), random.randint(0,self.rows - 1))
    
    # Función que cálcula la distancia restante entre el Snake y la comida
    def dis_food_snake(self):
        x = self.food_position[0] - self.head[0]
        y = self.food_position[1] - self.head[1]
        self.distancia = abs(x) + abs(y)

    def fitness(self, cromosoma):
        r = 0
        for i in range(len(cromosoma)):
            r += abs(cromosoma[i]) /self.food_position 
        return r