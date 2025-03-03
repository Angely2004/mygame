import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego con Pygame")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

# Cargar música de fondo con manejo de errores
try:
    pygame.mixer.music.load("sonidos/fondo.mp3")
    pygame.mixer.music.set_volume(0.5)
except pygame.error:
    print("Advertencia: No se pudo cargar la música de fondo.")

# Cargar efectos de sonido con manejo de errores
try:
    sonido_colision = pygame.mixer.Sound("sonidos/explo.mp3")
except pygame.error:
    print("Advertencia: No se pudo cargar el sonido de colisión.")
    sonido_colision = None  # Evita errores si el archivo no existe

# Skins de los jugadores (colores)
skins = [ROJO, VERDE, AZUL]
jugador_color = skins[0]  # Color por defecto

# Fuente para la puntuación
fuente = pygame.font.Font(None, 36)

# Clase Jugador
class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y, color, velocidad):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad = velocidad
        self.color_original = color
        self.tiempo_colision = 0  # Para gestionar el cambio de color tras la colisión

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocidad
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocidad

        # Restaurar color después de un tiempo tras la colisión
        if self.tiempo_colision > 0:
            self.tiempo_colision -= 1
        else:
            self.image.fill(self.color_original)

# Clase Obstáculo
class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(NEGRO)
        self.rect = self.image.get_rect(center=(x, y))

# Pantalla de inicio
def pantalla_inicio():
    global jugador_color
    ejecutando = True
    seleccionado = 0

    while ejecutando:
        pantalla.fill(BLANCO)
        texto_titulo = fuente.render("Selecciona tu color", True, NEGRO)
        pantalla.blit(texto_titulo, (ANCHO // 2 - 100, 50))

        for i, color in enumerate(skins):
            pygame.draw.rect(pantalla, color, (300 + i * 100, 200, 50, 50))
            if i == seleccionado:
                pygame.draw.rect(pantalla, NEGRO, (300 + i * 100, 200, 50, 50), 3)

        texto_inicio = fuente.render("Presiona Enter para comenzar", True, NEGRO)
        pantalla.blit(texto_inicio, (ANCHO // 2 - 150, 400))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    seleccionado = max(0, seleccionado - 1)
                if evento.key == pygame.K_RIGHT:
                    seleccionado = min(len(skins) - 1, seleccionado + 1)
                if evento.key == pygame.K_RETURN:
                    jugador_color = skins[seleccionado]
                    ejecutando = False

# Función principal del juego
def main():
    reloj = pygame.time.Clock()
    jugador = Jugador(ANCHO // 2, ALTO - 100, jugador_color, 5)
    obstaculos = pygame.sprite.Group()

    # Crear obstáculos
    for _ in range(5):
        obstaculo = Obstaculo(random.randint(50, ANCHO - 50), random.randint(50, ALTO - 200))
        obstaculos.add(obstaculo)

    jugadores = pygame.sprite.Group()
    jugadores.add(jugador)

    puntuacion = 0
    colision_detectada = False  # Para evitar la suma continua de puntos en colisión

    if pygame.mixer.music.get_busy() == 0:
        pygame.mixer.music.play(-1)  # Reproducir música en bucle si está disponible

    corriendo = True
    while corriendo:
        pantalla.fill(BLANCO)
        keys = pygame.key.get_pressed()
        jugadores.update(keys)

        # Comprobar colisiones
        if pygame.sprite.spritecollide(jugador, obstaculos, False):
            if not colision_detectada:  # Solo aumentar la puntuación una vez por colisión
                colision_detectada = True
                puntuacion += 1
                jugador.image.fill(ROJO)  # Cambia de color al chocar
                jugador.tiempo_colision = 30  # Mantener el color por un corto tiempo
                if sonido_colision:
                    sonido_colision.play()
        else:
            colision_detectada = False  # Resetear la detección de colisión

        # Dibujar elementos
        jugadores.draw(pantalla)
        obstaculos.draw(pantalla)

        # Mostrar puntuación
        texto_puntuacion = fuente.render(f"Puntuación: {puntuacion}", True, NEGRO)
        pantalla.blit(texto_puntuacion, (10, 10))

        pygame.display.flip()
        reloj.tick(60)

        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

    pygame.quit()

# Ejecutar el juego
pantalla_inicio()
main()
