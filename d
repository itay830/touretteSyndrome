import pygame
import time
import random
from math import sin, cos, atan2
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

toolBarSurf = pygame.Surface((200, 900))
toolBarSurf.fill((67, 67, 67))
toolBarRect = toolBarSurf.get_rect(topleft=(0, 0))

syringeimg = pygame.image.load('resources/tools/syringe.png').convert_alpha()

startimg = pygame.image.load('resources/buttons/start.png').convert_alpha()
optionsimg = pygame.image.load('resources/buttons/options.png').convert_alpha()
exitimg = pygame.image.load('resources/buttons/exit.png').convert_alpha()

rightArrowimg = pygame.image.load('resources/buttons/rightArrow.png').convert_alpha()
leftArrowimg = pygame.image.load('resources/buttons/leftArrow.png').convert_alpha()

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
        if False:
            self.image = self.images[1]
        else:
            self.image = self.images[0]
        screen.blit(self.image, self.rect)

mouse = Mouse()



class Button:

    def __init__(self, pos, img=None, radius=200):
        if img is not None:
            self.surf = img
        else:
            self.surf = pygame.Surface((radius*2.5, radius*2.5))
            pygame.draw.circle(self.surf, (67, 67, 67), (self.surf.get_width()/2, self.surf.get_height()/2), radius)

        self.surf.set_colorkey(BLACK)
        self.rect = self.surf.get_rect(center=pos)

        self.clickStage = None
        self.held = False

    def draw(self):
        screen.blit(self.surf, self.rect)

    def logic(self):
        if self.rect.colliderect(mouse.rect):
            self.clickStage = False
            if pygame.mouse.get_pressed()[0]:
                self.held = True
            if self.held and not pygame.mouse.get_pressed()[0]:
                self.clickStage = True
                self.held = False

        else:
            self.clickStage = False
            self.held = False

    def update(self):
        self.logic()
        self.draw()



levels = []
class Level:
    def __init__(self, student_positions, student_time_range, lv_time):
        self.name = f"lv{len(levels)+1}"
        self.students = set()
        for pos in student_positions:
            self.students.add(Student(pos, student_time_range))

        self.timer = lv_time
        self.start_time = time.time()

        self.watch = Watch((1150, 100), 5, 10)

        levels.append(self)



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
        self.sick = False

    def symptoms_showing(self):
        self.image = sickimg
        self.rect = self.image.get_rect(center=self.rect.center)
        self.sick = True

    def cured(self):
        self.curedTime = time.time()
        self.symptomDelay = random.randint(self.timerRange[0], self.timerRange[1])
        self.image = standimg
        self.rect = self.image.get_rect(center=self.rect.center)
        self.sick = False

    def timer(self):
        if time.time() - self.curedTime > self.symptomDelay:
            self.symptoms_showing()

    def update(self):
        self.timer()
        screen.blit(self.image, self.rect)


class Tool:
    def __init__(self, img, y):
        self.surf = img
        self.rect = self.surf.get_rect(center=(100, y))
        self.pos = (10, y)

        self.station = pygame.Surface((1, 1)).get_rect(center=(50, y))

        # Alternate method :
        self.station_pos = (100, y)
        self.dx = 0
        self.dy = 0
        self.jump_counter = 0
        self.steps = 10


        self.moveBack = False
        self.someoneCured = False

        self.hold = False
        self.dragPos = (10, y)
        self.mousex_in_rect = 0
        self.mousey_in_rect = 0

    def draw(self):
        screen.blit(self.surf, self.rect)

    def drag(self, students):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.hold = True

        if not pygame.mouse.get_pressed()[0]:
            self.hold = False
            self.moveBack = True

            # Alternate method :
            self.dx = (self.station_pos[0] - self.rect.centerx) / self.steps
            self.dy = (self.station_pos[1] - self.rect.centery) / self.steps


        if self.rect.collidepoint(mouse_pos) and not pygame.mouse.get_pressed()[0]:
            self.mousex_in_rect = self.rect.right - self.rect.left - (self.rect.right - mouse_pos[0])
            self.mousey_in_rect = self.rect.bottom - self.rect.top - (self.rect.bottom - mouse_pos[1])
            self.dragPos = pygame.mouse.get_pos()

        if self.hold and not self.moveBack:
            self.rect.x = self.dragPos[0] + (mouse_pos[0] - self.dragPos[0]) - self.mousex_in_rect
            self.rect.y = self.dragPos[1] + (mouse_pos[1] - self.dragPos[1]) - self.mousey_in_rect
        else:
            for student in students:
                if self.rect.colliderect(student.rect) and student.sick and not self.someoneCured:
                    student.cured()
                    self.moveBack = True

                    # Alternate method :
                    self.dx = (self.station_pos[0] - self.rect.centerx) / self.steps
                    self.dy = (self.station_pos[1] - self.rect.centery) / self.steps


                    self.someoneCured = True
                    break

            if self.rect.colliderect(self.station):
                self.moveBack = False
                self.someoneCured = False

            if self.moveBack:
                '''angle = atan2(self.pos[1] - self.rect.topleft[1], self.pos[0] - self.rect.topleft[0])
                dx = cos(angle)
                dy = sin(angle)
                self.rect.x += round(dx, 2) * 30
                self.rect.y += round(dy, 2) * 30'''

                # Alternate method :
                self.rect.x += self.dx
                self.rect.y += self.dy
                if self.jump_counter < steps - 1:
                    self.jump_counter += 1
                else:
                    self.jump_counter = 0


