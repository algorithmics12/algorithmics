import pygame
import math
import random

pygame.init()

# =========================
# WINDOW
# =========================

WIDTH = 1400
HEIGHT = 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Football AI Simulation")

clock = pygame.time.Clock()

# =========================
# COLORS
# =========================

GREEN = (40, 140, 80)
WHITE = (255, 255, 255)
BLUE = (50, 100, 255)
RED = (255, 70, 70)
YELLOW = (255, 230, 50)
BLACK = (20, 20, 20)

# =========================
# SCORE
# =========================

blue_score = 0
red_score = 0

# =========================
# BALL
# =========================

BALL_RADIUS = 9

ball_x = WIDTH // 2
ball_y = HEIGHT // 2

ball_vel_x = 0
ball_vel_y = 0

ball_owner = None

# =========================
# FONT
# =========================

font = pygame.font.SysFont("arial", 34)

# =========================
# PLAYER CLASS
# =========================

class Player:

    def __init__(self, x, y, color, side, role):

        self.x = x
        self.y = y

        self.home_x = x
        self.home_y = y

        self.color = color
        self.side = side
        self.role = role

        self.radius = 13

        self.speed = random.uniform(1.5, 2.2)

        self.has_ball = False

    def move_towards(self, target_x, target_y):

        dx = target_x - self.x
        dy = target_y - self.y

        distance = math.sqrt(dx * dx + dy * dy)

        if distance > 0:

            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

    def update(self):

        global ball_owner
        global ball_x
        global ball_y
        global ball_vel_x
        global ball_vel_y

        # =====================
        # IF PLAYER HAS BALL
        # =====================

        if self.has_ball:

            # Dribble forward

            if self.side == "left":
                target_x = self.x + 80
            else:
                target_x = self.x - 80

            target_y = self.y

            self.move_towards(target_x, target_y)

            # Ball follows player
            ball_x = self.x
            ball_y = self.y

            # PASS
            if random.randint(1, 100) < 2:

                teammate = random.choice(
                    blue_team if self.side == "left"
                    else red_team
                )

                if teammate != self:

                    dx = teammate.x - self.x
                    dy = teammate.y - self.y

                    distance = math.sqrt(dx * dx + dy * dy)

                    if distance > 0:

                        power = 8

                        ball_vel_x = (dx / distance) * power
                        ball_vel_y = (dy / distance) * power

                        self.has_ball = False
                        ball_owner = None

            # SHOOT
            if (
                (self.side == "left" and self.x > 1100)
                or
                (self.side == "right" and self.x < 300)
            ):

                target_goal_y = random.randint(320, 480)

                if self.side == "left":
                    target_goal_x = WIDTH
                else:
                    target_goal_x = 0

                dx = target_goal_x - self.x
                dy = target_goal_y - self.y

                distance = math.sqrt(dx * dx + dy * dy)

                if distance > 0:

                    power = 14

                    ball_vel_x = (dx / distance) * power
                    ball_vel_y = (dy / distance) * power

                    self.has_ball = False
                    ball_owner = None

        # =====================
        # NO BALL
        # =====================

        else:

            # Closest player presses
            if self == get_closest_player(self.side):

                self.move_towards(ball_x, ball_y)

            else:

                # Hold formation
                self.move_towards(
                    self.home_x,
                    self.home_y
                )

            # Take possession
            distance = math.sqrt(
                (ball_x - self.x) ** 2
                + (ball_y - self.y) ** 2
            )

            if distance < 18 and ball_owner is None:

                self.has_ball = True
                ball_owner = self

    def draw(self):

        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x), int(self.y)),
            self.radius
        )

        # Ball possession indicator
        if self.has_ball:

            pygame.draw.circle(
                screen,
                YELLOW,
                (int(self.x), int(self.y - 22)),
                5
            )

# =========================
# CREATE TEAMS
# =========================

blue_team = []
red_team = []

# 4-3-3 formation

blue_positions = [

    (100, 400, "GK"),

    (250, 150, "DEF"),
    (250, 300, "DEF"),
    (250, 500, "DEF"),
    (250, 650, "DEF"),

    (500, 220, "MID"),
    (500, 400, "MID"),
    (500, 580, "MID"),

    (850, 220, "ATT"),
    (850, 400, "ATT"),
    (850, 580, "ATT")
]

