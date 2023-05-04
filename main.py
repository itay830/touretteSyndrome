import pygame
import time
import random
from sys import exit


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

standimg = pygame.image.load('resources/student/student_stand.png').convert_alpha()
sickimg = pygame.image.load('resources/student/sick_student.png').convert_alpha()


class App:
    def __init__(self):
        self.gameState = 'main menu'

    @staticmethod
    def regular_events():
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()


class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = [pygame.image.load('resources/mouse/arrow.png').convert_alpha(), pygame.image.load('resources/mouse/hand.png').convert_alpha()]
        self.image = self.images[0]
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.topleft = pygame.mouse.get_pos()
        if self.rect.colliderect(b) and app.gameState == 'main menu' or self.rect.colliderect(lv1_b) and app.gameState == 'level menu':
            self.image = self.images[1]
        else:
            self.image = self.images[0]
        screen.blit(self.image, self.rect)

mouse = Mouse()



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




class Level:
    def __init__(self, students):
        self.students = students
        self.spriteGroup = pygame.sprite.Group()
        for student in self.students:
            self.spriteGroup.add(student)

    def draw_students(self):
        self.spriteGroup.draw(screen)


class Student(pygame.sprite.Sprite):
    def __init__(self, pos, timer):
        super().__init__()
        self.image = standimg

        self.rect = self.image.get_rect(center=pos)
        self.timerRange = timer
        self.symptomDelay = random.randint(self.timerRange[0], self.timerRange[1])
        self.curedTime = time.time()

    def symptoms_showing(self):
        self.image = sickimg
        self.rect = self.image.get_rect(center=self.rect.center)
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
            self.cured()

    def cured(self):
        self.curedTime = time.time()
        self.symptomDelay = random.randint(self.timerRange[0], self.timerRange[1])
        self.image = standimg
        self.rect = self.image.get_rect(center=self.rect.center)

    def timer(self):
        if time.time() - self.curedTime > self.symptomDelay:
            self.symptoms_showing()

    def draw(self):
        screen.blit(self.image, self.rect)
        self.timer()





#lv1 = Level([Student(pos, (3, 8)) for pos in [(400, 600), (500, 600), (600, 600), (700, 600)]])

student = Student((WIDTH/2, HEIGHT/2), (3, 7))

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
            #lv1.draw_students()
            student.draw()


    mouse.update()
    pygame.display.update()

