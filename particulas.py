import pygame
import random

class Particula(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 5)) 
        self.image.fill((255, 0, 0)) # Color rojo para la sangre 
        self.rect = self.image.get_rect(center=(x, y)) 
        self.velocidad_x = random.uniform(-2, 2) 
        self.velocidad_y = random.uniform(-2, 2) 
        self.tiempo_vida = 30 # Duración de la partícula en frames

    def update(self): 
        self.rect.x += self.velocidad_x 
        self.rect.y += self.velocidad_y 
        self.tiempo_vida -= 1 
        if self.tiempo_vida <= 0: 
            self.kill()