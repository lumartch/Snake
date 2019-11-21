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

    def updateWindow(self):
        self.window.fill((0,0,0))   
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
    
    def gameplay(self):
        while self.flag:
            self.updateWindow()
            self.clock.tick(20)
            pygame.time.delay(50)

class SnakeBody:
    def __init__(self):
        pass
    
    def move(self):
        pass

    def draw(self):
        pass