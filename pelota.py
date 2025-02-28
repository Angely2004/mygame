import pygame #importar la libreria par trabajar graficos

pygame.init() #inicializa las funciones epygame

#configura la ventana
ANCHO, ALTO = 1000,800
pantalla = pygame.display.set_mode((ANCHO,ALTO)) #creamos la ventana con el tamaño definido 
pygame.display.set_caption("pelota rebotando")

#variables de la pelota
pelota = pygame.Rect(800,500,80,80)
velocidad_x,velocidad_y = 3,3 #restablecemos velocidad en eje x

#bucle principal del juego
ejecutando = True #variable para controlar el bucle principal
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False #cambia la variable para salir del juego 

     #mueve la pelota sumando la velocidad a su posicion actual
    pelota.x += velocidad_x
    pelota.y += velocidad_y

     #colisiones con los bordes de las ventanas
    if pelota.left <= 0 or pelota.right >= ANCHO : #si la pelota toca el lado izquierdo de la ventana 
        velocidad_x = -velocidad_x #invierte la direccion en el eje x
    if pelota.top <= 0 or pelota.bottom >= ALTO :
        velocidad_y = -velocidad_y # invierte la direccion en el eje y

    pantalla.fill((0,0,0)) #rellena la pantalla de color negro
    pygame.draw.ellipse(pantalla,(0,255,0),pelota)
    pygame.display.flip()
pygame.quit()


