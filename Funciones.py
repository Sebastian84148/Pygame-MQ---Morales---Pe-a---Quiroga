import pygame
import random
import json
import os
from datetime import datetime
from Constantes import *

lista_botones = []
for i in range(5):
    boton = {}
    boton["superficie"] = IMAGENES_BOTONES[f"IMAGEN_{i + 1}"]
    boton["superficie"] = pygame.transform.scale(boton["superficie"], (250,100))
    boton["rectangulo"] = boton["superficie"].get_rect()
    lista_botones.append(boton)

def mostrar_menu(pantalla:pygame.Surface, cola_eventos:list[pygame.event.Event]) -> str:
    #Eventos
    retorno = "menu"
    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(lista_botones)):
                if lista_botones[i]["rectangulo"].collidepoint(evento.pos):
                    boton_seleccionado = i + 1
                    if boton_seleccionado == 1:
                        SONIDO_CLICK.play()
                        retorno = "juego"
                    if boton_seleccionado == 2:
                        SONIDO_CLICK.play()
                        retorno = "opciones"
                    if boton_seleccionado == 3:
                        SONIDO_CLICK.play()
                        retorno = "puntuaciones"
                    if boton_seleccionado == 4:
                        SONIDO_CLICK.play()
                        retorno = "salir"
                    if boton_seleccionado == 5:
                        SONIDO_CLICK.play()
                        preguntas_adicionales = []
                        #Integracion 8
                        leer_csv("Preguntas_adicionales.csv",preguntas_adicionales,True)
                        actualizar_csv("Preguntas_integracion_7.csv", preguntas_adicionales, False)
        if evento.type == pygame.QUIT:
            retorno = "salir"

    #Acutalizar juego

    #Dibujar pantalla y superficies
    pantalla.blit(FONDO_MENU,(0,0))

    lista_botones[0]["rectangulo"] = pantalla.blit(lista_botones[0]["superficie"],(125,125))
    lista_botones[1]["rectangulo"] = pantalla.blit(lista_botones[1]["superficie"],(425,125))
    lista_botones[2]["rectangulo"] = pantalla.blit(lista_botones[2]["superficie"],(125,250))
    lista_botones[3]["rectangulo"] = pantalla.blit(lista_botones[3]["superficie"],(425,250))
    lista_botones[4]["rectangulo"] = pantalla.blit(lista_botones[4]["superficie"],(125,375))

    return retorno

def mostrar_opciones(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], DIFICULTAD_ACTUAL: dict) -> tuple[str, dict]:
    #Eventos
    global VOLUMEN
    global TEXTO
    retorno = "opciones"

    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if BARRA_VOLUMEN.collidepoint(evento.pos):
                    VOLUMEN = (evento.pos[0] - BARRA_VOLUMEN.x) / BARRA_VOLUMEN.width
                    VOLUMEN = max(0, min(VOLUMEN, 1))
                    pygame.mixer.music.set_volume(VOLUMEN)
                if lista_botones[3]["rectangulo"].collidepoint(evento.pos):
                    SONIDO_CLICK.play()
                    retorno = "menu"
                elif pygame.Rect(35, 350, 270, 75).collidepoint(evento.pos):
                    TEXTO = "Modo Fácil seleccionado"
                    SONIDO_CLICK.play()
                    DIFICULTAD_ACTUAL = FACIL
                elif pygame.Rect(290, 350, 270, 75).collidepoint(evento.pos):
                    TEXTO = "Modo Medio seleccionado"
                    SONIDO_CLICK.play()
                    DIFICULTAD_ACTUAL = MEDIO
                elif pygame.Rect(545, 350, 270, 75).collidepoint(evento.pos):
                    TEXTO = "Modo Difícil seleccionado"
                    SONIDO_CLICK.play()
                    DIFICULTAD_ACTUAL = DIFICIL
    #Acutalizar juego
    #Dibujar pantalla y superficies
    pantalla.blit(FONDO_MENU,(0,0))

    pygame.draw.rect(PANTALLA, COLOR_BAR_FONDO, BARRA_VOLUMEN)
    pygame.draw.rect(PANTALLA, COLOR_BAR_VOLUMEN, (BARRA_VOLUMEN.x, BARRA_VOLUMEN.y, VOLUMEN * BARRA_VOLUMEN.width, BARRA_VOLUMEN.height))


    lista_botones[3]["rectangulo"] = pantalla.blit(lista_botones[3]["superficie"],(270,470))
    PANTALLA.blit(pygame.transform.scale(BOTON_FACIL, (220, 75)), (35, 350))
    PANTALLA.blit(pygame.transform.scale(BOTON_MEDIO, (220, 75)), (290, 350))
    PANTALLA.blit(pygame.transform.scale(BOTON_DIFICIL, (220, 75)), (545, 350)) 

    superficie_texto = FUENTE_MENU.render(TEXTO, True, NEGRO) #Ajustes
    texto_volumen = FUENTE_MENU.render(f"Volumen: {int(VOLUMEN * 100)}%", True, NEGRO)
    pantalla.blit(texto_volumen, (BARRA_VOLUMEN.x + 10, BARRA_VOLUMEN.y - 40))
    pantalla.blit(superficie_texto, (200, 100))  # Coordenadas
    return retorno, DIFICULTAD_ACTUAL

