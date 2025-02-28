import pygame
pygame.init()  # Inicia todos los módulos de Pygame

# Configurar pantalla
ANCHO, ALTO = 800, 600  # Definir el ancho y alto de la ventana
pantalla = pygame.display.set_mode((ANCHO, ALTO))  # Crea la ventana del juego
pygame.display.set_caption("Dibujar círculo morado en Pygame")  # Establece un título para la ventana

# Define los colores
MORADO = (128, 0, 128)  # Define el color morado en formato RGB

# Bucle del juego
ejecutando = True  # Variable que controla si el juego está ejecutando
while ejecutando:  # Bucle principal del juego
    for evento in pygame.event.get():  # Captura los eventos que ocurren
        if evento.type == pygame.QUIT:  # Si se detecta el evento de cerrar la ventana
            ejecutando = False  # Cambia la variable para salir del bucle

    # Limpiar pantalla antes de redibujar
    pantalla.fill((1, 0, 92))  # Rellena la pantalla de color negro (RGB: 0, 0, 0)

    # Dibujar un círculo en la pantalla
    pygame.draw.circle(pantalla, MORADO, (400, 300), 100)  # Dibuja un círculo morado con centro (400, 300) y radio de 100 píxeles

    # Actualizar la pantalla
    pygame.display.flip()  # Refresca la pantalla para mostrar los cambios

# Salir del juego cuando el bucle termine
pygame.quit()
