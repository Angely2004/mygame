import pygame
import random
import math
pygame.init

#configura la ventana
ANCHO, ALTO = 800,600
screen = pygame.display.set_mode((ANCHO,ALTO)) #creamos la ventana con el tamaño definido 
pygame.display.set_caption("my game")

#fondo pantalla
fondo = pygame.image.load("imagenes/fondo1.jpg")#cargamos imagen desde el archivo
fondo = pygame.transform.scale(fondo,(ANCHO,ALTO))

#player
playerImg= pygame.image.load('imagenes/drago.png')
playerX = 400
playerY = 450
playerX_change = 0

#fuego
fuegoImg= pygame.image.load('imagenes/fuego.png')
fuegoX = 0
fuegoY = 450
fuegoX_change = 0
fuego_change = 0.5
fuego_state = "ready"

#enemy
enemyImg= pygame.image.load('imagenes/cazador.png')
enemyX = random.randint (0,701) #coloca valores aleatorios
enemyY = random.randint (50,150)
enemyX_change = 20
enemyY_change = 40

#funcion para dibujar el juegador
def player(x,y):
    screen.blit(playerImg,(x,y))

#funcion para dibujar el enemigo
def enemy(x,y):
    screen.blit(enemyImg,(x,y))

# funcion fuego
def fire_fuego(x,y):
    global fuego_state
    fuego_state = "fire"
    screen.blit(fuegoImg,(x +90 ,y +1 )) #pixeles para que el fuego salga del dragon 

# funcion para colisionar
def colisiones(enemyX,enemyY,fuegoX,fuegoY):
    distance = math.sqrt((math.pow(enemyX-fuegoX,2))+(math.pow(enemyY-fuegoY,2)))
    if distance < 27:
        return True
    else:
        return False

score = 0


running = True
while running:

    screen.blit(fondo,(0,0))

    for evento in pygame.event.get() : #captura eventos (teclado,raton)
        if evento.type == pygame.QUIT:
            running = False #sale del bucle

        
        if evento.type == pygame.KEYDOWN:

            # mover el juegador con teclas hacia la izquierda
            if evento.key == pygame.K_LEFT:
                playerX_change = -0.3
            #Mover con tecla hacia la derecha
            if evento.key == pygame.K_RIGHT:
                playerX_change = 0.3
            #para disparar con espacio
            if evento.key == pygame.K_SPACE:
                if fuego_state == "ready":
                    fuegoX = playerX
                    fire_fuego(playerX,fuegoY)

        # para reconocer un no se esta moviendo
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                playerX_change = 0
            


    playerX+= playerX_change

    # para que no se desborde en las paredes de la ventana
    if playerX <=0:
        playerX = 0
    elif playerX >=550: #porque quitamos en tamaño del jugador
        playerX = 550

    enemyX += enemyX_change
    # para que no se desborde en las paredes de la ventana
    if enemyX <=0:
        enemyX_change = 0.3
        enemyY += enemyY_change # para moverse hacia abajo
    elif enemyX >=701: #porque quitamos en tamaño del jugador
        enemyX_change = -0.4
        #enemyY += enemyY_change 

    # movimiento del fuego
    
    if fuegoY <=0:
        fuegoY = 450
        fuego_state = "ready" # reainiciar los tiros de fuego porque al salir de la pantalla seria menor o igual a cero (rango de 1 a 800)

    if fuego_state == "fire" :
       fire_fuego(fuegoX,fuegoY)
       fuegoY -= fuego_change


    colision = colisiones(enemyX,enemyY,fuegoX,fuegoY)
    if colision:
        fuegoY = 0
        fuego_state ="ready"
        score +=1
        print(score)
        enemyX = random.randint(0,800)
        enemyY = random.randint(50,150)

    player(playerX,playerY)
    enemy(enemyX,enemyY)
    #actualiza la pantalla para mostrar los cambios
    pygame.display.update()