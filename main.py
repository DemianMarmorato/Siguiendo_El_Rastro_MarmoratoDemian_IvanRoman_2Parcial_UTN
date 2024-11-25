import pygame
import random
from config import ANCHO, ALTO, BLANCO, NEGRO
from sprites import Jugador, Proyectil, Enemigo

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Siguiendo el Rastro")


def main():
    reloj = pygame.time.Clock()
    puntaje = 0
    fuente = pygame.font.Font(None, 36)

    # Cargar la imagen del fondo
    fondo = pygame.image.load("sprites/bosque.jpg").convert()
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
        pantalla.blit(fondo, (fondo_x1, -150))  # Ajustar -150 para bajar el fondo
        pantalla.blit(fondo, (fondo_x2, -150))  # Ajustar -150 para bajar el fondo
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


if __name__ == "__main__":
    main()
