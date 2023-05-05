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

clockimg = pygame.image.load('resources/clock/clock.png').convert_alpha()
clock_time_font = pygame.font.SysFont('gadugi', 35, True, False)

toolBarSurf = pygame.Surface((150, 900))
toolBarSurf.fill((67, 67, 67))
toolBarRect = toolBarSurf.get_rect(topleft=(0, 0))

syringeimg = pygame.image.load('resources/tools/syringe.png').convert_alpha()


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
    def __init__(self, student_positions, student_time_range, lv_time):
        self.students = set()
        for pos in student_positions:
            self.students.add(Student(pos, student_time_range))

        self.timer = lv_time
        self.start_time = time.time()

        self.watch = Watch((1150, 100), 5, 10)



    def logic(self):
        for student in self.students:
            student.update()
        self.watch.change_time()
        self.watch.show_time()


class Watch:
    def __init__(self, pos, stime, etime):
        self.surf = clockimg
        self.stime = stime
        self.etime = etime
        self.rect = self.surf.get_rect(center=pos)
        self.txt = clock_time_font.render(f'{self.stime}am', True, (255, 0, 0))
        self.txtrect = self.txt.get_rect(center=self.rect.center)

        self.dt = 0
        self.startTime = time.time()


    def show_time(self):
        screen.blit(self.surf, self.rect)
        screen.blit(self.txt, self.txtrect)

    def change_time(self):
        if int((time.time() - self.startTime)) >= 60:
            self.dt += 1
            self.startTime = time.time()
        self.txt = clock_time_font.render(f'{self.stime + self.dt}am', True, (255, 0, 0))
        self.txtrect = self.txt.get_rect(center=self.rect.center)


class Student:
    def __init__(self, pos, timer):
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

    def update(self):
        self.timer()
        screen.blit(self.image, self.rect)


class Tool:
    def __init__(self, img, y):
        self.surf = img
        self.rect = self.surf.get_rect(topleft=(10, y))

    def draw(self):
        screen.blit(self.surf, self.rect)

    def drag(self):
        if pygame.mouse.get_pressed()[1] and self.rect.collidepoint(pygame.mouse.get_pos()):
            ...


syringe = Tool(syringeimg, 50)


lv1 = Level([(400, 600), (500, 600), (600, 600), (700, 600)], (3, 8), 200)
s = Student((WIDTH/2, HEIGHT/2), (3, 8))


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
        screen.blit(toolBarSurf, toolBarRect)

        if app.gameState == 'lv1':
            lv1.logic()
            syringe.draw()


    mouse.update()
    pygame.display.update()