def ordenar_mayor_menor(lista:list) -> list:
    for i in range(len(lista) - 1):
        for j in range(i + 1, len(lista)):
            if lista[i]["puntuacion"] < lista[j]["puntuacion"]:
                aux = lista[i]
                lista[i] = lista[j]
                lista[j] = aux

    return lista

def crear_filas_vacias(top_10:list, filas_vacias:int) -> list:
    for i in range(filas_vacias):
        diccionario = {}
        diccionario["nombre"] = "-"
        diccionario["puntuacion"] = 0
        diccionario["fecha"] = "-"
        top_10.append(diccionario)

def mostrar_datos_puntuaciones(pantalla:pygame.Surface, top_10:list, posicion_y:int, separacion:int) -> None:
    espacio = 0
    for i in range(len(top_10)):
        if top_10[i]["fecha"] == "-":
            espacio = 75
        mostrar_texto(pantalla, f"{i + 1}", (75, posicion_y + separacion), FUENTE_PUNTUACIONES, NEGRO)
        mostrar_texto(pantalla, f"{top_10[i]["nombre"]}", (200  + espacio,posicion_y + separacion), FUENTE_PUNTUACIONES, NEGRO)
        mostrar_texto(pantalla, f"{top_10[i]["puntuacion"]}", (475, posicion_y + separacion), FUENTE_PUNTUACIONES, NEGRO)
        mostrar_texto(pantalla, f"{top_10[i]["fecha"]}", (610  + espacio, posicion_y + separacion), FUENTE_PUNTUACIONES, NEGRO)
        separacion += 40

def mostrar_texto(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, False, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

def verificar_respuesta(datos_juego:dict, pregunta_actual:dict, respuesta:int, diccionario:dict, comodin_x2:bool) -> bool:
    datos_juego["tiempo"] = 20
    diccionario["cantidad_veces_preguntada"] += 1
    if respuesta == pregunta_actual["respuesta_correcta"]:
        if comodin_x2:
            datos_juego["puntuacion"] += PUNTUACION_ACIERTO
        datos_juego["puntuacion"] += PUNTUACION_ACIERTO
        diccionario["cantidad_aciertos"] += 1
        retorno = True
    else:
        if datos_juego["puntuacion"] > PUNTUACION_ERROR:
            datos_juego["puntuacion"] -= PUNTUACION_ERROR

        datos_juego["vidas"] -= 1
        diccionario["cantidad_fallos"] += 1
        retorno = False

    diccionario["porcentaje_aciertos"] = (diccionario["cantidad_aciertos"] / diccionario["cantidad_veces_preguntada"]) * 100
    
    return retorno

def crear_boton(escala:tuple, imagen) -> dict:
    diccionario = {}
    diccionario["superficie"] = imagen
    diccionario["superficie"] = pygame.transform.scale(diccionario["superficie"], escala)
    diccionario["rectangulo"] = diccionario["superficie"].get_rect()

    return diccionario

def crear_lista_botones(escala:tuple, cantidad_botones:int, imagen) -> list:
    lista = []
    for i in range(cantidad_botones):
        boton = crear_boton(escala, imagen)
        lista.append(boton)

    return lista

def crear_lista_datos(lista:list, datos_juego:dict) -> list:
    diccionario = {}
    diccionario["nombre"] = datos_juego["nombre"]
    diccionario["puntuacion"] = datos_juego["puntuacion"]
    diccionario["fecha"] = str(datetime.now().date())
    lista.append(diccionario)
    return lista

def mezclar_lista(lista_preguntas:list) -> None:
    random.shuffle(lista_preguntas)

def crear_comodin_bomba(pregunta_actual:dict) -> list:
    lista = []
    while len(lista) < 2:
        numero = random.randint(1,4)
        if numero != pregunta_actual["respuesta_correcta"]:
            if lista == []:
                lista.append(numero)
            elif numero != lista[0]:
                lista.append(numero)

    return lista

def crear_comodin_pasar(indice: int, lista_preguntas: list) -> bool:
    # Avanzar al siguiente índice, reiniciar si es la última pregunta
    retorno = False
    indice += 1
    if indice >= len(lista_preguntas):
        indice = 0
        retorno = True  # Reinicia el índice si llega al final de la lista
    return retorno

#CSV
def crear_diccionario(lista_valores:list, integracion_7:bool) -> dict:
    diccionario = {}
    diccionario["pregunta"] = lista_valores[0]
    for i in range(1,5):
        diccionario[f"respuesta_{i}"] = lista_valores[i]
    diccionario["respuesta_correcta"] = int(lista_valores[5])
    if integracion_7:
        diccionario["porcentaje_aciertos"] = float(lista_valores[6])
        diccionario["cantidad_fallos"] = int(lista_valores[7])
        diccionario["cantidad_aciertos"] = int(lista_valores[8])
        diccionario["cantidad_veces_preguntada"] = int(lista_valores[9])

    return diccionario

def leer_csv(nombre_archivo:str, lista:list, integracion_7:bool) -> bool:
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, "r",  encoding="utf-8") as archivo:
            archivo.readline()
            for linea in archivo:
                linea_aux = linea.replace("\n","")
                lista_valores = linea_aux.split(",")
            
                diccionario_aux = crear_diccionario(lista_valores, integracion_7)
                lista.append(diccionario_aux)
        retorno = True
    else:
        retorno = False

    return retorno