red_positions = [

    (1300, 400, "GK"),

    (1150, 150, "DEF"),
    (1150, 300, "DEF"),
    (1150, 500, "DEF"),
    (1150, 650, "DEF"),

    (900, 220, "MID"),
    (900, 400, "MID"),
    (900, 580, "MID"),

    (550, 220, "ATT"),
    (550, 400, "ATT"),
    (550, 580, "ATT")
]

for pos in blue_positions:

    blue_team.append(
        Player(
            pos[0],
            pos[1],
            BLUE,
            "left",
            pos[2]
        )
    )

for pos in red_positions:

    red_team.append(
        Player(
            pos[0],
            pos[1],
            RED,
            "right",
            pos[2]
        )
    )

# =========================
# GET CLOSEST PLAYER
# =========================

def get_closest_player(side):

    team = blue_team if side == "left" else red_team

    closest = None
    closest_distance = 999999

    for player in team:

        if player.role == "GK":
            continue

        distance = math.sqrt(
            (ball_x - player.x) ** 2
            + (ball_y - player.y) ** 2
        )

        if distance < closest_distance:

            closest_distance = distance
            closest = player

    return closest

# =========================
# DRAW FIELD
# =========================

def draw_field():

    screen.fill(GREEN)

    pygame.draw.rect(
        screen,
        WHITE,
        (40, 40, WIDTH - 80, HEIGHT - 80),
        5
    )

    pygame.draw.line(
        screen,
        WHITE,
        (WIDTH // 2, 40),
        (WIDTH // 2, HEIGHT - 40),
        5
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (WIDTH // 2, HEIGHT // 2),
        90,
        5
    )

    # Goals
    pygame.draw.rect(
        screen,
        WHITE,
        (0, 300, 40, 200)
    )

    pygame.draw.rect(
        screen,
        WHITE,
        (WIDTH - 40, 300, 40, 200)
    )

# =========================
# BALL MOVEMENT
# =========================

def move_ball():

    global ball_x
    global ball_y
    global ball_vel_x
    global ball_vel_y
    global blue_score
    global red_score
    global ball_owner

    if ball_owner is None:

        ball_x += ball_vel_x
        ball_y += ball_vel_y

        ball_vel_x *= 0.98
        ball_vel_y *= 0.98

    # Bounce top/bottom
    if ball_y < 50:

        ball_y = 50
        ball_vel_y *= -1

    if ball_y > HEIGHT - 50:

        ball_y = HEIGHT - 50
        ball_vel_y *= -1

    # LEFT GOAL
    if ball_x <= 40:

        if 300 <= ball_y <= 500:

            red_score += 1
            reset()

        else:

            ball_x = 40
            ball_vel_x *= -1

    # RIGHT GOAL
    if ball_x >= WIDTH - 40:

        if 300 <= ball_y <= 500:

            blue_score += 1
            reset()

        else:

            ball_x = WIDTH - 40
            ball_vel_x *= -1

# =========================
# RESET
# =========================

def reset():

    global ball_x
    global ball_y
    global ball_vel_x
    global ball_vel_y
    global ball_owner

    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2

    ball_vel_x = 0
    ball_vel_y = 0

    ball_owner = None

    for player in blue_team:

        player.x = player.home_x
        player.y = player.home_y
        player.has_ball = False

    for player in red_team:

        player.x = player.home_x
        player.y = player.home_y
        player.has_ball = False

# =========================
# DRAW BALL
# =========================

def draw_ball():

    pygame.draw.circle(
        screen,
        YELLOW,
        (int(ball_x), int(ball_y)),
        BALL_RADIUS
    )

# =========================
# DRAW SCORE
# =========================

def draw_score():

    text = font.render(
        str(blue_score)
        + " - "
        + str(red_score),
        True,
        WHITE
    )

    screen.blit(
        text,
        (
            WIDTH // 2 - text.get_width() // 2,
            10
        )
    )

# =========================
# MAIN LOOP
# =========================

running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    # Update players
    for player in blue_team:
        player.update()

    for player in red_team:
        player.update()

    # Ball physics
    move_ball()

    # Draw
    draw_field()

    for player in blue_team:
        player.draw()

    for player in red_team:
        player.draw()

    draw_ball()

    draw_score()

    pygame.display.flip()

pygame.quit()