
import pygame
import random

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        image = pygame.image.load("cloud.png")
        self.surf = pygame.transform.scale(image, (75, 75))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    # Move the cloud based on a constant speed
    # Remove the cloud when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        image = pygame.image.load("bomb.png")
        self.surf = pygame.transform.scale(image, (25, 25))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        image = pygame.image.load("jet.png")
        self.surf = pygame.transform.scale(image, (50,50))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP] or pressed_keys[K_w]:
            self.rect.move_ip(0, -10)
        if pressed_keys[K_DOWN] or pressed_keys[K_s]:
            self.rect.move_ip(0, 10)
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.rect.move_ip(-10, 0)
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.rect.move_ip(10, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()

def game_intro():
    intro = True
    # button = pygame.Surface((200, 100))
    # button.fill(green)
    # button_rect = button.get_rect(center=(200, 400))
    button = pygame.draw.rect(screen, green, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 200, 100))
    while intro:
        button_color = (0,100,0)
        if button.collidepoint(pygame.mouse.get_pos()):
            button_color = green
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if button.collidepoint(pygame.mouse.get_pos()):
                    intro = False
            elif event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if (event.key == K_RETURN) or (event.key == K_SPACE):
                    intro = False

        screen.fill((255,255,255))
        largeText = pygame.font.Font('freesansbold.ttf', 80)
        TextSurf, TextRect = text_objects("Dodge the bombs", largeText)
        TextRect.center = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 4))

        # pygame.display.flip()
        button = pygame.draw.rect(screen,button_color,(SCREEN_WIDTH / 2,SCREEN_HEIGHT / 2,200,100))

        font = pygame.font.SysFont('Arial', 60)

        screen.blit(font.render('Start', True, black), (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 200, 100))
        screen.blit(TextSurf, TextRect)

        pygame.display.set_caption('Dodge the bombs')
        pygame.display.update()

        # screen.blit(button, button_rect)
        # for entity in buttons:
        #     screen.blit(entity.surf, entity.rect)


        clock.tick(30)

# Press the green button in the gutter to run the script.
def game_loop():
    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 250)

    ADDCLOUD = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDCLOUD, 1000)

    player = Player()

    enemies = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    # Run until the user asks to quit
    running = True
    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            elif event.type == ADDENEMY:
                # Create the new enemy and add it to sprite groups
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
            elif event.type == ADDCLOUD:
                # Create the new cloud and add it to sprite groups
                new_cloud = Cloud()
                clouds.add(new_cloud)
                all_sprites.add(new_cloud)

        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)

        # Update enemy position
        enemies.update()
        clouds.update()

        # Fill the background with white
        screen.fill((135, 206, 250))

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # Check if any enemies have collided with the player
        if pygame.sprite.spritecollideany(player, enemies):
            # If so, then remove the player and stop the loop
            player.kill()
            running = False
        # screen.blit(player.surf, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(player.surf, player.rect)

        pygame.display.flip()
        clock.tick(30)


from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_w,
    K_DOWN,
    K_s,
    K_LEFT,
    K_a,
    K_RIGHT,
    K_d,
    K_ESCAPE,
    KEYDOWN,
    K_RETURN,
    K_SPACE,
    QUIT,
)

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



clock = pygame.time.Clock()

done = False
while not done:
    game_intro()
    game_loop()
# Done! Time to quit.
pygame.quit()

