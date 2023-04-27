import pygame
from sys import exit
import time

pygame.init()

WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My-Special-Classroom")
clock = pygame.time.Clock()
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class App:
    def __init__(self):
        self.gameState = 'main menu'


class Button:

    def __init__(self, pos, width, height, color):
        self.surf = pygame.Surface((width, height))
        self.color = color
        self.surf.set_colorkey(BLACK)
        self.rect = self.surf.get_rect(center=pos)
        pygame.draw.ellipse(self.surf, self.color, (0, self.surf.get_height()/2, self.surf.get_width(), self.surf.get_height()/100 * 1))

        self.clickStage = None
        self.held = False

    def draw(self):
        screen.blit(self.surf, self.rect)

    def logic(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.clickStage = 0
            self.surf.fill((255, 0, 0))
            if pygame.mouse.get_pressed()[0]:
                self.held = True
                self.surf.fill((0, 255, 0))
            if self.held and not pygame.mouse.get_pressed()[0]:
                self.clickStage = 1

        else:
            self.clickStage = False
            self.held = False
            #pygame.draw.ellipse(self.surf, self.color, (0, self.surf.get_height()/2, self.surf.get_width(), self.surf.get_height()/100 * 50))

    def update(self):
        self.logic()
        self.draw()


b = Button((200, 500), 200, 100, WHITE)
app = App()
while 1:
    clock.tick(FPS)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()


    if app.gameState == 'main menu':
        screen.fill(BLACK)

        b.update()

    pygame.display.update()

