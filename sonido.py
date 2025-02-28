import pygame
pygame.init()

pygame.mixer.init()
pantalla = pygame.display.set_mode((800,600))
pygame.display.set_caption("reproducir sonidos")

sonido_salto = pygame.mixer.Sound("sonidos/dragon.mp3")

ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        if evento.type == pygame.KEYDOWN : #si se presiona la tecla en el espacio sse reproduce el sonido
            if evento.key == pygame.K_SPACE:
             sonido_salto.play()
pygame.quit()
