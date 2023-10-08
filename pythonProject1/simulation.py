import pygame
import math


# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
SUN_COLOR = (255, 255, 0)
EARTH_COLOR = (0, 0, 255)
MOON_COLOR = (169, 169, 169)
G = 6.67430e-11  # Gravitational constant (m^3/kg/s^2)

# Define the initial conditions
earth_x, earth_y = WIDTH // 2, HEIGHT // 2
earth_radius = 149.52
earth_angle = 0
earth_speed = 0.0174533 # Angular speed (radians per frame)

moon_x, moon_y = earth_x + earth_radius, earth_y
moon_radius = 20
moon_angle = 0
moon_speed = 0.51108876748  # Angular speed (radians per frame)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Earth-Moon-Sun Orbit Simulation")

# Initialize font
font = pygame.font.Font(None, 36)

# Flag to determine when to display "You Win" text
you_win = False

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # Calculate the new positions of Earth and Moon
    earth_angle += earth_speed
    moon_angle += moon_speed

    earth_x = WIDTH // 2 + earth_radius * math.cos(earth_angle)
    earth_y = HEIGHT // 2 + earth_radius * math.sin(earth_angle)

    moon_x = earth_x + moon_radius * math.cos(moon_angle)
    moon_y = earth_y + moon_radius * math.sin(moon_angle)

    # Draw the Sun, Earth, and Moon
    pygame.draw.circle(screen, SUN_COLOR, (WIDTH // 2, HEIGHT // 2), 40)
    pygame.draw.circle(screen, EARTH_COLOR, (int(earth_x), int(earth_y)), 10)
    pygame.draw.circle(screen, MOON_COLOR, (int(moon_x), int(moon_y)), 5)

    # Check for a winning condition (e.g., when the moon completes an orbit)
    if moon_angle >= 2 * math.pi:
        you_win = True

    if you_win:
        # Display "You Win" text
        text = font.render("You Win!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 8, HEIGHT //10))
        font = pygame.font.Font(None, 70)
        screen.blit(text, text_rect)




    pygame.display.flip()
    clock.tick(60)

pygame.quit()