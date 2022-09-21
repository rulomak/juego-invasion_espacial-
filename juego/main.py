import pygame
import random
import math
from pygame import mixer


pygame.init()   # inicializa pygame
# creo la pantala
pantalla = pygame.display.set_mode((800, 600))

# Titulo e icono
pygame.display.set_caption("Invasion Espacial")
# iconos bajados de flaticon.es
icono = pygame.image.load("ovni.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load('fondo.jpg')
# agregar musica
mixer.music.load('MusicaFondo.mp3')
mixer.music.play(-1)

# jugador + posicion inicial
img_jugador = pygame.image.load("cohete.png")
jugador_x = 368              # ancho en pix
jugador_Y = 520              # alto
jugador_x_cambio = 0

# enemigo - variables
img_enemigo = []
enemigo_x = []
enemigo_Y = []
enemigo_x_cambio = []
enemigo_Y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):   # se generan enemigos dentro de la listas
    img_enemigo.append(pygame.image.load("enemigo.png"))
    enemigo_x.append(random.randint(0,736))     # rango aleatorio de movimiento
    enemigo_Y.append(random.randint(50,200))    # alto
    enemigo_x_cambio.append(0.6)
    enemigo_Y_cambio.append(50)

# variables de bala
img_bala = pygame.image.load("bala.png")
bala_x = 0
bala_Y = 560
bala_x_cambio = 0
bala_Y_cambio = 1
bala_visible = False

# puntaje
puntaje = 0
fuente = pygame.font.Font('freesansbold.ttf',32)
texto_x = 10
texto_y = 10

# texto final de juego
fuente_final = pygame.font.Font('freesansbold.ttf',42)
def texto_final():
    mi_fuente_final = fuente_final.render("JUEGO TERMINADO", True, (255,255,255))
    pantalla.blit(mi_fuente_final, (200,200))

# funcion mostrar puntaje
def mostrar_puntaje(x,y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255,255,255))
    pantalla.blit(texto, (x, y))

# funcion jugados
def jugador(x,y):
    pantalla.blit(img_jugador,(x,y))  # .blit arrojar o insertar
# funcion enemigo
def enemigo(x,y,ene):
    pantalla.blit(img_enemigo[ene], (x, y))

# funcion bala
def disparar_bala(x,y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))  # se le agrega pix, para que salga del centro de la nave

# funcion detectar coliciones
def hay_colision(x_1,y_1,x_2,y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1, 2))  # calcula la distancia entre los 2 objetos
    if distancia < 22:
        return True
    else:
        False

# loop del juego
se_ejecuta = True
while se_ejecuta:                # mientra que se ejecuta sea True
    pantalla.blit(fondo,(0,0))   # imagen de fondo
     # iterar eventos
    for evento in pygame.event.get():
        # evento cerrar
        if evento.type == pygame.QUIT:
            se_ejecuta = False             # se_ejecuta = a False y se cierra ventana
        # evento presionar teclas
        if evento.type == pygame.KEYDOWN:     # tecla presionada (cualquira)
            if evento.key == pygame.K_LEFT:   # tecla izq
                jugador_x_cambio = -0.6
            if evento.key == pygame.K_RIGHT:  # igual a tecla der
                jugador_x_cambio = 0.6
            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound('disparo.mp3')

                if bala_visible == False:   # solamente se dispara una vez y no cambiara la pasision cada ves que apretemos space
                    bala_x = jugador_x      # esto hace que la bala mantenga la posision de disparo y no corra junto al jugador
                    disparar_bala(bala_x,bala_Y)
                    sonido_bala.play()
            # evento soltar tecla
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0
        # modificar la ubicacion J
    jugador_x += jugador_x_cambio       # jugadorX (ancho) va a ser igual que jugadorX cambiao que estara cambiando
    # mantener dentro de margenes Jugador
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

        # modificar la ubicacion Enemigo
    for e in range(cantidad_enemigos):
        # fin del juego
        if enemigo_Y[e] > 465:
            for k in range(cantidad_enemigos):
                enemigo_Y[k] = 1000
            texto_final()
            break

        enemigo_x[e] += enemigo_x_cambio[e]


          # mantener dentro de margenes Enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 0.5   # esto deberia hacer que cuando toque el borde cambie el movimiento hacia el otro lado
            enemigo_Y[e] += enemigo_Y_cambio[e]   # con esto bajaria 50 pip
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -0.5  # esto deberia hacer que cuando toque el borde cambie el movimiento hacia el otro lado
            enemigo_Y[e] += enemigo_Y_cambio[e]

        # colision
        colision = hay_colision(enemigo_x[e], enemigo_Y[e], bala_x, bala_Y)
        if colision:
            sonido_colision = mixer.Sound('golpe.mp3')
            sonido_colision.play()
            bala_Y = 500
            bala_visible = False
            puntaje += 1
            enemigo_x[e] = random.randint(0, 736)
            enemigo_Y[e] = random.randint(50, 200)
        enemigo(enemigo_x[e], enemigo_Y[e],e)

    # movimiento bala
    if bala_Y <= -64:
        bala_Y = 500
        bala_visible = False     # si la bala sale de la pantalla, se resetea y desaparece
    if bala_visible == True:
        disparar_bala(bala_x, bala_Y)
        bala_Y -= bala_Y_cambio


    jugador(jugador_x, jugador_Y)

    mostrar_puntaje(texto_x, texto_y)

    pygame.display.update()  # actualizar display



