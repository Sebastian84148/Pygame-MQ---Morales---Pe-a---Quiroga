import pygame
from Constantes import *
from Funciones import *

pygame.init()

cuadro_texto = crear_boton((350, 70), BOTON_BLANCO)
boton_confirmar = crear_boton((150,50), BOTON_GUARDAR)
boton_atras = crear_boton((80,50), BOTON_SALIR)

nombre = ""
bandera_confirmar = False

def mostrar_juego_terminado(pantalla:pygame.Surface, cola_eventos:list[pygame.event.Event], datos_juego:dict) -> str:
    global nombre
    global bandera_confirmar
    retorno = "terminado"

    #Eventos
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            if bandera_confirmar:
                retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_confirmar["rectangulo"].collidepoint(evento.pos):
                if bandera_confirmar == False and nombre != "":
                    datos_juego["nombre"] = nombre
                    SONIDO_CLICK.play()
                    if leer_json("partidas.json") == []:
                        lista_puntuaciones = []
                    else:
                        lista_puntuaciones = leer_json("partidas.json")
                    crear_lista_datos(lista_puntuaciones, datos_juego)
                    generar_json("partidas.json", lista_puntuaciones)
                    bandera_confirmar = True
            if boton_atras["rectangulo"].collidepoint(evento.pos):
                if datos_juego["nombre"] != "":
                    SONIDO_CLICK.play()
                    retorno = "menu"
        elif evento.type == pygame.KEYDOWN:
            block_mayus = pygame.key.get_mods() and pygame.KMOD_CAPS
            letra_presionada = pygame.key.name(evento.key)

            if bandera_confirmar == False:
                if letra_presionada == "space":
                    nombre += " "
                if letra_presionada == "backspace" and len(nombre) > 0:
                    nombre = nombre[0:-1]
                    cuadro_texto["superficie"] = BOTON_BLANCO
                    cuadro_texto["superficie"] = pygame.transform.scale(cuadro_texto["superficie"], (350,70))

                if len(letra_presionada) == 1 and (letra_presionada.isalnum() and len(nombre) < 13):
                    if block_mayus != 0:
                        nombre += letra_presionada.upper()
                    else:
                        nombre += letra_presionada

    #Dibujar pantalla, superficies y texto
    mostrar_texto(cuadro_texto["superficie"], nombre, (10,20), FUENTE_MENU, NEGRO)

    pantalla.blit(FONDO_JUEGO,(0,0))

    cuadro_texto["rectangulo"] = pantalla.blit(cuadro_texto["superficie"], (225,180))
    boton_confirmar["rectangulo"] = pantalla.blit(boton_confirmar["superficie"], (325,280))
    boton_atras["rectangulo"] = pantalla.blit(boton_atras["superficie"], (10,10))

    mostrar_texto(pantalla, f"Te quedaste sin vidas... Obtuviste: {datos_juego["puntuacion"]} puntos.", (100,100), FUENTE_MENU, NEGRO)
    mostrar_texto(pantalla, "Ingrese su nombre de usuario", (150,135), FUENTE_MENU, NEGRO)
    if bandera_confirmar:
        mostrar_texto(pantalla, f"El usuario {datos_juego['nombre']} fue guardado correctamente", (150,350), FUENTE_MENU, NEGRO)

    return retorno