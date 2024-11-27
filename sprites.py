import pygame
import random
from config import ANCHO, ALTO, ROJO

# Constantes para ajustar tamaños y velocidades
JUGADOR_ANCHO = 170
JUGADOR_ALTO = 170
PROYECTIL_ANCHO = 50
PROYECTIL_ALTO = 50
ENEMIGO_ANCHO = 180
ENEMIGO_ALTO = 180


# Jugador
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Cargar el sprite sheet
        sprite_sheet = pygame.image.load("sprites/jugador.png").convert_alpha()

        # Definir el primer frame (x, y, ancho, alto)
        frame_rect = pygame.Rect(220, 50, 50, 50)

        # Crear una superficie nueva para el frame específico
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.image.blit(sprite_sheet, (0, 0), frame_rect)

        # Escalar la imagen al tamaño deseado
        self.image = pygame.transform.scale(self.image, (JUGADOR_ANCHO, JUGADOR_ALTO))

        # Ajustar el rectángulo de colisión al nuevo tamaño manualmente
        self.rect = self.image.get_rect()
        self.rect.inflate_ip(
            -140, -80
        )  # Ajusta los valores para reducir el área de colisión

        # Posición inicial del jugador
        self.rect.left = 50
        self.rect.centery = ALTO // 2
        self.velocidad_y = 0

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > ALTO:
            self.rect.bottom = ALTO
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO


# Proyectil
class Proyectil(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Cargar la imagen del sprite del proyectil
        self.image = pygame.image.load("sprites/proyectil.png").convert_alpha()

        # Escalar la imagen del proyectil si es necesario
        self.image = pygame.transform.scale(
            self.image, (PROYECTIL_ANCHO, PROYECTIL_ALTO)
        )

        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.centery = y
        self.velocidad_x = 10
        self.rect.inflate_ip(-35, -35)

    def update(self):
        self.rect.x += self.velocidad_x
        if self.rect.left > ANCHO:
            self.kill()


# Enemigo
class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Cargar las imágenes de los enemigos
        imagenes_enemigos = [
            pygame.image.load("sprites/enemigo1.png").convert_alpha(),
            pygame.image.load("sprites/enemigo2.png").convert_alpha(),
        ]

        # Seleccionar aleatoriamente una imagen de enemigo
        self.image = random.choice(imagenes_enemigos)

        # Escalar la imagen del enemigo al tamaño deseado
        self.image = pygame.transform.scale(self.image, (ENEMIGO_ANCHO, ENEMIGO_ALTO))

        # Rotar la imagen horizontalmente para que mire hacia la izquierda
        self.image = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect()
        self.rect.right = ANCHO
        self.rect.inflate_ip(-100, -30)
        self.rect.y = random.randint(0, ALTO - self.rect.height)
        self.velocidad_x = random.randint(3, 7)

    def update(self):
        self.rect.x -= self.velocidad_x
        if self.rect.left < 0:
            self.kill()
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > ALTO:
            self.rect.bottom = ALTO
        if self.rect.right < 0:  # Si el enemigo sale por el borde izquierdo, se elimina
            self.kill()
