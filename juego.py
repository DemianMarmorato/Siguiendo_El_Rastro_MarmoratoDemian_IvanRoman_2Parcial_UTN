import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Siguiendo el Rastro")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)


# Jugador
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Cargar el sprite sheet
        sprite_sheet = pygame.image.load("sprites/jugador.png").convert_alpha()

        # Definir el primer frame (x, y, ancho, alto)
        frame_rect = pygame.Rect(
            220, 50, 50, 50
        )  # Cambia estos valores según el frame que quieras usar

        # Crear una superficie nueva para el frame específico
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.image.blit(sprite_sheet, (0, 0), frame_rect)

        # Escalar la imagen al tamaño deseado (por ejemplo, 150x150)
        self.image = pygame.transform.scale(self.image, (150, 150))

        # Ajustar el rectángulo de colisión al nuevo tamaño manualmente
        self.rect = self.image.get_rect()
        self.rect.inflate_ip(
            -50, -50
        )  # Ajusta los valores para reducir el área de colisión

        self.rect.left = 50
        self.rect.centery = ALTO // 2
        self.velocidad_y = 0

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > ALTO:
            self.rect.bottom = ALTO


# Proyectil
class Proyectil(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Cargar la imagen del sprite del proyectil
        self.image = pygame.image.load("sprites/proyectil.png").convert_alpha()

        # Escalar la imagen del proyectil si es necesario
        self.image = pygame.transform.scale(
            self.image, (50, 50)
        )  # Ajusta el tamaño según sea necesario

        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.centery = y
        self.velocidad_x = 10

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

        # Escalar la imagen del enemigo si es necesario
        self.image = pygame.transform.scale(
            self.image, (50, 50)
        )  # Ajusta el tamaño según sea necesario

        self.rect = self.image.get_rect()
        self.rect.right = ANCHO
        self.rect.y = random.randint(0, ALTO - self.rect.height)
        self.velocidad_x = random.randint(3, 7)

    def update(self):
        self.rect.x -= self.velocidad_x
        if self.rect.right < 0:
            self.kill()


# Configuración del juego
def main():
    reloj = pygame.time.Clock()
    puntaje = 0
    fuente = pygame.font.Font(None, 36)

    # Cargar la imagen del fondo
    fondo = pygame.image.load("bosque.png").convert()
    fondo = pygame.transform.scale(fondo, (1440, 771))  # Tamaño original de la imagen
    fondo_x1 = 0
    fondo_x2 = fondo.get_width()

    # Grupos de sprites
    todos_los_sprites = pygame.sprite.Group()
    proyectiles = pygame.sprite.Group()
    enemigos = pygame.sprite.Group()

    # Crear jugador
    jugador = Jugador()
    todos_los_sprites.add(jugador)

    # Bucle principal del juego
    jugando = True
    tiempo_spawn_enemigo = 0
    while jugando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False

            # Controles del jugador
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    jugador.velocidad_y = -8  # Aumentar velocidad en dirección negativa
                if evento.key == pygame.K_DOWN:
                    jugador.velocidad_y = 8  # Aumentar velocidad en dirección positiva
                if evento.key == pygame.K_SPACE:
                    # Crear proyectil
                    proyectil = Proyectil(jugador.rect.right, jugador.rect.centery)
                    todos_los_sprites.add(proyectil)
                    proyectiles.add(proyectil)

            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_UP or evento.key == pygame.K_DOWN:
                    jugador.velocidad_y = 0

        # Actualizar
        todos_los_sprites.update()

        # Desplazar el fondo
        fondo_x1 -= 2  # Ajusta la velocidad del fondo
        fondo_x2 -= 2
        if fondo_x1 <= -fondo.get_width():
            fondo_x1 = fondo.get_width()
        if fondo_x2 <= -fondo.get_width():
            fondo_x2 = fondo.get_width()

        # Spawn de enemigos
        tiempo_spawn_enemigo += 1
        if tiempo_spawn_enemigo > 60:
            enemigo = Enemigo()
            todos_los_sprites.add(enemigo)
            enemigos.add(enemigo)
            tiempo_spawn_enemigo = 0

        # Colisiones proyectil-enemigo
        colisiones = pygame.sprite.groupcollide(proyectiles, enemigos, True, True)
        puntaje += len(colisiones)

        # Colisiones jugador-enemigo
        choques = pygame.sprite.spritecollide(jugador, enemigos, False)
        if choques:
            jugando = False

        # Dibujar
        pantalla.fill(NEGRO)
        pantalla.blit(fondo, (fondo_x1, 50))  # Ajustar 50 para bajar el fondo
        pantalla.blit(fondo, (fondo_x2, 50))  # Ajustar 50 para bajar el fondo
        todos_los_sprites.draw(pantalla)

        # Mostrar puntaje
        texto_puntaje = fuente.render(f"Puntaje: {puntaje}", True, BLANCO)
        pantalla.blit(texto_puntaje, (10, 10))

        pygame.display.flip()
        reloj.tick(60)

    # Pantalla de fin de juego
    pantalla.fill(NEGRO)
    texto_game_over = fuente.render(
        f"Juego Terminado. Puntaje: {puntaje}", True, BLANCO
    )
    texto_rect = texto_game_over.get_rect(center=(ANCHO // 2, ALTO // 2))
    pantalla.blit(texto_game_over, texto_rect)
    pygame.display.flip()

    # Esperar antes de cerrar
    pygame.time.wait(2000)
    pygame.quit()


# Ejecutar el juego
if __name__ == "__main__":
    main()
