import pygame
from sys import exit
import time

pygame.init()

WIDTH, HEIGHT = 1400, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My-Special-Classroom")
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CENTER = (WIDTH/2, HEIGHT/2)
classroomBg = pygame.image.load('resources/bgs/classroom.png').convert_alpha()

mouse_current_img = mouseArrow = pygame.image.load('resources/mouse/arrow.png').convert_alpha()
mouseHand = pygame.image.load('resources/mouse/hand.png').convert_alpha()

class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = [pygame.image.load('resources/mouse/arrow.png').convert_alpha(), pygame.image.load('resources/mouse/hand.png').convert_alpha()]
        self.rect = self.images[0].get_rect()

    def update(self):
        self.rect.topleft = pygame.mouse.get_pos()
        screen.blit(self.image, self.rect)

mouse = Mouse()

class App:
    def __init__(self):
        self.gameState = 'main menu'

    @staticmethod
    def regular_events():
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()






class Button:

    def __init__(self, pos, width, height):
        self.surf = pygame.Surface((width, height))
        self.surf.set_colorkey(BLACK)
        self.rect = self.surf.get_rect(center=pos)

        self.clickStage = None
        self.held = False

    def draw(self):
        screen.blit(self.surf, self.rect)

    def logic(self):
        if self.rect.colliderect(mouse.rect):
            self.clickStage = False
            self.surf.fill((255, 0, 0))
            if pygame.mouse.get_pressed()[0]:
                self.held = True
                self.surf.fill((0, 255, 0))
            if self.held and not pygame.mouse.get_pressed()[0]:
                self.clickStage = True

        else:
            self.clickStage = False
            self.held = False
            self.surf.fill((255, 0, 255))

    def update(self):
        self.logic()
        self.draw()




b = Button(CENTER, 200, 100)
lv1_b = Button((150, 100), 200, 100)

app = App()
while 1:
    clock.tick(FPS)
    app.regular_events()


    if app.gameState == 'main menu':
        screen.fill(BLACK)
        b.update()
        if b.clickStage:
            app.gameState = 'level menu'

    if app.gameState == 'level menu':
        screen.fill(BLACK)
        lv1_b.update()
        if lv1_b.clickStage:
            app.gameState = 'lv1'

    if app.gameState.startswith('lv'):
        screen.blit(classroomBg, (0, 0))
        if app.gameState == 'lv1':
            ...

    screen.blit(mouse_current_img, pygame.mouse.get_pos())
    pygame.display.update()

