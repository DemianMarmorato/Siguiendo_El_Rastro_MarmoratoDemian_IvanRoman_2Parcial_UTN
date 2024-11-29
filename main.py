import pygame
import random
from config import ANCHO, ALTO, BLANCO, NEGRO, ROJO
from sprites import Jugador, Proyectil, Enemigo
from particulas import Particula
import musica

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Siguiendo el Rastro")

# Cargar y reproducir la música de fondo
musica.cargar_musica(musica.musica_juego)
musica.reproducir_musica()

# Inicializar el puntaje más alto
puntaje_alto = 0


def mostrar_pantalla_inicio(pantalla, fuente):
    """
    Función para mostrar la pantalla de inicio del juego.
    """
    pantalla.fill(NEGRO)
    texto_titulo = fuente.render("Siguiendo el Rastro", True, BLANCO)
    texto_instrucciones = fuente.render(
        "Presiona cualquier tecla para empezar", True, BLANCO
    )
    pantalla.blit(
        texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, ALTO // 2 - 40)
    )
    pantalla.blit(
        texto_instrucciones,
        (ANCHO // 2 - texto_instrucciones.get_width() // 2, ALTO // 2),
    )
    pygame.display.flip()

    esperando_inicio = True
    while esperando_inicio:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                esperando_inicio = False


def mostrar_instrucciones(pantalla, fuente):
    """
    Función para mostrar las instrucciones del juego.
    """
    instrucciones = [
        "Instrucciones:",
        "Usa las flechas arriba y abajo para moverte",
        "Presiona ESPACIO para disparar",
        "Presiona ESC para salir",
    ]
    pantalla.fill(NEGRO)
    for i, linea in enumerate(instrucciones):
        texto = fuente.render(linea, True, BLANCO)
        pantalla.blit(
            texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - 60 + i * 30)
        )
    pygame.display.flip()
    pygame.time.wait(2000)  # Esperar 2 segundos


def mostrar_pantalla_game_over(pantalla, fuente, puntaje, puntaje_alto):
    """
    Función para mostrar la pantalla de Game Over y manejar la lógica de reinicio.
    """
    # Actualizar el puntaje más alto si el puntaje actual es mayor
    if puntaje > puntaje_alto:
        puntaje_alto = puntaje

    # Detener la música actual del juego
    musica.detener_musica()
    # Reproducir la música de Game Over
    musica.cargar_musica(musica.musica_game_over)
    musica.reproducir_musica()

    pantalla.fill(NEGRO)
    texto_game_over = fuente.render(
        f"Juego Terminado. Puntaje: {puntaje}", True, BLANCO
    )
    texto_puntaje_alto = fuente.render(
        f"Puntaje más alto: {puntaje_alto}", True, BLANCO
    )
    texto_rect = texto_game_over.get_rect(center=(ANCHO // 2, ALTO // 2 - 40))
    texto_rect_alto = texto_puntaje_alto.get_rect(center=(ANCHO // 2, ALTO // 2))
    pantalla.blit(texto_game_over, texto_rect)
    pantalla.blit(texto_puntaje_alto, texto_rect_alto)

    texto_reiniciar = fuente.render(
        "Presiona R para reiniciar la partida o ESC para salir", True, ROJO
    )
    texto_rect_reiniciar = texto_reiniciar.get_rect(center=(ANCHO // 2, ALTO // 2 + 40))
    pantalla.blit(texto_reiniciar, texto_rect_reiniciar)

    pygame.display.flip()

    esperando_reiniciar = True
    while esperando_reiniciar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    esperando_reiniciar = False
                    # Volver a la música del juego principal
                    musica.detener_musica()
                    musica.cargar_musica(musica.musica_juego)
                    musica.reproducir_musica()
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
    return puntaje_alto


def main():
    """
    Función principal que inicia y controla el flujo del juego.
    """
    global puntaje_alto
    reloj = pygame.time.Clock()
    puntaje = 0
    fuente = pygame.font.Font(None, 36)

    # Mostrar pantalla de inicio
    mostrar_pantalla_inicio(pantalla, fuente)

    # Mostrar instrucciones
    mostrar_instrucciones(pantalla, fuente)

    # Cargar la imagen del fondo
    fondo = pygame.image.load("sprites/bosque.jpg").convert()
    fondo = pygame.transform.scale(fondo, (1440, 771))  # Tamaño original de la imagen
    fondo_x1 = 0
    fondo_x2 = fondo.get_width()

    # Grupos de sprites
    todos_los_sprites = pygame.sprite.Group()
    proyectiles = pygame.sprite.Group()
    enemigos = pygame.sprite.Group()
    particulas = pygame.sprite.Group()

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
                    musica.reproducir_sonido(musica.sonido_disparo)
                if evento.key == pygame.K_ESCAPE:
                    jugando = False

            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_UP or evento.key == pygame.K_DOWN:
                    jugador.velocidad_y = 0

        # Actualizar
        todos_los_sprites.update()
        particulas.update()

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
        for colision in colisiones:
            musica.reproducir_sonido(
                musica.sonido_muerte_enemigo
            )  # Reproducir el sonido cuando un enemigo es eliminado
            for _ in range(20):  # Generar 20 partículas por enemigo
                particula = Particula(colision.rect.centerx, colision.rect.centery)
                particulas.add(particula)
                todos_los_sprites.add(particula)
        puntaje += len(colisiones)

        # Colisiones jugador-enemigo
        choques = pygame.sprite.spritecollide(jugador, enemigos, False)
        if choques:
            musica.reproducir_sonido(musica.sonido_muerte_jugador)
            puntaje_alto = mostrar_pantalla_game_over(
                pantalla, fuente, puntaje, puntaje_alto
            )
            jugando = True
            main()

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

    pygame.quit()


if __name__ == "__main__":
    main()
