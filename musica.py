import pygame

# Inicializar Pygame y Mixer
pygame.mixer.init()

# Funciones para cargar y reproducir música y sonidos
def cargar_musica(ruta_musica):
    pygame.mixer.music.load(ruta_musica)
    pygame.mixer.music.set_volume(0.5)

def reproducir_musica(loop=-1):
    pygame.mixer.music.play(loop)

def detener_musica():
    pygame.mixer.music.stop()

def cargar_sonido(ruta_sonido):
    return pygame.mixer.Sound(ruta_sonido)

def reproducir_sonido(sonido):
    sonido.play()

# Definición de rutas de música y sonidos
musica_juego = "Siguiendo_El_Rastro_MarmoratoDemian_IvanRoman_2Parcial_UTN/musica/temadeljuego.mp3"
musica_game_over = "Siguiendo_El_Rastro_MarmoratoDemian_IvanRoman_2Parcial_UTN/musica/musicaorientaltriste.mp3"
sonido_muerte_enemigo_ruta = "Siguiendo_El_Rastro_MarmoratoDemian_IvanRoman_2Parcial_UTN/musica/sonidomuerteenemigo.mp3"
sonido_muerte_jugador_ruta = "Siguiendo_El_Rastro_MarmoratoDemian_IvanRoman_2Parcial_UTN/musica/sonidomuertejugador.mp3"
sonido_disparo_ruta = "Siguiendo_El_Rastro_MarmoratoDemian_IvanRoman_2Parcial_UTN/musica/sonidoviento.mp3"

# Cargar sonidos
sonido_muerte_enemigo = cargar_sonido(sonido_muerte_enemigo_ruta)
sonido_muerte_jugador = cargar_sonido(sonido_muerte_jugador_ruta)
sonido_disparo = cargar_sonido(sonido_disparo_ruta)
