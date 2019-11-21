import pygame

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
        self.window.fill((0,0,0))   
        self.snake.draw()
        self.drawGrid()
        pygame.display.update()

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
            self.updateWindow()
            self.clock.tick(20)
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

    # Función para el movimiento de la serpiente dentro del mapa
    def move(self):
        pass
    
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