import pygame
pygame.init()  # Inicia todos los módulos de Pygame

# Configurar pantalla
ANCHO, ALTO = 800, 600  # Definir el ancho y alto de la ventana
pantalla = pygame.display.set_mode((ANCHO, ALTO))  # Crea la ventana del juego
pygame.display.set_caption("Dibujar rectángulo en Pygame")  # Establece un título para la ventana

# Define los colores
ROJO = (255, 0, 0)  # Define el color rojo en formato RGB

# Bucle del juego
ejecutando = True  # Variable que controla si el juego está ejecutando
while ejecutando:  # Bucle principal del juego
    for evento in pygame.event.get():  # Captura los eventos que ocurren
        if evento.type == pygame.QUIT:  # Si se detecta el evento al cerrar la ventana
            ejecutando = False  # Se cambia la variable para salir del bucle

    # Limpiar pantalla antes de redibujar
    pantalla.fill((0, 0, 0))  # Rellena la pantalla de color negro (RGB: 0, 0, 0)

    # Dibujar un rectángulo en la pantalla
    pygame.draw.rect(pantalla, ROJO, (100, 150, 200, 100))  # Dibuja un rectángulo rojo

    # Actualizar la pantalla
    pygame.display.flip()  # Refresca la pantalla para mostrar los cambios

# Salir del juego cuando el bucle termine
pygame.quit()
