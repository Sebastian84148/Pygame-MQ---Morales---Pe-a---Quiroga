import pygame
pygame.init()

#Configuraciones Basicas
pygame.display.set_caption("Juego MQ")
RELOJ = pygame.time.Clock()
FPS = 30
ANCHO = 800
ALTO = 600
VENTANA = (ANCHO,ALTO)
PANTALLA = pygame.display.set_mode(VENTANA)
FUENTE_MENU = pygame.font.SysFont("Archivos/Ribeye-Regular.ttf", 45)
FUENTE_PUNTUACIONES = pygame.font.SysFont("Archivos/Ribeye-Regular.ttf", 35)
ICONO = pygame.image.load("Imagenes/Icono.png")
pygame.display.set_icon(ICONO)

#Colores
NEGRO = (0,0,0)
BLANCO = (255,255,255)
ROJO = (255,0,0)
VERDE = (0,255,0)
AZUL = (0,0,255)
COLOR_BAR_VOLUMEN = (231, 181, 248)
COLOR_BAR_FONDO = (200, 200, 200)

BARRA_VOLUMEN = pygame.Rect(50, 200, 700, 20)

#Imagenes
FONDO_MENU = pygame.image.load("Imagenes/Fondo_Menu.jpg")
FONDO_MENU = pygame.transform.scale(FONDO_MENU, VENTANA)
FONDO_JUEGO = pygame.image.load("Imagenes/Fondo_Juego.jpg")
FONDO_JUEGO = pygame.transform.scale(FONDO_JUEGO, VENTANA)

BOTON_BLANCO = pygame.image.load("Imagenes/Cuadro_imagen.png")
BOTON_GUARDAR = pygame.image.load("Imagenes/Boton_Guardar.png")
BOTON_SALIR = pygame.image.load("Imagenes/Boton_Salir.png")
BOTON_FACIL = pygame.image.load("Imagenes/Boton_Fácil.png")
BOTON_MEDIO = pygame.image.load("Imagenes/Boton_Medio.png")
BOTON_DIFICIL = pygame.image.load("Imagenes/Boton_Dificil.png")

CUADRO_IMAGEN = pygame.image.load("Imagenes/Boton_Jugar.png")
I_R_INCORRECTA = pygame.image.load("Imagenes/Respuesta_incorrecta.png")
I_R_CORRECTA = pygame.image.load("Imagenes/Respuesta_correcta.png")
I_R_DESCARTADA = pygame.image.load("Imagenes/Respuesta_descartada.png")

IMAGENES_BOTONES = {}
IMAGENES_BOTONES["IMAGEN_1"] = pygame.image.load("Imagenes/Boton_Jugar.png")
IMAGENES_BOTONES["IMAGEN_2"] = pygame.image.load("Imagenes/Boton_Opciones.png")
IMAGENES_BOTONES["IMAGEN_3"] = pygame.image.load("Imagenes/Boton_Puntuaciones.png")
IMAGENES_BOTONES["IMAGEN_4"] = pygame.image.load("Imagenes/Boton_Salir.png")
IMAGENES_BOTONES["IMAGEN_5"] = pygame.image.load("Imagenes/Sumar_preguntas.png")

#Sonidos
SONIDO_CLICK = pygame.mixer.Sound("Sonidos/Pop-sound.mp3")
SONIDO_CORRECTO = pygame.mixer.Sound("Sonidos/Correct.wav")
SONIDO_INCORRECTO = pygame.mixer.Sound("Sonidos/Incorrect.wav")
SONIDO_CUENTA_ATRAS = pygame.mixer.Sound("Sonidos/Countdown.wav")

VOLUMEN = 0.5
pygame.mixer.music.set_volume(VOLUMEN)

TEXTO = ""

#Preguntados
PUNTUACION_ACIERTO = 100
PUNTUACION_ERROR = 25

COMODINES = {}
COMODINES["COMODIN_1"] = pygame.image.load("Imagenes/Bomba.png")
COMODINES["COMODIN_2"] = pygame.image.load("Imagenes/X2.png")
COMODINES["COMODIN_3"] = pygame.image.load("Imagenes/Doble_chance.png")
COMODINES["COMODIN_4"] = pygame.image.load("Imagenes/Pasar.png")

COMODINES_UTILIZADOS = {}
COMODINES_UTILIZADOS["COMODIN_1"] = pygame.image.load("Imagenes/Bomba_utilizada.png")
COMODINES_UTILIZADOS["COMODIN_2"] = pygame.image.load("Imagenes/X2_utilizado.png")
COMODINES_UTILIZADOS["COMODIN_3"] = pygame.image.load("Imagenes/Doble_chance_utilizado.png")
COMODINES_UTILIZADOS["COMODIN_4"] = pygame.image.load("Imagenes/Pasar_utilizado.png")

FACIL = {"puntuacion" : 100,"vidas" : 6,"tiempo" : 40, "nombre" : "", "porcentaje_aciertos" : "0","imagen" : BOTON_FACIL}
MEDIO = {"puntuacion" : 50,"vidas" : 3,"tiempo" : 20, "nombre" : "", "porcentaje_aciertos" : "0","imagen" : BOTON_MEDIO}
DIFICIL = {"puntuacion" : 0,"vidas" : 2,"tiempo" : 10, "nombre" : "", "porcentaje_aciertos" : "0","imagen" : BOTON_DIFICIL}
DIFICULTAD_ACTUAL = FACIL

#Integracion 7
PORCENTAJE_ACIERTOS = 0
CANTIDAD_FALLOS = 0
CANTIDAD_ACIERTOS = 0
CANTIDAD_VECEZ_PREGUNTADA = 0