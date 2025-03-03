import pygame
import random
import time

pygame.init()

# Configura la ventana
ANCHO, ALTO = 800, 600
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("My Game")

# Fuentes
fuente = pygame.font.Font(None, 36)
fuente_victoria = pygame.font.Font(None, 80)
fuente_menu = pygame.font.Font(None, 50)

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)

# Cargar imágenes
fondo = pygame.image.load("imagenes/fondo1.jpg")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
playerImg = pygame.image.load('imagenes/drago.png')
fuegoImg = pygame.image.load('imagenes/fuego.png')
enemyImg = pygame.image.load('imagenes/cazador.png')

def dibujar_texto(texto, fuente, color, x, y):
    img = fuente.render(texto, True, color)
    screen.blit(img, (x, y))

def pantalla_inicio():
    while True:
        screen.fill(BLANCO)
        dibujar_texto("My Game", fuente_menu, NEGRO, ANCHO//2 - 100, 200)
        dibujar_texto("Presiona ENTER para Jugar", fuente, NEGRO, ANCHO//2 - 140, 300)
        pygame.display.update()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                return

def menu_pausa():
    while True:
        screen.fill(BLANCO)
        dibujar_texto("Pausa", fuente_menu, NEGRO, ANCHO//2 - 50, 200)
        dibujar_texto("Presiona R para reanudar", fuente, NEGRO, ANCHO//2 - 130, 300)
        dibujar_texto("Presiona Q para salir", fuente, NEGRO, ANCHO//2 - 100, 350)
        pygame.display.update()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    return
                if evento.key == pygame.K_q:
                    pygame.quit()
                    quit()

def mostrar_mensaje_derrota():
    while True:
        screen.fill(BLANCO)
        dibujar_texto("Game Over", fuente_victoria, ROJO, ANCHO// 2 - 50, 200)
        dibujar_texto("Presiona R para reiniciar", fuente, NEGRO, ANCHO // 2 - 130, 300)
        dibujar_texto("Presiona Q para salir", fuente, NEGRO, ANCHO//2 - 100, 350)
        pygame.display.update()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    return
                if evento.key == pygame.K_q:
                    pygame.quit()
                    quit()
                

def jugar():
    while True:
        inicio_tiempo = time.time()
        score = 0
        disparos_realizados = 0
        playerX = 400
        playerX_change = 0
        fuego_state = "ready"
        fuegoX, fuegoY = 0, 450
        enemyX, enemyY = random.randint(0, 701), random.randint(50, 150)
        enemyX_change, enemyY_change = 0.3, 40
        running = True
        while running:
            screen.blit(fondo, (0, 0))
            tiempo_transcurrido = time.time() - inicio_tiempo
            
            if tiempo_transcurrido >= 60 and score < 5:
                mostrar_mensaje_derrota()
                break
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_LEFT:
                        playerX_change = -0.3
                    if evento.key == pygame.K_RIGHT:
                        playerX_change = 0.3
                    if evento.key == pygame.K_SPACE and fuego_state == "ready":
                        fuegoX = playerX
                        fuego_state = "fire"
                        disparos_realizados += 1
                    if evento.key == pygame.K_p:
                        menu_pausa()
                    if evento.key == pygame.K_p:
                        mostrar_mensaje_derrota()
                if evento.type == pygame.KEYUP and evento.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    playerX_change = 0

            # Movimiento
            playerX = max(0, min(playerX + playerX_change, 550))
            enemyX += enemyX_change
            if enemyX <= 0 or enemyX >= 701:
                enemyX_change *= -1
                enemyY += enemyY_change
            if fuego_state == "fire":
                screen.blit(fuegoImg, (fuegoX + 80, fuegoY - 5))
                fuegoY -= 0.5
            if fuegoY <= 0:
                fuegoY, fuego_state = 450, "ready"

            # Colisión
            if pygame.Rect(enemyX, enemyY, enemyImg.get_width(), enemyImg.get_height()).colliderect(
                    pygame.Rect(fuegoX, fuegoY, fuegoImg.get_width(), fuegoImg.get_height())):
                fuegoY, fuego_state, score = 450, "ready", score + 1
                enemyX, enemyY = random.randint(0, 701), random.randint(50, 150)

            # Dibujar elementos
            screen.blit(playerImg, (playerX, 450))
            screen.blit(enemyImg, (enemyX, enemyY))
            dibujar_texto(f"Puntaje: {score}", fuente, NEGRO, 10, 10)
            dibujar_texto(f"Tiempo: {int(60 - tiempo_transcurrido)}s", fuente, NEGRO, 650, 10)
            dibujar_texto(f"Disparos: {disparos_realizados}", fuente, NEGRO, 650, 40)
            
            if score >= 5:
                dibujar_texto("¡Victoria!", fuente_victoria, (255, 255, 0), ANCHO // 2 - 150, ALTO // 2 - 40)
                pygame.display.update()
                pygame.time.delay(3000)
                running = False
                menu_pausa()

            pygame.display.update()
        
# Pantalla de inicio
pantalla_inicio()
# Iniciar el juego
while True:
    jugar()




