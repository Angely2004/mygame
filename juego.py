import pygame
import random
pygame.init

#configura la ventana
ANCHO, ALTO = 800,600
screen = pygame.display.set_mode((ANCHO,ALTO)) #creamos la ventana con el tamaño definido 
pygame.display.set_caption("my game")

#fondo pantalla
fondo = pygame.image.load("imagenes/fondo.jpg")#cargamos imagen desde el archivo
fondo = pygame.transform.scale(fondo,(ANCHO,ALTO))

#player
playerImg= pygame.image.load('imagenes/dragon1.png')
playerX = 400
playerY = 500
playerX_change = 0

#enemy
enemyImg= pygame.image.load('imagenes/random3.jpg')
enemyX = random.randint (0,800) #coloca valores aleatorios
enemyY = random.randint (50,150)
enemyX_change = 30
enemyX_change = 40

#funcion para dibujar el juegador
def player(x,y):
    screen.blit(playerImg,(x,y))
#funcion para dibujar el enemigo
def enemy(x,y):
    screen.blit(enemyImg,(x,y))


running = True
while running:

    screen.blit(fondo,(0,0))

    for evento in pygame.event.get() : #captura eventos (teclado,raton)
        if evento.type == pygame.QUIT:
            running = False #sale del bucle

        # mover el juegador con teclas hacia la izquierda
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                playerX_change = -0.1
        #Mover con tecla hacia la derecha
            if evento.key == pygame.K_RIGHT:
                playerX_change = 0.1
        # para reconocer un no se esta moviendo
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                playerX_change = 0
            


    playerX+= playerX_change

    # para que no se desborde en las paredes de la ventana
    if playerX <=0:
        playerX = 0
    elif playerX >=736: #porque quitamos en tamaño del jugador
        playerX = 736

    enemyX+= enemyX_change
    # para que no se desborde en las paredes de la ventana
    if enemyX <=0:
        enemyX_change = 0.3
        enemyY += enemyX_change
    elif enemyX >=736: #porque quitamos en tamaño del jugador
        enemyX_change = -0.3
        enemyY += enemyX_change # para moverse hacia abajo

    player(playerX,playerY)
    enemy(enemyX,enemyY)
    #actualiza la pantalla para mostrar los cambios
    pygame.display.update()