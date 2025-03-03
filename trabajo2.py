import pygame
import random
import time

pygame.init()

# Configuración de la ventana
ANCHO, ALTO = 800, 600
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("My Game")
#

# Cargar imágenes
fondo = pygame.image.load("imagenes/fondo1.jpg")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
player_skins = [
    pygame.image.load("imagenes/drago.png"),
    pygame.image.load("imagenes/drago2.png"),
    pygame.image.load("imagenes/drago3.png")
]

# Cargar imágenes
fondo = pygame.image.load("imagenes/fondo1.jpg")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
playerImg = pygame.image.load('imagenes/drago.png')
fuegoImg = pygame.image.load('imagenes/fuego.png')
enemyImg = pygame.image.load('imagenes/cazador.png')
explosionImg = pygame.image.load('imagenes/explosion.png')

# Cargar música y sonidos
pygame.mixer.music.load("sonidos/fondo.mp3")
pygame.mixer.music.play(-1)
sonido_disparo = pygame.mixer.Sound("sonidos/disparo.mp3")
sonido_explosion = pygame.mixer.Sound("sonidos/explo.mp3")

# Función para mostrar puntuación
def mostrar_puntuacion(score):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Puntuación: {score}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

# Función para dibujar el jugador
def player(x, y):
    screen.blit(playerImg, (x, y))

# Función para dibujar el enemigo
def enemy(x, y):
    screen.blit(enemyImg, (x, y))

# Función para calcular la velocidad del enemigo basada en la distancia al jugador
def calcular_velocidad_enemigo(playerX, playerY, enemyX, enemyY, velocidad_base):
    distancia = ((playerX - enemyX) ** 2 + (playerY - enemyY) ** 2) ** 0.5
    velocidad = velocidad_base + max((300 - distancia) / 100, 0)  # Aumenta velocidad al acercarse
    return velocidad
#

#funcio para cambiar personaje
def seleccionar_personaje():
    indice = 0
    seleccionando = True
    while seleccionando:
        screen.blit(fondo, (0, 0))
        font = pygame.font.Font(None, 50)
        text = font.render("Selecciona tu personaje", True, (0, 0, 0))
        screen.blit(text, (ANCHO // 2 - 200, 50))
        screen.blit(player_skins[indice], (ANCHO // 2 - 50, ALTO // 2 - 50))
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    indice = (indice - 1) % len(player_skins)
                if evento.key == pygame.K_RIGHT:
                    indice = (indice + 1) % len(player_skins)
                if evento.key == pygame.K_RETURN:
                    seleccionando = False
    return player_skins[indice]

# Función para pantalla de inicio
def pantalla_inicio():
    screen.blit(fondo, (0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render("Presiona ENTER para iniciar", True, (0, 0, 0))
    text2 = pygame.font.Font(None, 30).render("Presiona P para pausar el juego", True, (0, 0, 0))
    screen.blit(text, (ANCHO // 2 - 200, ALTO // 2 - 30))
    screen.blit(text2, (ANCHO // 2 - 150, ALTO // 2 + 20))
    pygame.display.update()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                esperando = False

playerImg = seleccionar_personaje()
pantalla_inicio()
# Función para pantalla de pausa
def pantalla_pausa():
    font = pygame.font.Font(None, 60)
    text = font.render("Juego Pausado", True, (0, 0, 0))
    screen.blit(text, (ANCHO // 2 - 150, ALTO // 2 - 30))
    pygame.display.update()
    pausado = True
    while pausado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_p:
                pausado = False

# Función para pantalla de Game Over
def pantalla_game_over(mensaje):
    font = pygame.font.Font(None, 50)
    text = font.render(mensaje, True, (255, 255, 255))
    button_restart = pygame.Rect(300, 350, 200, 50)
    button_exit = pygame.Rect(300, 420, 200, 50)

    esperando = True
    while esperando:
        screen.blit(fondo, (0, 0))
        screen.blit(text, (ANCHO // 2 - 100, ALTO // 2 - 30))
        pygame.draw.rect(screen, (0, 255, 0), button_restart)
        pygame.draw.rect(screen, (255, 0, 0), button_exit)
        screen.blit(pygame.font.Font(None, 40).render("Reiniciar", True, (0, 0, 0)), (350, 360))
        screen.blit(pygame.font.Font(None, 40).render("Salir", True, (0, 0, 0)), (375, 430))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_restart.collidepoint(event.pos):
                    return True  # Reiniciar el juego
                if button_exit.collidepoint(event.pos):
                    pygame.quit()
                    exit()

        pygame.display.update()

# Inicializar variables
def reiniciar_juego():
    return 400, 450, 0, [], 0.5, random.randint(0, 701), random.randint(50, 150), 1, 40, 0, time.time()

# Mostrar la pantalla de inicio
pantalla_inicio()

# Variables del juego
playerX, playerY, playerX_change, fuegos, fuego_change, enemyX, enemyY, enemyX_change, enemyY_change, score, start_time = reiniciar_juego()

running = True
while running:
    elapsed_time = time.time() - start_time
    screen.blit(fondo, (0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                playerX_change = -3
            if evento.key == pygame.K_RIGHT:
                playerX_change = 3
            if evento.key == pygame.K_SPACE:
                fuegos.append([playerX + 90, playerY])
                sonido_disparo.play()
            if evento.key == pygame.K_p:
                pantalla_pausa()
        if evento.type == pygame.KEYUP and evento.key in (pygame.K_LEFT, pygame.K_RIGHT):
            playerX_change = 0

    playerX += playerX_change
    playerX = max(0, min(playerX, 550))

    velocidad_enemigo = calcular_velocidad_enemigo(playerX, playerY, enemyX, enemyY, 1)
    if enemyX < playerX:
        enemyX += velocidad_enemigo
    else:
        enemyX -= velocidad_enemigo

    if enemyY < playerY:
        enemyY += velocidad_enemigo / 10
    else:
        enemyY -= velocidad_enemigo / 10

    nuevos_fuegos = []
    for fuego in fuegos:
        fuego[1] -= fuego_change
        if fuego[1] > 0:
            nuevos_fuegos.append(fuego)
        screen.blit(fuegoImg, (fuego[0], fuego[1]))
    fuegos = nuevos_fuegos

    enemy_rect = pygame.Rect(enemyX, enemyY, enemyImg.get_width(), enemyImg.get_height())
    player_rect = pygame.Rect(playerX, playerY, playerImg.get_width(), playerImg.get_height())

    for fuego in fuegos[:]:
        fuego_rect = pygame.Rect(fuego[0], fuego[1], fuegoImg.get_width(), fuegoImg.get_height())
        if enemy_rect.colliderect(fuego_rect):
            screen.blit(explosionImg, (enemyX, enemyY))
            sonido_explosion.play()
            pygame.time.delay(100)
            score += 1
            enemyX, enemyY = random.randint(0, 701), random.randint(50, 150)
            fuegos.remove(fuego)

    if score >= 5 or enemy_rect.colliderect(player_rect):
        if pantalla_game_over("¡Victoria!" if score >= 5 else "Game Over"):
            playerX, playerY, playerX_change, fuegos, fuego_change, enemyX, enemyY, enemyX_change, enemyY_change, score, start_time = reiniciar_juego()

    player(playerX, playerY)
    enemy(enemyX, enemyY)
    mostrar_puntuacion(score)
    pygame.display.update()



