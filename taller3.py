import pygame
import sys
import random
import os
from pygame import mixer

# Inicialización de Pygame
pygame.init()
mixer.init()

# Constantes del juego
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Configuración de la pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Colisiones")
clock = pygame.time.Clock()

# Cargar sonidos
def load_sound(filename):
    try:
        sound_path = os.path.join("sonidos", filename)
        if os.path.exists(sound_path):
            return mixer.Sound(sound_path)
        else:
            print(f"No se pudo encontrar el archivo: {sound_path}")
            return None
    except Exception as e:
        print(f"Error al cargar el sonido {filename}: {e}")
        return None

# Cargar sonidos
collision_sound = load_sound("sonidos/colision.mp3")
powerup_sound = load_sound("sonidos/power.mp3")
game_over_sound = load_sound("sonidos/gameover.mp3")

# Cargar música de fondo
has_music = False
try:
    music_path = os.path.join("sonidos/fondo.mp3")
    if os.path.exists(music_path):
        pygame.mixer.music.load(music_path)
        has_music = True
    else:
        print("No se pudo encontrar el archivo de música de fondo")
except Exception as e:
    print(f"Error al cargar la música de fondo: {e}")

# Función para reproducir sonidos de manera segura
def play_sound(sound):
    if sound:
        try:
            sound.play()
        except Exception as e:
            print(f"Error al reproducir sonido: {e}")

# Clase para jugadores
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color, controls, player_id):
        super().__init__()
        self.original_image = pygame.Surface((30, 30))
        self.original_image.fill(color)
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5
        self.controls = controls
        self.color = color
        self.original_color = color
        self.collision_timer = 0
        self.score = 0
        self.player_id = player_id
        self.powerup_timer = 0
        self.is_powered_up = False

    def update(self):
        keys = pygame.key.get_pressed()
        
        # Movimiento del jugador
        if keys[self.controls[0]]:  # Arriba
            self.rect.y -= self.speed
        if keys[self.controls[1]]:  # Abajo
            self.rect.y += self.speed
        if keys[self.controls[2]]:  # Izquierda
            self.rect.x -= self.speed
        if keys[self.controls[3]]:  # Derecha
            self.rect.x += self.speed
            
        # Mantener al jugador dentro de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            
        # Efecto visual de colisión
        if self.collision_timer > 0:
            self.collision_timer -= 1
            if self.collision_timer == 0:
                self.image.fill(self.color)
                
        # Gestión del power-up
        if self.is_powered_up:
            self.powerup_timer -= 1
            if self.powerup_timer <= 0:
                self.speed = 5
                self.is_powered_up = False
                self.color = self.original_color
                self.image.fill(self.color)

    def collision_effect(self):
        self.image.fill(WHITE)
        self.collision_timer = 10
        
    def apply_powerup(self):
        self.speed = 8
        self.is_powered_up = True
        self.powerup_timer = 180  # 3 segundos a 60 FPS
        self.color = YELLOW
        self.image.fill(YELLOW)
        play_sound(powerup_sound)

# Clase para obstáculos
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect(topleft=(x, y))

# Clase para power-ups
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect(center=(x, y))
        
# Clase para el efecto de explosión
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.size = 20
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=center)
        self.life = 15  # Duración de la explosión
        
    def update(self):
        self.life -= 1
        if self.life <= 0:
            self.kill()
        elif self.life < 10:
            self.size = 15
            self.image = pygame.Surface((self.size, self.size))
            self.image.fill(ORANGE)
            self.rect = self.image.get_rect(center=self.rect.center)
        elif self.life < 5:
            self.size = 10
            self.image = pygame.Surface((self.size, self.size))
            self.image.fill(YELLOW)
            self.rect = self.image.get_rect(center=self.rect.center)

# Función para dibujar texto
def draw_text(surface, text, size, x, y, color=WHITE):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

# Función para crear obstáculos
def create_obstacles():
    obstacles = pygame.sprite.Group()
    
    # Obstáculos horizontales
    obstacles.add(Obstacle(100, 100, 200, 20))
    obstacles.add(Obstacle(500, 100, 200, 20))
    obstacles.add(Obstacle(100, 480, 200, 20))
    obstacles.add(Obstacle(500, 480, 200, 20))
    
    # Obstáculos verticales
    obstacles.add(Obstacle(380, 200, 20, 200))
    
    return obstacles

# Función para generar power-ups aleatorios
def spawn_powerup():
    x = random.randint(50, WIDTH - 50)
    y = random.randint(50, HEIGHT - 50)
    return PowerUp(x, y)

