import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
DARK_BLUE = (0, 0, 128)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Eclipse-rise of Phoenix")

# Load background images for the initial screen and gameplay
background_start = pygame.image.load("backgrounds/start_background.png")
background_start = pygame.transform.scale(background_start, (WIDTH, HEIGHT))

background_gameplay = pygame.image.load("backgrounds/gameplay_background.jpg")
background_gameplay = pygame.transform.scale(background_gameplay, (WIDTH, HEIGHT))

# Load and resize the updated spaceship image
spaceship = pygame.image.load("assets/ship1.png")
spaceship = pygame.transform.scale(spaceship, (50, 50))
spaceship_rect = spaceship.get_rect()
spaceship_rect.center = (WIDTH // 2, HEIGHT - 50)

# Load and resize multiple obstacle images (excluding the moon)
obstacles = [
    pygame.image.load("obstacles/obstacle1.png"),
    pygame.image.load("obstacles/obstacle2.png"),
    pygame.image.load("obstacles/obstacle3.png"),
    pygame.image.load("obstacles/obstacle4.png"),
    pygame.image.load("obstacles/obstacle5.png"),
]

obstacle_size = (50, 50)
obstacles = [pygame.transform.scale(obstacle, obstacle_size) for obstacle in obstacles]


class Obstacle:
    def __init__(self, x, y, speed):
        self.image = random.choice(obstacles)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed


obstacles_list = []

# Game variables
running = True
game_started = False
instruction_displayed = False
obstacle_spawn_rate = 40
obstacle_spawn_delay = 1.0
last_spawn_time = 0
spaceship_speed = 0.65
obstacle_speed = 0.500001
won = False
lost = False
show_oops_message = False
oops_message_timer = None
OOPS_MESSAGE_DELAY = 3
moon = None
trivia_question_displayed = False
moon_appearance_time = None
moon_rect = None
level_2_started = False
correct_answer_selected_time = None

# Trivia questions and options
trivia_questions = [
    "What do you understand by an eclipse?",
    "When does a Lunar Eclipse occur?",
    "During a total lunar eclipse, the Moon appears to:",
    "How often does a total solar eclipse occur at a given location on Earth on average?",
    "What causes a seasonal eclipse to occur?"
]

trivia_options = [
    [
        "A. Partial or total blocking of light of one celestial object by another.",
        "B. Partial or total blocking of light by the Moon.",
        "C. Partial or total blocking of light by the Earth.",
        "D. Partial or total blocking of light by the Sun."
    ],
    [
        "A. When Sun is between Earth and Moon",
        "B. When Earth is between Sun and Moon",
        "C. When Moon is between Earth and Sun",
        "D. When Earth is between Sun and other celestial bodies"
    ],
    [
        "A. Disappear completely",
        "B. Turn blue",
        "C. Turn red or coppery",
        "D. Emit a bright white light"
    ],
    [
        "A) About once a month",
        "B) About once a year",
        "C) About once every 10 years",
        "D) About once every 100 years"
    ],
    [
        "A) The Earth's shadow falls on the Moon, creating a lunar eclipse.",
        "B) The Moon's shadow falls on the Earth, creating a solar eclipse.",
        "C) The alignment of the Sun, Moon, and Earth in a straight line.",
        "D) The tilt of the Earth's axis and its orbit around the Sun."
    ]
]

correct_answers = ["A", "B", "C", "C", "D"]

moon_landings = 0
current_question = 0
correct_answer_selected = False
selected_option = None
current_question_set = 0
current_question_set_2 = len(trivia_questions)
congrats_message = ""
TEXT_BOX_DELAY = 3
TEXT_BOX_FONT = pygame.font.Font(None, 36)
TEXT_BOX_COLOR = (255, 255, 255)
text_box_timer = None
text_box_message = ""

# Add a variable to track the player's score
score = 0


def display_text_box(message):
    global text_box_timer, text_box_message
    text_box_message = message
    text_box_timer = time.time() + TEXT_BOX_DELAY


# Custom function to draw text with a glow
def draw_text_with_glow(surface, text, font, text_color, glow_color, pos):
    # Create a text surface with the given color
    text_surface = font.render(text, True, text_color)

    # Create a glow surface with an outline around the text
    glow_surface = pygame.Surface((text_surface.get_width() + 12, text_surface.get_height() + 12), pygame.SRCALPHA)
    pygame.draw.rect(glow_surface, glow_color, (0, 0, glow_surface.get_width(), glow_surface.get_height()))
    glow_surface.blit(text_surface, (6, 6))  # Offset the text within the glow surface

    # Blit the glow surface onto the main surface
    surface.blit(glow_surface, pos)


def display_trivia_question():
    global current_question, current_question_set, current_question_set_2

    if current_question_set < len(trivia_questions):
        questions_to_display = trivia_questions[current_question_set:current_question_set_2]
    else:
        questions_to_display = []

    text_y = HEIGHT // 2 - 100
    pygame.draw.rect(screen, (0, 0, 0), (50, text_y, WIDTH - 100, 220))
    pygame.draw.rect(screen, DARK_BLUE, (50, text_y, WIDTH - 100, 220), 3)
    trivia_font = pygame.font.Font(None, 24)

    if current_question < len(questions_to_display):
        question_surface = trivia_font.render(questions_to_display[current_question], True, (255, 255, 255))
        screen.blit(question_surface, (WIDTH // 2 - question_surface.get_width() // 2, text_y + 20))

        option_font = pygame.font.Font(None, 20)
        option_y = text_y + 80

        for i, option in enumerate(trivia_options[current_question_set + current_question], start=1):
            option_surface = option_font.render(option, True, (255, 255, 255))
            screen.blit(option_surface, (WIDTH // 2 - option_surface.get_width() // 2, option_y))
            option_y += 30


def display_congratulatory_message():
    global moon_landings, current_question, correct_answer_selected, second_moon_landing, congrats_message, fourth_moon_landing

    if moon_landings == 0:
        congrats_message = "Congrats, You landed on the moon. Let's see how much you know about eclipses."
    elif moon_landings == 1:
        congrats_message = "Congrats, You landed on the moon again. Let's continue to test your knowledge. Ready or not here we go."
        current_question = 1
    elif moon_landings == 2:
        congrats_message = "Congrats, You're really getting the hang of this game. Next Question!"
        current_question += 1
    elif moon_landings == 3:
        congrats_message = "Bet the obstacles are getting more difficult to dodge. No worries, We've only got one more to go."
        current_question += 1
    elif moon_landings == 4:
        congrats_message = "WOOHOO! You did it! Last Question"
        current_question += 1
    text_font = pygame.font.Font(None, 24)
    text_surface = text_font.render(congrats_message, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.center = (WIDTH // 2, HEIGHT // 2)
    screen.blit(text_surface, text_rect)


def display_wrong_answer_message():
    wrong_text = "Wrong Answer! Better luck next time."
    text_font = pygame.font.Font(None, 24)
    text_surface = text_font.render(wrong_text, True, (255, 0, 0))  # Red color for wrong answer
    text_rect = text_surface.get_rect()
    text_rect.center = (WIDTH // 2, HEIGHT // 2)
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()


def display_final_congratulatory_message():
    final_message = "Congratulations! You've won the game and reached the end."
    score_message = f"Your final score is: {score}"
    enjoy_message = "We hope you enjoyed playing!"

    final_font = pygame.font.Font(None, 36)
    final_surface = final_font.render(final_message, True, (255, 255, 255))
    score_surface = final_font.render(score_message, True, (255, 255, 255))
    enjoy_surface = final_font.render(enjoy_message, True, (255, 255, 255))

    final_rect = final_surface.get_rect()
    score_rect = score_surface.get_rect()
    enjoy_rect = enjoy_surface.get_rect()

    final_rect.center = (WIDTH // 2, HEIGHT // 2 - 50)
    score_rect.center = (WIDTH // 2, HEIGHT // 2)
    enjoy_rect.center = (WIDTH // 2, HEIGHT // 2 + 50)

    screen.blit(final_surface, final_rect)
    screen.blit(score_surface, score_rect)
    screen.blit(enjoy_surface, enjoy_rect)


# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_started:
        screen.blit(background_start, (0, 0))
    else:
        screen.blit(background_gameplay, (0, 0))

    keys = pygame.key.get_pressed()

    if not game_started:
        if not instruction_displayed:
            instruction_text = [
                "Space Eclipse Game",
                "Instructions:",
                "Use the left and right arrow keys to move the spaceship.",
                "Use the up and down arrow keys to move forward and backward.",
                "Land on the moon."
                "Avoid the incoming obstacles.",
                "Press any key to start."
            ]
            y_offset = 50
            for line in instruction_text:
                instruction_line = pygame.font.Font(None, 36).render(line, True, (255, 105, 180))
                screen.blit(instruction_line, (WIDTH // 2 - instruction_line.get_width() // 2, HEIGHT // 2 - y_offset))
                y_offset -= 40

            if any(keys):
                game_started = True
                instruction_displayed = True
                moon_appearance_time = time.time() + 10
                lost = False

        else:
            start_text = pygame.font.Font(None, 36).render("Press any key to start", True, (0, 0, 0))
            screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 50))

    if game_started and not won and not lost:
        if keys[pygame.K_LEFT]:
            spaceship_rect.x -= spaceship_speed
            if spaceship_rect.left < 0:
                spaceship_rect.left = 0
        if keys[pygame.K_RIGHT]:
            spaceship_rect.x += spaceship_speed
            if spaceship_rect.right > WIDTH:
                spaceship_rect.right = WIDTH
        if keys[pygame.K_UP]:
            spaceship_rect.y -= spaceship_speed
            if spaceship_rect.top < 0:
                spaceship_rect.top = 0
        if keys[pygame.K_DOWN]:
            spaceship_rect.y += spaceship_speed
            if spaceship_rect.bottom > HEIGHT:
                spaceship_rect.bottom = HEIGHT

        screen.blit(spaceship, spaceship_rect)

        current_time = time.time()
        if current_time - last_spawn_time > obstacle_spawn_delay:
            if random.randint(0, 100) < obstacle_spawn_rate:
                x = random.randint(0, WIDTH - obstacle_size[0])
                y = random.randint(-200, -100)
                speed = obstacle_speed
                obstacle = Obstacle(x, y, speed)
                obstacles_list.append(obstacle)
                last_spawn_time = current_time

        buffer_distance = 10
        for obstacle in obstacles_list:
            obstacle.rect.y += obstacle.speed
            screen.blit(obstacle.image, obstacle.rect)

            if spaceship_rect.colliderect(obstacle.rect.inflate(-buffer_distance, -buffer_distance)):
                show_oops_message = True
                oops_message_timer = time.time() + OOPS_MESSAGE_DELAY
                score -= 0.005

    if show_oops_message:
        oops_text = "Ooops! No Problem!"
        text_font = pygame.font.Font(None, 36)
        text_surface = text_font.render(oops_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (WIDTH // 2, HEIGHT // 2)
        screen.blit(text_surface, text_rect)

        if time.time() > oops_message_timer:
            show_oops_message = False

    if game_started and moon is None and time.time() >= moon_appearance_time:
        moon = pygame.image.load("win/moon.png")
        moon = pygame.transform.scale(moon, (50, 50))
        moon_rect = moon.get_rect()
        moon_rect.x = random.randint(0, WIDTH - moon_rect.width)
        moon_rect.y = random.randint(0, HEIGHT - moon_rect.height)

    if moon is not None:
        screen.blit(moon, moon_rect)

        if spaceship_rect.colliderect(moon_rect):
            display_congratulatory_message()
            pygame.display.flip()
            time.sleep(5)

            # Increase the score when landing on the moon
            score += 20

            moon_landings += 1

            if moon_landings == 2:
                second_moon_landing = True
                moon = None
                moon_appearance_time = time.time() + 25
                obstacle_spawn_rate += 30
                obstacle_speed += 0.05

            if moon_landings == 3:
                third_moon_landing = True
                moon = None
                moon_appearance_time = time.time() + 25
                obstacle_spawn_rate += 18
                obstacle_speed += 0.05
                obstacle_spawn_delay -= 0.2

            if moon_landings == 4:
                fourth_moon_landing = True
                moon = None
                moon_appearance_time = time.time() + 30
                obstacle_spawn_rate += 20
                obstacle_speed += 0.05
                obstacle_spawn_delay -= 0.4

            # Reset game state
            won = True
            level_2_started = False
            moon = None

    if lost:
        loss_message = pygame.font.Font(None, 48).render("Sorry, You lost. Restart from level 1.", True, DARK_BLUE)
        screen.blit(loss_message, (WIDTH // 2 - loss_message.get_width() // 2, HEIGHT // 2 - 50))
        pygame.display.flip()

        key_pressed = False
        while not key_pressed:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    key_pressed = True

        game_started = False
        instruction_displayed = False
        obstacles_list = []
        moon = None
        won = False

    if won:
        if not level_2_started:
            level_2_started = True

        if not trivia_question_displayed:
            display_trivia_question()
            keys = pygame.key.get_pressed()
            if any(keys):
                if keys[pygame.K_a]:
                    selected_option = "A"
                elif keys[pygame.K_b]:
                    selected_option = "B"
                elif keys[pygame.K_c]:
                    selected_option = "C"
                elif keys[pygame.K_d]:
                    selected_option = "D"

            if selected_option is not None:
                trivia_question_displayed = True
                if selected_option == correct_answers[current_question]:
                    correct_answer_selected = True
                    correct_answer_selected_time = time.time()
                    selected_option = None
                    if current_question == 0:
                        moon_appearance_time = time.time() + 20
                    elif current_question == 1:
                        moon_appearance_time = time.time() + 20
                    elif current_question == 2:
                        moon_appearance_time = time.time() + 20
                    else:
                        moon_appearance_time = time.time() + 20
                    won = False
                    level_2_started = False
                    trivia_question_displayed = False
                    moon = None
                else:
                    display_wrong_answer_message()

    if correct_answer_selected:
        current_time = time.time()
        if current_question == 4 :
            if current_time - correct_answer_selected_time > 5:
                final_message = f"Congratulations! You've won the game with a score of {score}. We hope you enjoyed it."
                final_message_font = pygame.font.Font(None, 25)
                final_message_surface = final_message_font.render(final_message, True, (217, 156, 217))
                final_message_rect = final_message_surface.get_rect()
                final_message_rect.center = (WIDTH // 2, HEIGHT // 2)
                screen.blit(final_message_surface, final_message_rect)
                pygame.display.flip()
                time.sleep(5)
                exit()

        elif current_time - correct_answer_selected_time < 5:
            congrats_text = "Woohoo! Correct Ans. Continue to the next level."
            text_font = pygame.font.Font(None, 24)
            text_surface = text_font.render(congrats_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            text_rect.center = (WIDTH // 2, HEIGHT // 2)
            screen.blit(text_surface, text_rect)
        else:
            correct_answer_selected = False





    score_text = f"Score: {score}"
    score_font = pygame.font.Font(None, 24)
    score_surface = score_font.render(score_text, True, (255, 255, 255))
    score_rect = score_surface.get_rect()
    score_rect.topleft = (WIDTH - 150, 10)
    screen.blit(score_surface, score_rect)

    pygame.display.flip()


pygame.quit()
sys.exit()
