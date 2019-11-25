import copy
import numpy as np
import pygame

# Clase Individuo
class Individuo:
    def __init__(self, dimensiones, cromosoma):
        self.dimensiones = dimensiones
        self.cromosoma = cromosoma
        self.fitness = 0

# Algoritmo Genético continuo
class AGC:
    def __init__(self, problema, c_individuos = 80, generaciones = 2000, dimensiones = 2, indice_mutacion = 0.02):
        # Variables para el algoritmo genético
        self.c_individuos = c_individuos
        self.dimensiones = dimensiones
        self.generaciones = generaciones
        self.indice_mutacion = indice_mutacion
        # Problema a evaluar -> Snake
        self.problema = problema
        # Arreglo de individuos
        self.array_individuos = np.array([])
        # El mejor individuo histórico
        self.mejor_historico = 0

    # Inicializa a los individuos del algoritmo
    def inicializar_individuos(self):
        for i in range(self.c_individuos):
            cromosoma = self.problema.MIN_VALUE + np.random.random(size = self.dimensiones) * (self.problema.MAX_VALUE - self.problema.MIN_VALUE)
            individuo = Individuo(self.dimensiones, cromosoma)
            self.array_individuos = np.append(self.array_individuos, [individuo])

    # Se hace la evaluación del fitness del individuo
    def evaluar_individuos(self):
        for individuo in self.array_individuos:
            individuo.fitness = self.problema.fitness(individuo.cromosoma)
            individuo.fitness *= -1
            individuo.fitness += self.problema.MAX_VALUE ** self.dimensiones * 1000

    def ruleta(self):
        f_sum = np.sum([individuo.fitness for individuo in self.array_individuos])
        r = np.random.randint(f_sum + 1, dtype = np.int64)
        k = 0
        F = self.array_individuos[k].fitness
        while F < r and k < (len(self.array_individuos) - 1):
            k += 1
            F += self.array_individuos[k].fitness
        return k

    def cruza(self, i1, i2):
        h1 = copy.deepcopy(i1)
        h2 = copy.deepcopy(i2)
        s = self.dimensiones - 1
        punto_cruza = np.random.randint(s) + 1
        for i in range(punto_cruza, self.dimensiones):
            h1.cromosoma[i], h2.cromosoma[i] = h2.cromosoma[i], h1.cromosoma[i]
        return h1, h2

    def mutacion(self, hijos):
        for h in hijos:
            for a in range(len(h.cromosoma)):
                if np.random.rand() < self.indice_mutacion:
                    h.cromosoma[a] = self.problema.MIN_VALUE + np.random.random() * (self.problema.MAX_VALUE - self.problema.MIN_VALUE)

    def mejor(self):
        for individuo in self.array_individuos:
            if individuo.fitness > self.mejor_historico.fitness:
                self.mejor_historico = copy.deepcopy(individuo)

    def run(self):
        #self.inicializar_individuos()
        #self.mejor_historico = self.array_individuos[0]
        #generacion = 0
        # Condición de paro para el algoritmo genético
        while self.problema.flag:
            #self.evaluar_individuos()
            #self.mejor()
            # Código que va ligado a pintar el mejor individuo en 
            self.problema.updateWindow()                        # Actualización de los elementos en pantalla
            self.problema.clock.tick(10)                        # Velocidad del juego
            self.problema.move(self.mejor_historico)                          # Listener del movimiento del Snake
            self.problema.flag = self.problema.collition()# Corroboración de los límites del snake
            pygame.time.delay(10)
            # Implementación del algoritmo Genético
        #    hijos = np.array([])
        #    while len(hijos) < len(self.array_individuos):
        #        padre1 = self.ruleta()
        #        padre2 = self.ruleta()
        #        while padre1 == padre2:
        #            padre2 = self.ruleta()
        #        h1, h2 = self.cruza(self.array_individuos[padre1], self.array_individuos[padre2])
        #        hijos = np.append(hijos, [h1])
        #        hijos = np.append(hijos, [h2])
        #    self.mutacion(hijos)
        #    self.array_individuos = np.copy(hijos)
        #    print("Generación: ", generacion, 'Mejor Histórico: ', self.mejor_historico.cromosoma, -1 * (self.mejor_historico.fitness - self.problema.MAX_VALUE ** self.dimensiones * 1000))
        #    generacion += 1
        pygame.display.quit()
        pygame.quit()