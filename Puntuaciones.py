import pygame
from Constantes import *
from Funciones import *

pygame.init()

boton_atras = crear_boton((80,50), BOTON_SALIR)

bandera_json = True

def mostrar_puntuaciones(pantalla:pygame.Surface, cola_eventos:list[pygame.event.Event]) -> str:
    global bandera_json
    global claves
    global top_10
    retorno = "puntuaciones"

    if bandera_json:
        top_10 = leer_json("partidas.json")
        ordenar_mayor_menor(top_10)
        bandera_json = False

    #Eventos
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_atras["rectangulo"].collidepoint(evento.pos):
                SONIDO_CLICK.play()
                retorno = "menu"

    pantalla.blit(FONDO_JUEGO,(0,0))

    boton_atras["rectangulo"] = pantalla.blit(boton_atras["superficie"], (10,10))
    mostrar_texto(pantalla, "TOP 10 Puntuaciones", (250,80), FUENTE_MENU, NEGRO)
    if top_10 == []:
        crear_filas_vacias(top_10, 10)
    else:
        largo_top_10 = len(top_10)
        if largo_top_10 < 10:
            crear_filas_vacias(top_10, 10 - largo_top_10)

        claves = list(top_10[0].keys())
        mostrar_texto(pantalla, "Posicion", (30,150), FUENTE_PUNTUACIONES, NEGRO)
        mostrar_texto(pantalla, f"{claves[0]}".capitalize(), (225,150), FUENTE_PUNTUACIONES, NEGRO)
        mostrar_texto(pantalla, f"{claves[1]}".capitalize(), (420,150), FUENTE_PUNTUACIONES, NEGRO)
        mostrar_texto(pantalla, f"{claves[2]}".capitalize(), (640,150), FUENTE_PUNTUACIONES, NEGRO)

        mostrar_datos_puntuaciones(pantalla, top_10, 190, 0)

    return retorno