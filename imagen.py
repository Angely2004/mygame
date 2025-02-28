import pygame
pygame.init

#configura la ventana
ANCHO, ALTO = 900,900
pantalla = pygame.display.set_mode((ANCHO,ALTO)) #creamos la ventana con el tamaño definido 
pygame.display.set_caption("cambia fondo")

#fondo pantalla
fondo = pygame.image.load("imagenes/random.jpg")#cargamos imagen desde el archivo
fondo = pygame.transform.scale(fondo,(ANCHO,ALTO))

ejecutando = True
while ejecutando:
    #manejo de eventos 
    for evento in pygame.event.get() : #captura eventos (teclado,raton)
        if evento.type == pygame.QUIT:
            ejecutando = False #sale del bucle
    pantalla.blit(fondo,(0,0))
    #actualiza la pantalla para mostrar los cambios
    pygame.display.flip()