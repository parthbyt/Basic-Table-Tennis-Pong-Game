import pygame
pygame.init()

from pygame.locals import (
    K_UP,
    K_DOWN,
    QUIT,
    RLEACCEL
)


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.surf = pygame.image.load("Ball.png")
        self.surf = pygame.transform.scale(self.surf, (40, 40))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.center = [250, 250]
        self.direction = [1, 1]
        self.speed = 2

    def update(self):
        self.dx = self.direction[0]
        self.dy = self.direction[1]
        self.rect.move_ip(self.speed * self.dx, self.speed * self.dy)

        if self.rect.right >= 500 or self.rect.left <= 0:
            self.direction[0] = -self.dx
            self.direction[1] = self.dy
        if self.rect.bottom >= 500 or self.rect.top <= 0:
            self.direction[0] = self.dx
            self.direction[1] = -self.dy
    
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("Racket.png")
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.surf = pygame.transform.scale(self.surf, (60, 120))
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)

        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom > 500:
            self.rect.bottom = 500

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("Racket.png")
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.surf = pygame.transform.scale(self.surf, (60, 120))
        self.surf = pygame.transform.flip(self.surf, True, False)
        self.rect = self.surf.get_rect()
        self.rect.center = (460, 0)

    def update(self, y_coordinate):
        self.rect.center = (480, y_coordinate)
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom > 500:
            self.rect.bottom = 500

class Defender(pygame.sprite.Sprite):
    def __init__(self):
        super(Defender, self).__init__()
        self.surf = pygame.Surface((5, 1000))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect()
        self.rect.center = (0, 0)

screen = pygame.display.set_mode([500, 500])

pygame.display.set_caption('Table Tennis Pong')

ball = Ball()

player = Player()

enemy = Enemy()

defender = Defender()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(ball)
all_sprites.add(enemy)
all_sprites.add(defender)

clock = pygame.time.Clock()

font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('Game Over', True, (255, 0, 0), (255, 255, 255) )
textRect = text.get_rect()
textRect.center = (250, 250)

bg = pygame.image.load("Board.png")
bg = pygame.transform.scale(bg, (500, 500))

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    screen.blit(bg, (0, 0))
    
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    enemy.update(ball.rect.center[1])
    
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    ball.update()

    if pygame.sprite.collide_rect(ball, enemy) or pygame.sprite.collide_rect(ball, player):
        ball.direction[0] = -ball.dx
        ball.direction[1] = ball.dy

    if pygame.sprite.collide_rect(ball, defender):
        screen.blit(text, textRect)
        running = False

    pygame.display.flip()

pygame.quit()
