import pygame
import random
import time

pygame.init()

# Configuración de la ventana
ANCHO, ALTO = 800, 600
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("My Game")

# Cargar imágenes
fondo = pygame.image.load("imagenes/fondo1.jpg")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
player_skins = [
    pygame.image.load("imagenes/drago.png"),
    pygame.image.load("imagenes/drago2.png"),
    pygame.image.load("imagenes/drago3.png")
]
fuegoImg = pygame.image.load("imagenes/fuego.png")
enemyImg = pygame.image.load("imagenes/cazador.png")
explosionImg = pygame.image.load("imagenes/explosion.png")

# Cargar música y sonidos
pygame.mixer.music.load("sonidos/fondo.mp3")
pygame.mixer.music.play(-1)
sonido_disparo = pygame.mixer.Sound("sonidos/disparo.mp3")
sonido_explosion = pygame.mixer.Sound("sonidos/explo.mp3")

def seleccionar_personaje():
    indice = 0
    seleccionando = True
    while seleccionando:
        screen.blit(fondo, (0, 0))
        font = pygame.font.Font(None, 50)
        text = font.render("Selecciona tu personaje", True, (255, 255, 255))
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

def pantalla_inicio():
    screen.blit(fondo, (0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render("Presiona ENTER para iniciar", True, (255, 255, 255))
    screen.blit(text, (ANCHO // 2 - 200, ALTO // 2 - 30))
    pygame.display.update()
    
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                esperando = False

def mostrar_texto(texto, x, y, tamaño=36, color=(255, 255, 255)):
    font = pygame.font.Font(None, tamaño)
    render_texto = font.render(texto, True, color)
    screen.blit(render_texto, (x, y))

def pantalla_game_over():
    screen.blit(fondo, (0, 0))
    mostrar_texto("GAME OVER", ANCHO // 2 - 100, ALTO // 2 - 50, 50, (255, 0, 0))
    mostrar_texto("Presiona ENTER para reiniciar", ANCHO // 2 - 180, ALTO // 2, 36, (255, 255, 255))
    pygame.display.update()
    
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                esperando = False
                return True
    return False

playerImg = seleccionar_personaje()
pantalla_inicio()

def reiniciar_juego():
    return 400, 450, 0, [], 5, random.randint(0, 701), random.randint(50, 150), 1, 0.5, 0, time.time()

playerX, playerY, playerX_change, fuegos, fuego_change, enemyX, enemyY, enemyX_change, enemyY_change, score, start_time = reiniciar_juego()

running = True
while running:
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
                fuegos.append([playerX + playerImg.get_width() // 2 - fuegoImg.get_width() // 2, playerY])
                sonido_disparo.play()
        if evento.type == pygame.KEYUP and evento.key in (pygame.K_LEFT, pygame.K_RIGHT):
            playerX_change = 0

    playerX += playerX_change
    playerX = max(0, min(playerX, ANCHO - playerImg.get_width()))
    
    enemyY += enemyY_change
    if enemyY > ALTO:
        pantalla_game_over()
        playerX, playerY, playerX_change, fuegos, fuego_change, enemyX, enemyY, enemyX_change, enemyY_change, score, start_time = reiniciar_juego()
    
    nuevos_fuegos = []
    for fuego in fuegos:
        fuego[1] -= fuego_change
        if fuego[1] > 0:
            nuevos_fuegos.append(fuego)
        screen.blit(fuegoImg, (fuego[0], fuego[1]))
    fuegos = nuevos_fuegos

    enemy_rect = pygame.Rect(enemyX, enemyY, enemyImg.get_width(), enemyImg.get_height())
    for fuego in fuegos[:]:
        fuego_rect = pygame.Rect(fuego[0], fuego[1], fuegoImg.get_width(), fuegoImg.get_height())
        if enemy_rect.colliderect(fuego_rect):
            screen.blit(explosionImg, (enemyX, enemyY))
            sonido_explosion.play()
            pygame.time.delay(100)
            score += 1
            enemyX, enemyY = random.randint(0, 701), random.randint(50, 150)
            fuegos.remove(fuego)

    screen.blit(playerImg, (playerX, playerY))
    screen.blit(enemyImg, (enemyX, enemyY))
    mostrar_texto(f"Puntuación: {score}", 10, 10, 36, (0, 0, 0))
    
    pygame.display.update()

pygame.quit()

