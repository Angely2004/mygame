import pygame

# Inicialización de Pygame
pygame.init()
pygame.mixer.init()

# Definición de la pantalla
ANCHO, ALTO = 900, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))  # Crea la ventana del juego
pygame.display.set_caption("Reproducir Sonido y Fondo")


fondo = pygame.image.load("imagenes/random.jpg")  # Cargamos imagen desde el archivo
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))


sonido_salto = pygame.mixer.Sound("sonidos/dragon.mp3")


ejecutando = True

while ejecutando:
    
    for evento in pygame.event.get():  # Captura eventos (teclado, ratón)
        if evento.type == pygame.QUIT:
            ejecutando = False  # Sale del bucle si se cierra la ventana
        if evento.type == pygame.KEYDOWN:  # Si se presiona una tecla
            if evento.key == pygame.K_SPACE:  # Si se presiona la barra espaciadora
                sonido_salto.play()  # Reproduce el sonido
    pantalla.blit(fondo, (0, 0))

    pygame.display.flip()
pygame.quit()