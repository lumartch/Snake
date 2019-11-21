import pygame
import copy

class Snake:
    def __init__(self, size = 600, rows = 21):
        # Variables para definir el tamaño de la pantalla y sus subdivisiones
        self.width = size
        self.height = size
        self.size = size
        self.rows = rows
        # Bandera para terminar el juego
        self.flag = True
        # Variables para mostrar la pantalla
        self.window = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        # Instancia de la clase Snake
        self.snake = SnakeBody(self.size, self.rows, self.window)

    # Función para actualizar el estado de la pantalla
    def updateWindow(self):
        self.window.fill((0,0,0))       # Define el color de la pantalla en NEGRO
        self.snake.draw()               # Dibuja la serpiente en pantalla
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
    
    # Función para desplegar el gamplay completo del snake
    def gameplay(self):
        while self.flag:
            self.updateWindow()             # Actualización de los elementos en pantalla
            self.clock.tick(5)              # Velocidad del juego
            self.snake.move()               # Listener del movimiento del Snake
            self.flag = self.snake.colittion() # Corroboración de los límites del snake
            pygame.time.delay(50)

# Clase para pintar el cuerpo de la serpiente en el mapa
class SnakeBody:
    def __init__(self, size, rows, window, colorHead = (255,255,255), colorBody = (47,79,79)):
        # Variables para el manejo del cuerpo de la serpiente
        self.body = []
        self.size = size
        self.rows = rows
        self.head = (int(self.rows/2), int(self.rows/2))
        self.body.append(self.head)
        # Variables para el apartado gráfico de la serpiente
        self.window = window
        self.colorHead = colorHead
        self.colorBody = colorBody
        # Variables para agrear de forma continua el movimiento del Snake
        self.x = 1
        self.y = 0

    # Función para el movimiento de la serpiente dentro del mapa
    def move(self):
        aux_body = []
        # Se crea el ciclo donde será evaluado el listener
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
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
        # Se actualiza la nueva posición del Head del Snake
        self.head = (self.head[0] + self.x, self.head[1] + self.y)
        # Se crea un nuevo cuerpo para la serpiente de forma auxiliar
        aux_body.append(self.head)
        for i in range(len(self.body) - 1):
            aux_body.append(self.body[i])
        # El cuerpo nuevo sustituye al viejo
        self.body = aux_body.copy()
    
    # Función para verificar si el Snake no ha chocado contra las paredes
    def colittion(self):
        # Verifica si no se ha salido del eje X o Y positivo en caso de hacerlo, se termina el juego
        if self.head[0] > self.rows or self.head[1] > self.rows:
            pygame.display.quit()
            pygame.quit()
            return False
        # Verifica si no se ha salido del eje X o Y negativo en caso de hacerlo, se termina el juego
        elif self.head[0] < 0 or self.head[1] < 0:
            pygame.display.quit()
            pygame.quit()
            return False
        else:
            return True


    
    # Dibuja el cuerpo de la serpiente en pantalla
    def draw(self):
        is_head = True
        # Por cada elemento guardado en la variable "Body" se tomaran los ejex X y Y para pintarlos en pantalla
        for b in self.body: 
            i = b[0]
            j = b[1]
            dis = self.size / self.rows
            if is_head:
                pygame.draw.rect(self.window, self.colorHead, (i * dis + 1, j * dis + 1, dis, dis))
                is_head = False
            else:
                pygame.draw.rect(self.window, self.colorBody, (i * dis + 1, j * dis + 1, dis, dis))