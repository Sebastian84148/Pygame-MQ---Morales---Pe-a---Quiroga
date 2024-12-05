import pygame
from Constantes import *
from Preguntados import *
from Terminado import *
from Puntuaciones import *
from Funciones import *

#Inicializar Pygame
pygame.init()

corriendo = True

ventana_actual = "menu"
lista_preguntas = []

if os.path.exists("Preguntas_integracion_7.csv"):
    leer_csv("Preguntas_integracion_7.csv", lista_preguntas, True)
else:
    leer_csv("Preguntas.csv", lista_preguntas, False)
    #Integracion 7
    guardar_csv("Preguntas_integracion_7.csv", lista_preguntas, True)
    lista_preguntas = []
    leer_csv("Preguntas_integracion_7.csv", lista_preguntas, True)

bandera_mezclar = False
bandera_musica = False

while corriendo:
    #FPS
    RELOJ.tick(FPS)

    #Eventos
    cola_eventos = pygame.event.get()

    #Ventanas
    if ventana_actual == "menu":
        ventana_actual = mostrar_menu(PANTALLA, cola_eventos)
    elif ventana_actual == "juego":
        if bandera_mezclar == False:
            mezclar_lista(lista_preguntas)
            bandera_mezclar = True
        if bandera_musica == False:
            pygame.mixer.music.load("Sonidos/musica.mp3")
            pygame.mixer.music.set_volume(VOLUMEN)
            pygame.mixer.music.play(-1)
            bandera_musica = True
        ventana_actual = mostrar_preguntados(PANTALLA, cola_eventos, DIFICULTAD_ACTUAL, lista_preguntas)
    elif ventana_actual == "opciones":
        ventana_actual, DIFICULTAD_ACTUAL = mostrar_opciones(PANTALLA, cola_eventos, DIFICULTAD_ACTUAL)
    elif ventana_actual == "puntuaciones":
        ventana_actual = mostrar_puntuaciones(PANTALLA, cola_eventos)
    elif ventana_actual == "terminado":
        if bandera_musica == True:
            pygame.mixer.music.stop()
            bandera_musica = False
        ventana_actual = mostrar_juego_terminado(PANTALLA, cola_eventos, DIFICULTAD_ACTUAL)
    elif ventana_actual == "salir":
        corriendo = False

    pygame.display.flip()

pygame.quit()