def crear_cabecera(diccionario:dict,separador:str, integracion_7:bool) -> str:
    lista_claves = list(diccionario.keys())
    if integracion_7:
        lista_claves_integracion_7 = ["porcentaje_aciertos","cantidad_fallos","cantidad_aciertos","cantidad_veces_preguntada"]
        lista_claves.extend(lista_claves_integracion_7)
    cabecera = separador.join(lista_claves)

    return cabecera

def crear_datos_csv(diccionario:dict, separador:str, integracion_7:bool) -> str:
    lista_valores = list(diccionario.values())
    if integracion_7:
        lista_valores_integracion_7 = [PORCENTAJE_ACIERTOS,CANTIDAD_FALLOS,CANTIDAD_ACIERTOS,CANTIDAD_VECEZ_PREGUNTADA]
        lista_valores.extend(lista_valores_integracion_7)
    for i in range(len(lista_valores)):
        lista_valores[i] = str(lista_valores[i])
    
    datos = separador.join(lista_valores)

    return datos

def guardar_csv(nombre_archivo:str, lista:list, integracion_7:bool) -> bool:
    if type(lista) == list and len(lista) > 0:
        cabecera = crear_cabecera(lista[0], ",", integracion_7)
        with open(nombre_archivo, "w", encoding='utf-8') as archivo:
            archivo.write(cabecera)
            for elemento in lista:
                linea = crear_datos_csv(elemento, ",", integracion_7)
                # linea = linea.encode('utf-8', errors='replace').decode('utf-8')
                archivo.write("\n" + linea)
        retorno = True
    else:
        retorno = False

    return retorno

def actualizar_csv(nombre_archivo:str, lista:list, integracion_7:bool) -> bool:
    if type(lista) == list and len(lista) > 0:
        with open(nombre_archivo, "a", encoding='utf-8') as archivo:
            for elemento in lista:
                linea = crear_datos_csv(elemento, ",", integracion_7)
                # linea = linea.encode('utf-8', errors='replace').decode('utf-8')
                archivo.write("\n" + linea)
        retorno = True
    else:
        retorno = False

    return retorno

#JSON
def generar_json(nombre_archivo:str, lista:list) -> bool:
    if type(lista) == list and len(lista) > 0:
        with open(nombre_archivo,"w") as archivo:
            json.dump(lista,archivo,indent=4)
        retorno = True
    else:
        retorno = False

    return retorno

def leer_json(nombre_archivo:str) -> list:
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, "r") as archivo:
            retorno = json.load(archivo)
    else:
        retorno = []

    return retorno