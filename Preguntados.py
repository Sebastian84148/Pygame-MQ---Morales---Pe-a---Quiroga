import pygame
from Constantes import *
from Funciones import *

pygame.init()

#Eventos Personalizados
evento_tiempo_1s = pygame.USEREVENT
pygame.time.set_timer(evento_tiempo_1s,1000)
evento_tiempo_5s = pygame.USEREVENT + 1
pygame.time.set_timer(evento_tiempo_5s,5000)

#Pregunta
cuadro_pregunta = crear_boton((500,125), BOTON_BLANCO)

#Respuestas
cuadro_respuestas = crear_lista_botones((250,75), 4, BOTON_BLANCO)

#Comodines
lista_comodines = []
for i in range(4):
    comodin = {}
    comodin["superficie"] = COMODINES[f"COMODIN_{i + 1}"]
    comodin["superficie"] = pygame.transform.scale(comodin["superficie"], (100,50))
    comodin["rectangulo"] = comodin["superficie"].get_rect()
    lista_comodines.append(comodin)

indice = 0
respuestas_correctas = 0
bandera_respuesta = False
bandera_comodin = False
bandera_comodin_bomba = False
bandera_comodin_x2 = False
bandera_comodin_repetir = False
bandera_comodin_pasar = False

def mostrar_preguntados(pantalla:pygame.Surface, cola_eventos:list[pygame.event.Event], datos_juego:dict, lista_preguntas:list) -> str:
    global indice
    global respuestas_correctas
    global bandera_respuesta
    global bandera_comodin
    global bandera_comodin_bomba
    global bandera_comodin_x2
    global bandera_comodin_repetir
    global bandera_comodin_pasar

    retorno = "juego"

    if bandera_respuesta:
        pygame.time.delay(500)
        if datos_juego["vidas"] == 0:
            guardar_csv("Preguntas_integracion_7.csv", lista_preguntas, False)
            retorno = "terminado"

        cuadro_pregunta["superficie"] = BOTON_BLANCO
        cuadro_pregunta["superficie"] = pygame.transform.scale(cuadro_pregunta["superficie"], (500,125))
        for i in range(4):
            cuadro_respuestas[i]["superficie"] = BOTON_BLANCO
            cuadro_respuestas[i]["superficie"] = pygame.transform.scale(cuadro_respuestas[i]["superficie"], (250,75))

            lista_comodines[i]["superficie"] = COMODINES[f"COMODIN_{i + 1}"]
            lista_comodines[i]["superficie"] = pygame.transform.scale(lista_comodines[i]["superficie"], (100,50))
        bandera_respuesta = False

    pregunta_actual = lista_preguntas[indice]

    #Eventos
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"

        if evento.type == evento_tiempo_1s:
            datos_juego["tiempo"] -= 1
            if datos_juego["tiempo"] <= 5:
                SONIDO_CUENTA_ATRAS.play()
                if datos_juego["tiempo"] == 0:
                    datos_juego["vidas"] -= 1

        if evento.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(lista_comodines)):
                if lista_comodines[i]["rectangulo"].collidepoint(evento.pos):
                        comodin_seleccionado = i + 1
                        if comodin_seleccionado == 1 and bandera_comodin_bomba == False:
                            lista_comodines[i]["superficie"] = COMODINES_UTILIZADOS[f"COMODIN_{i + 1}"]
                            lista_comodines[i]["superficie"] = pygame.transform.scale(lista_comodines[i]["superficie"], (100,50))
                            indices_cuadros_descartados = crear_comodin_bomba(pregunta_actual)
                            for indice_cuadro in indices_cuadros_descartados:
                                cuadro_respuestas[indice_cuadro - 1]["superficie"] = I_R_DESCARTADA
                                cuadro_respuestas[indice_cuadro - 1]["superficie"] = pygame.transform.scale(cuadro_respuestas[indice_cuadro - 1]["superficie"], (250,75))
                            bandera_comodin_bomba = True
                        elif comodin_seleccionado == 2 and bandera_comodin_x2 == False:
                            lista_comodines[i]["superficie"] = COMODINES_UTILIZADOS[f"COMODIN_{2}"]
                            lista_comodines[i]["superficie"] = pygame.transform.scale(lista_comodines[i]["superficie"], (100,50))
                            bandera_comodin_x2 = True
                        # elif comodin_seleccionado == 3 and bandera_comodin_repetir == False:
                        #     pass
                        elif comodin_seleccionado == 4 and bandera_comodin_pasar == False:
                            lista_comodines[i]["superficie"] = COMODINES_UTILIZADOS[f"COMODIN_{3}"]
                            lista_comodines[i]["superficie"] = pygame.transform.scale(lista_comodines[i]["superficie"], (100,50))
                            indice = crear_comodin_pasar(indice, lista_preguntas)
                            bandera_comodin_pasar = True
            for i in range(len(cuadro_respuestas)):
                if cuadro_respuestas[i]["rectangulo"].collidepoint(evento.pos):
                    respuesta_jugador = i + 1
                    if verificar_respuesta(datos_juego, pregunta_actual, respuesta_jugador, lista_preguntas[indice], bandera_comodin_x2) == True:
                        cuadro_respuestas[i]["superficie"] = I_R_CORRECTA
                        cuadro_respuestas[i]["superficie"] = pygame.transform.scale(cuadro_respuestas[i]["superficie"], (250,75))
                        respuestas_correctas += 1
                        if respuestas_correctas == 5:
                            respuestas_correctas = 0
                            datos_juego["vidas"] += 1
                        SONIDO_CORRECTO.play()
                    else:
                        cuadro_respuestas[i]["superficie"] = I_R_INCORRECTA
                        cuadro_respuestas[i]["superficie"] = pygame.transform.scale(cuadro_respuestas[i]["superficie"], (250,75))
                        SONIDO_INCORRECTO.play()
                    bandera_respuesta = True

                    if indice == len(lista_preguntas):
                        indice = 0
                        mezclar_lista(lista_preguntas)
                    indice += 1

    #Actualizar juego

    #Dibujar pantalla y superficies
    #Texto
    mostrar_texto(cuadro_pregunta["superficie"],f"{pregunta_actual["pregunta"]}",(15,20),FUENTE_MENU,NEGRO)

    for i in range(4):
        mostrar_texto(cuadro_respuestas[i]["superficie"],f"{pregunta_actual[f"respuesta_{i + 1}"]}",(35,15),FUENTE_MENU,NEGRO)
    
    #Superficie
    pantalla.blit(FONDO_JUEGO,(0,0))
    pantalla.blit(cuadro_pregunta["superficie"],(150,100))

    cuadro_respuestas[0]["rectangulo"] = pantalla.blit(cuadro_respuestas[0]["superficie"],(125,275))
    cuadro_respuestas[1]["rectangulo"] = pantalla.blit(cuadro_respuestas[1]["superficie"],(425,275))
    cuadro_respuestas[2]["rectangulo"] = pantalla.blit(cuadro_respuestas[2]["superficie"],(125,400))
    cuadro_respuestas[3]["rectangulo"] = pantalla.blit(cuadro_respuestas[3]["superficie"],(425,400))

    lista_comodines[0]["rectangulo"] = pantalla.blit(lista_comodines[0]["superficie"],(175,550))
    lista_comodines[1]["rectangulo"] = pantalla.blit(lista_comodines[1]["superficie"],(300,550))
    lista_comodines[2]["rectangulo"] = pantalla.blit(lista_comodines[2]["superficie"],(425,550))
    lista_comodines[3]["rectangulo"] = pantalla.blit(lista_comodines[3]["superficie"],(550,550))

    mostrar_texto(pantalla,f"Vidas: {datos_juego['vidas']}",(10,10),FUENTE_MENU,NEGRO)
    mostrar_texto(pantalla,f"Puntuacion: {datos_juego['puntuacion']}",(10,40),FUENTE_MENU,NEGRO)
    mostrar_texto(pantalla,f"Tiempo: {datos_juego["tiempo"]}",(665,10),FUENTE_MENU,NEGRO)

    return retorno