# Pantalla de inicio
def show_start_screen():
    screen.fill(BLACK)
    draw_text(screen, "JUEGO DE COLISIONES", 50, WIDTH // 2, HEIGHT // 4, WHITE)
    draw_text(screen, "Jugador 1: Flechas", 25, WIDTH // 2, HEIGHT // 2 - 50, RED)
    draw_text(screen, "Jugador 2: WASD", 25, WIDTH // 2, HEIGHT // 2, GREEN)
    draw_text(screen, "Presiona ESPACIO para comenzar", 30, WIDTH // 2, HEIGHT * 3/4, WHITE)
    draw_text(screen, "ESC para salir", 20, WIDTH // 2, HEIGHT * 3/4 + 50, WHITE)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Menú de pausa
def show_pause_menu():
    pause_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pause_surface.fill((0, 0, 0, 150))
    screen.blit(pause_surface, (0, 0))
    
    draw_text(screen, "PAUSA", 60, WIDTH // 2, HEIGHT // 4, WHITE)
    draw_text(screen, "Presiona R para reanudar", 30, WIDTH // 2, HEIGHT // 2, WHITE)
    draw_text(screen, "Presiona Q para salir", 30, WIDTH // 2, HEIGHT // 2 + 50, WHITE)
    pygame.display.flip()
    
    paused = True
    while paused:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    paused = False
                if event.key == pygame.K_q:
                    return True  # Salir del juego
    return False  # Continuar el juego

# Pantalla de selección de personaje
def character_selection():
    player1_color = RED
    player2_color = GREEN
    colors = [RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE]
    p1_selection = 0
    p2_selection = 1
    
    selecting = True
    while selecting:
        screen.fill(BLACK)
        draw_text(screen, "SELECCIÓN DE PERSONAJE", 50, WIDTH // 2, HEIGHT // 4, WHITE)
        
        # Jugador 1
        draw_text(screen, "Jugador 1", 30, WIDTH // 4, HEIGHT // 2 - 80, WHITE)
        pygame.draw.rect(screen, colors[p1_selection], (WIDTH // 4 - 25, HEIGHT // 2 - 40, 50, 50))
        draw_text(screen, "← →", 20, WIDTH // 4, HEIGHT // 2 + 30, WHITE)
        
        # Jugador 2
        draw_text(screen, "Jugador 2", 30, WIDTH * 3 // 4, HEIGHT // 2 - 80, WHITE)
        pygame.draw.rect(screen, colors[p2_selection], (WIDTH * 3 // 4 - 25, HEIGHT // 2 - 40, 50, 50))
        draw_text(screen, "A D", 20, WIDTH * 3 // 4, HEIGHT // 2 + 30, WHITE)
        
        draw_text(screen, "Presiona ESPACIO para confirmar", 30, WIDTH // 2, HEIGHT * 3/4, WHITE)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    selecting = False
                # Controles de selección del jugador 1
                if event.key == pygame.K_LEFT:
                    p1_selection = (p1_selection - 1) % len(colors)
                    if p1_selection == p2_selection:
                        p1_selection = (p1_selection - 1) % len(colors)
                if event.key == pygame.K_RIGHT:
                    p1_selection = (p1_selection + 1) % len(colors)
                    if p1_selection == p2_selection:
                        p1_selection = (p1_selection + 1) % len(colors)
                # Controles de selección del jugador 2
                if event.key == pygame.K_a:
                    p2_selection = (p2_selection - 1) % len(colors)
                    if p2_selection == p1_selection:
                        p2_selection = (p2_selection - 1) % len(colors)
                if event.key == pygame.K_d:
                    p2_selection = (p2_selection + 1) % len(colors)
                    if p2_selection == p1_selection:
                        p2_selection = (p2_selection + 1) % len(colors)
        
        clock.tick(FPS)
    
    return colors[p1_selection], colors[p2_selection]

# Pantalla de Game Over
def show_game_over(player1, player2, win_score):
    play_sound(game_over_sound)
        
    screen.fill(BLACK)
    
    # Determinar el ganador correctamente basado en quién alcanzó el objetivo primero
    winner = None
    winner_color = WHITE
    
    if player1.score >= win_score and player2.score >= win_score:
        # Si ambos jugadores alcanzan la puntuación en la misma colisión, es empate
        winner = "¡Empate!"
        winner_color = WHITE
    elif player1.score >= win_score:
        winner = "Jugador 1"
        winner_color = player1.original_color
    elif player2.score >= win_score:
        winner = "Jugador 2"
        winner_color = player2.original_color
        
    draw_text(screen, f"¡{winner} GANA!", 60, WIDTH // 2, HEIGHT // 3, winner_color)
    draw_text(screen, f"Puntuación: Jugador 1: {player1.score} - Jugador 2: {player2.score}", 30, WIDTH // 2, HEIGHT // 2, WHITE)
    draw_text(screen, "Presiona R para jugar de nuevo", 30, WIDTH // 2, HEIGHT * 2/3, WHITE)
    draw_text(screen, "Presiona ESC para salir", 30, WIDTH // 2, HEIGHT * 2/3 + 50, WHITE)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  # Jugar de nuevo
                if event.key == pygame.K_ESCAPE:
                    return False  # Salir del juego

# Función principal del juego
def game():
    # Mostrar pantalla de inicio
    show_start_screen()
    
    # Selección de personaje
    player1_color, player2_color = character_selection()
    
    # Iniciar música si está disponible
    if has_music:
        try:
            pygame.mixer.music.play(-1)  # Reproducir en bucle
        except Exception as e:
            print(f"Error al reproducir música de fondo: {e}")
    
    while True:
        # Inicializar grupos de sprites
        all_sprites = pygame.sprite.Group()
        obstacles = create_obstacles()
        powerups = pygame.sprite.Group()
        explosions = pygame.sprite.Group()
        
        # Crear jugadores
        player1 = Player(WIDTH // 4, HEIGHT // 2, player1_color, 
                        [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT], 1)
        player2 = Player(WIDTH * 3 // 4, HEIGHT // 2, player2_color, 
                        [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d], 2)
        
        all_sprites.add(player1, player2)
        all_sprites.add(obstacles)
        
        # Configuración del juego
        win_score = 10
        running = True
        paused = False
        game_speed = 1.0
        powerup_spawn_timer = 180  # 3 segundos a 60 FPS
        winner_determined = False  # Variable para controlar quién gana primero
        
        # Bucle principal del juego
        while running:
            clock.tick(FPS)
            
            # Manejo de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = True
                        if show_pause_menu():  # Si retorna True, salir del juego
                            pygame.quit()
                            sys.exit()
            
            if not paused:
                # Actualizar sprites
                all_sprites.update()
                
                # Comprobar colisiones entre jugadores
                if pygame.sprite.collide_rect(player1, player2):
                    player1.collision_effect()
                    player2.collision_effect()
                    
                    # Aumentar puntuación
                    player1.score += 1
                    player2.score += 1
                    
                    # Añadir efecto de explosión
                    collision_pos = ((player1.rect.centerx + player2.rect.centerx) // 2,
                                    (player1.rect.centery + player2.rect.centery) // 2)
                    explosion = Explosion(collision_pos)
                    explosions.add(explosion)
                    all_sprites.add(explosion)
                    
                    play_sound(collision_sound)
                
                # Verificar colisiones con obstáculos
                pygame.sprite.spritecollide(player1, obstacles, False)
                pygame.sprite.spritecollide(player2, obstacles, False)
                
                # Manejar power-ups
                powerup_spawn_timer -= 1
                if powerup_spawn_timer <= 0:
                    new_powerup = spawn_powerup()
                    powerups.add(new_powerup)
                    all_sprites.add(new_powerup)
                    powerup_spawn_timer = random.randint(180, 360)  # 3-6 segundos
                
                # Verificar colisiones con power-ups
                powerup_hit = pygame.sprite.spritecollide(player1, powerups, True)
                if powerup_hit:
                    player1.apply_powerup()
                
                powerup_hit = pygame.sprite.spritecollide(player2, powerups, True)
                if powerup_hit:
                    player2.apply_powerup()
                
                # Aumentar la velocidad gradualmente
                if player1.score + player2.score > 0 and (player1.score + player2.score) % 5 == 0:
                    game_speed += 0.05
                
                # Verificar condiciones de victoria
                if not winner_determined:
                    if player1.score >= win_score:
                        winner_determined = True
                        if has_music:
                            try:
                                pygame.mixer.music.stop()
                            except:
                                pass
                        play_again = show_game_over(player1, player2, win_score)
                        if play_again:
                            if has_music:
                                try:
                                    pygame.mixer.music.play(-1)
                                except:
                                    pass
                            break  # Reiniciar el juego
                        else:
                            pygame.quit()
                            sys.exit()
                    elif player2.score >= win_score:
                        winner_determined = True
                        if has_music:
                            try:
                                pygame.mixer.music.stop()
                            except:
                                pass
                        play_again = show_game_over(player1, player2, win_score)
                        if play_again:
                            if has_music:
                                try:
                                    pygame.mixer.music.play(-1)
                                except:
                                    pass
                            break  # Reiniciar el juego
                        else:
                            pygame.quit()
                            sys.exit()
                
                # Dibujado
                screen.fill(BLACK)
                
                # Dibujar todos los sprites
                all_sprites.draw(screen)
                
                # Dibujar la puntuación
                draw_text(screen, f"Jugador 1: {player1.score}", 30, 100, 20, player1.original_color)
                draw_text(screen, f"Jugador 2: {player2.score}", 30, WIDTH - 100, 20, player2.original_color)
                draw_text(screen, f"Objetivo: {win_score} puntos", 20, WIDTH // 2, 20, WHITE)
                
                # Dibujar instrucciones de pausa
                draw_text(screen, "ESC: Pausa", 20, 60, HEIGHT - 20, WHITE)
                
                pygame.display.flip()

# Iniciar el juego
if __name__ == "__main__":
    game()