syringe = Tool(syringeimg, 50)


lv1 = Level([(400, 600), (500, 600), (600, 600), (700, 600)], (3, 8), 200)
lv2 = Level([(400, 800), (500, 600), (600, 600), (700, 600)], (3, 8), 200)
lv3 = Level([(400, 900), (500, 600), (600, 600), (700, 600)], (3, 8), 200)
lv4 = Level([(400, 900), (500, 600), (600, 600), (700, 600)], (3, 8), 200)
lv5 = Level([(400, 900), (500, 600), (600, 600), (700, 600)], (3, 8), 200)
lv6 = Level([(400, 900), (500, 600), (600, 600), (700, 600)], (3, 8), 200)

radius = 200
level_buttons = []
for x in range(len(levels)):
    level_buttons.append(Button((CENTER[0]+450*x, CENTER[1]), radius=radius))


startButton = Button((CENTER[0], CENTER[1] - 200), startimg)
optionsButton = Button((CENTER[0], CENTER[1]), optionsimg)
exitButton = Button((CENTER[0], CENTER[1] + 200), exitimg)

selectedLevel = 0
selectedRadius = 0
button_dx = 0
steps = 10
jumps_counter = 0
rightArrowButton = Button((WIDTH - 75, CENTER[1]), rightArrowimg)
leftArrowButton = Button((75, CENTER[1]), leftArrowimg)
arrowPass = True


def button_calc_dist():
    global selectedRadius
    selectedRadius = 0
    return False, 0, (CENTER[0] - level_buttons[selectedLevel].rect.centerx) / steps


app = App()
while 1:
    clock.tick(FPS)
    app.regular_events()

    if app.gameState == 'main menu':
        screen.fill(BLACK)
        startButton.update()
        optionsButton.update()
        exitButton.update()
        if startButton.clickStage:
            app.gameState = 'level menu'
        if optionsButton.clickStage:
            app.gameState = 'options'
        if exitButton.clickStage:
            pygame.quit()
            exit()

    if app.gameState == 'level menu':
        screen.fill(BLACK)



        if arrowPass:
            if rightArrowButton.clickStage and selectedLevel < len(levels) - 1:
                selectedLevel += 1
                arrowPass, jumps_counter, button_dx = button_calc_dist()

            elif rightArrowButton.clickStage:
                selectedLevel = 0
                arrowPass, jumps_counter, button_dx = button_calc_dist()

            if leftArrowButton.clickStage and selectedLevel > 0:
                selectedLevel -= 1
                arrowPass, jumps_counter, button_dx = button_calc_dist()

            elif leftArrowButton.clickStage:
                selectedLevel = len(levels) - 1
                arrowPass, jumps_counter, button_dx = button_calc_dist()

        for index, button in enumerate(level_buttons):
            button.rect.centerx += button_dx
            button.surf.fill(BLACK)

            if not level_buttons[selectedLevel] is button:
                pygame.draw.circle(button.surf, (67, 67, 67), (button.surf.get_width() / 2, button.surf.get_height() / 2), radius=radius)
            else:
                pygame.draw.circle(button.surf, (67, 67, 67), (button.surf.get_width() / 2, button.surf.get_height() / 2), radius=radius+selectedRadius)
            button.update()



        if not arrowPass:
            if jumps_counter == steps - 1:
                jumps_counter = 0
                button_dx = 0
                arrowPass = True
                selectedRadius += 25
            else:
                jumps_counter += 1
                level_buttons[selectedLevel].surf.fill(BLACK)

        if level_buttons[selectedLevel].clickStage:
            app.gameState = f'lv{selectedLevel+1}'

        rightArrowButton.update()
        leftArrowButton.update()
        pygame.draw.line(screen, (255, 0, 0), (WIDTH/2, 0), (WIDTH/2, HEIGHT))

    if app.gameState.startswith('lv'):
        screen.blit(classroomBg, (0, 0))
        screen.blit(toolBarSurf, toolBarRect)




        for level in levels:
            if app.gameState == level.name:
                level.logic()
                syringe.draw()
                syringe.drag(level.students)

    mouse.update()
    pygame.display.update()



