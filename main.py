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

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CENTER = (WIDTH/2, HEIGHT/2)

score_font = pygame.font.SysFont('verdana', 20, True)
msg_font = pygame.font.SysFont('Verdana', 200, True)
end_things_font = pygame.font.SysFont('Verdana', 80, True)

msg_pos = (CENTER[0], 200)
winMsg = msg_font.render('YOU WON', False, WHITE)
loseMsg = msg_font.render('YOU LOST', False, (255, 0, 0))
loseRect = loseMsg.get_rect(center=msg_pos)
winRect = winMsg.get_rect(center=msg_pos)
pause_surf = pygame.Surface((WIDTH, HEIGHT))
pause_surf.set_alpha(190)
pause_rect = pause_surf.get_rect(topleft=(0, 0))
end_menu = False


classroomBg = pygame.image.load('resources/bgs/classroom.png').convert_alpha()

stand_animation = [pygame.image.load(f'resources/student/student_stand_animation/sprite_{num}.png') for num in range(0, 4)]
voice_tick_animation = [pygame.image.load(f'resources/student/voice_tick_animation/sprite_{num}.png') for num in range(0, 4)]
motor_tick_animation = [pygame.image.load(f'resources/student/motor_tick_animation/sprite_{num}.png') for num in range(0, 4)]
eye_tick_animation = [pygame.image.load(f'resources/student/eyes_tick_animation/sprite_{num}.png') for num in range(0, 4)]
face_tick_animation = [pygame.image.load(f'resources/student/face_tick_animation/sprite_{num}.png') for num in range(0, 4)]
symptoms_ani = [voice_tick_animation, motor_tick_animation, eye_tick_animation, face_tick_animation]

clockimg = pygame.image.load('resources/clock/clock.png').convert_alpha()
clock_time_font = pygame.font.SysFont('gadugi', 35, True, False)

toolBarSurf = pygame.Surface((200, 900))
toolBarSurf.fill((67, 67, 67))
toolBarRect = toolBarSurf.get_rect(topleft=(0, 0))

syringeimg = pygame.image.load('resources/tools/syringe.png').convert_alpha()
haldolimg = pygame.image.load('resources/tools/haldol.png').convert_alpha()
clonidineimg = pygame.image.load('resources/tools/clonidine.png').convert_alpha()
pimozideimg = pygame.image.load('resources/tools/pimozide.png').convert_alpha()

startimg = pygame.image.load('resources/buttons/start.png').convert_alpha()
optionsimg = pygame.image.load('resources/buttons/options.png').convert_alpha()
exitimg = pygame.image.load('resources/buttons/exit.png').convert_alpha()
save_and_backimg = pygame.image.load('resources/buttons/save_and_back.png').convert_alpha()

rightArrowimg = pygame.image.load('resources/buttons/rightArrow.png').convert_alpha()
leftArrowimg = pygame.image.load('resources/buttons/leftArrow.png').convert_alpha()
backArrowimg = pygame.image.load('resources/buttons/back_arrow.png').convert_alpha()

heartFullimg = pygame.image.load('resources/heart/full_heart.png').convert_alpha()
heartEmptyimg = pygame.image.load('resources/heart/empty_heart.png').convert_alpha()

redSignimg = pygame.image.load('resources/signs/exclamation_mark.png').convert_alpha()

class App:
    def __init__(self):
        self.gameState = 'main menu'

    def regular_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()

            if e.type == pygame.KEYUP:
                if e.key == pygame.K_ESCAPE:
                    if self.gameState == 'main menu':
                        pygame.quit()
                        exit()

                    elif self.gameState == 'options' or self.gameState == 'level menu':
                        self.gameState = 'main menu'






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
    def __init__(self, student_positions, student_time_range, lv_time, hearts_num=5):
        self.name = f"lv{len(levels)+1}"
        self.students = set()
        self.hearts = []
        for pos in student_positions:
            self.students.add(Student(pos, student_time_range))
        for dx in range(hearts_num):
            self.hearts.append(Heart((300 + 105*dx, 50)))
        self.mistakes = len(self.hearts)
        self.timer = lv_time
        self.start_time = time.time()

        self.watch = Watch((1150, 100), 9)

        self.score = 0
        self.scoreTxt = clock_time_font.render(f'SCORE: {self.score}', True, (255, 255, 255))


        levels.append(self)

    def logic(self):
        global end_menu
        self.show_score()
        if not end_menu:
            self.watch.change_time()
        self.watch.show_time()

        for student in self.students:
            if not end_menu:
                student.update()
            else:
                student.draw()

        for index, heart in enumerate(self.hearts):
            if index+1 > self.mistakes:
                heart.img = heartEmptyimg
            else:
                heart.img = heartFullimg
            heart.draw()

        if self.mistakes <= 0:
            end_menu = True
            screen.blit(pause_surf, pause_rect)
            saveAndBackButton.update()
            screen.blit(loseMsg, loseRect)
            screen.blit(end_things_font.render(f"SCORE: {self.score}", True, (255, 255, 255)), (200, 300))
            screen.blit(end_things_font.render(f'TIME: {int(self.watch.endOfWorkTime - self.watch.startTime)}', True, (255, 255, 255)), (200, 400))
            if saveAndBackButton.clickStage:
                app.gameState = 'level menu'

        if int(self.watch.endOfWorkTime - self.watch.startTime) > self.timer:
            end_menu = True
            screen.blit(pause_surf, pause_rect)
            saveAndBackButton.update()
            screen.blit(winMsg, winRect)
            screen.blit(end_things_font.render(f"SCORE: {self.score}", True, (255, 255, 255)), (200, 300))
            screen.blit(end_things_font.render(f'TIME: {int(self.watch.endOfWorkTime - self.watch.startTime)}', True, (255, 255, 255)), (200, 400))
            if saveAndBackButton.clickStage:
                end_menu = False
                app.gameState = 'level menu'

    def show_score(self):
        self.scoreTxt = clock_time_font.render(f'SCORE: {self.score}', True, (255, 255, 255))
        self.rectTxt = self.scoreTxt.get_rect(center=(WIDTH-500, 60))
        screen.blit(self.scoreTxt, self.rectTxt)


class Watch:
    def __init__(self, pos, stime):
        self.surf = clockimg
        self.rect = self.surf.get_rect(center=pos)
        self.stime = stime
        self.txt = clock_time_font.render(f'{self.stime}am', True, (255, 0, 0))
        self.txtrect = self.txt.get_rect(center=self.rect.center)

        self.startTime = time.time()
        self.endOfWorkTime = time.time()
        self.timeLap = 60

    def show_time(self):
        screen.blit(self.surf, self.rect)
        screen.blit(self.txt, self.txtrect)

    def change_time(self):
        dseconds = int(time.time() - self.startTime)
        dminutes = dseconds//self.timeLap
        if dseconds / self.timeLap < 10:
            self.txt = clock_time_font.render(f'{self.stime + dminutes}:0{dseconds % self.timeLap}', True, (255, 0, 0))
        else:
            self.txt = clock_time_font.render(f'{self.stime+dminutes}:{dseconds % self.timeLap}', True, (255, 0, 0))
        self.txtrect = self.txt.get_rect(center=self.rect.center)
        self.endOfWorkTime = time.time()



class Student:
    def __init__(self, pos, timer, sickness_maxt=6):
        self.current_ani = stand_animation
        self.dtick = 0.1
        self.lowerTickRate = 0.01
        self.upperTickRate = 0.2
        self.image = self.current_ani[0]
        self.ani_tick = 0

        self.rect = self.image.get_rect(center=pos)
        self.timerRange = timer
        self.symptomDelay = random.randint(self.timerRange[0], self.timerRange[1])
        self.curedTime = time.time()
        self.sick = False

        self.timeOfSickness = time.time()
        self.maxSicknessTime = sickness_maxt
        self.redSighnImg = redSignimg
        self.redSighnRect = self.redSighnImg.get_rect(center=(self.rect.centerx, self.rect.centery-self.rect.height/2-self.redSighnImg.get_height()/2-20))

    def symptoms_showing(self):
        self.lowerTickRate = 0.1
        self.upperTickRate = 0.3
        self.change_animation(random.choice(symptoms_ani))
        self.sick = True

    def cured(self):
        self.curedTime = time.time()
        self.symptomDelay = random.randint(self.timerRange[0], self.timerRange[1])
        self.lowerTickRate = 0.01
        self.upperTickRate = 0.2
        self.change_animation(stand_animation)
        self.sick = False

    def timer(self):
        if time.time() - self.curedTime > self.symptomDelay and not self.sick:
            self.symptoms_showing()
        if not self.sick:
            self.timeOfSickness = time.time()

    def change_animation(self, ani):
        self.current_ani = ani
        self.image = self.current_ani[0]
        self.ani_tick = 0

    def animation(self):
        self.dtick = round(random.uniform(self.lowerTickRate, self.upperTickRate), 2)
        self.image = self.current_ani[int(self.ani_tick) % len(self.current_ani)]

        self.ani_tick += self.dtick
        if self.ani_tick > len(self.current_ani):
            self.ani_tick = 0

    def death_check(self):
        dt = time.time() - self.timeOfSickness
        if dt > self.maxSicknessTime:
            level.mistakes = 0
        else:
            alpha = int(dt / self.maxSicknessTime * 255)
            self.redSighnImg.set_alpha(alpha)
            self.image.set_alpha(255 - alpha)

    def draw(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.redSighnImg, self.redSighnRect)

    def update(self):
        self.timer()
        self.animation()
        self.death_check()
        self.draw()

class Heart:
    def __init__(self, pos):
        self.img = heartFullimg
        self.rect = self.img.get_rect(center=pos)

    def draw(self):
        screen.blit(self.img, self.rect)



tools = set()
class Tool:
    def __init__(self, img, y, name):
        self.name = name
        self.surf = img
        self.rect = self.surf.get_rect(center=(100, y))
        self.pos = (10, y)


        self.station_pos = (100, y)
        self.dx = 0
        self.dy = 0
        self.jump_counter = 0
        self.steps = 20

        self.cooldown = 1
        self.endWorkTime = time.time()


        self.moveBack = False
        self.someoneCured = False

        self.hold = False
        self.dragPos = (10, y)
        self.mousex_in_rect = 0
        self.mousey_in_rect = 0

        tools.add(self)

    def draw(self):
        screen.blit(self.surf, self.rect)

    def drag(self, students):
        global level
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.hold = True

        if not pygame.mouse.get_pressed()[0] or self.rect.collidepoint(mouse_pos) == False:
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
            self.someoneCured = False
        else:
            def someone_cured(s):
                s.cured()
                level.score += 100
                self.moveBack = True

            for student in students:
                if self.rect.colliderect(student.rect) and student.sick and not self.someoneCured and time.time() - self.endWorkTime > self.cooldown and student.rect.collidepoint(pygame.mouse.get_pos()):
                    self.endWorkTime = time.time()
                    if self.name == 'syringe' and student.current_ani == motor_tick_animation:
                        someone_cured(student)
                        break
                    elif self.name == 'haldol' and student.current_ani == voice_tick_animation:
                        someone_cured(student)
                        break
                    elif self.name == 'clonidine' and student.current_ani == eye_tick_animation:
                        someone_cured(student)
                        break
                    elif self.name == 'pimozide' and student.current_ani == face_tick_animation:
                        someone_cured(student)
                        break
                    else:
                        level.mistakes -= 1

                    self.someoneCured = True

            if self.moveBack:
                # Alternate method :
                self.rect.x += self.dx
                self.rect.y += self.dy
                if self.jump_counter < steps - 1:
                    self.jump_counter += 1
                else:
                    self.jump_counter = 0
                    self.moveBack = False



syringe = Tool(syringeimg, 100, 'syringe')
haldol = Tool(haldolimg, 250, 'haldol')
clonidine = Tool(clonidineimg, 400, 'clonidine')
pimozide = Tool(pimozideimg, 550, 'pimozide')

lv1 = Level([(400, 600), (600, 600), (800, 600), (1000, 600)], (3, 8), 5)
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
backArrowButton = Button((100, 100), backArrowimg)
saveAndBackButton = Button((CENTER[0], CENTER[1] + 300), save_and_backimg)

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

        if backArrowButton.clickStage:
            app.gameState = 'main menu'

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
            for tool in tools:
                tool.rect.center = tool.station_pos
                tool.endWorkTime = time.time()

            app.gameState = f'lv{selectedLevel+1}'
            for level in levels:
                if app.gameState == level.name:
                    level.score = 0
                    level.mistakes = len(level.hearts)

                    for student in level.students:
                        student.timeOfSickness = time.time()
                        student.cured()
                        student.curedTime = time.time()
                    level.watch.startTime = time.time()
                    break


        rightArrowButton.update()
        leftArrowButton.update()
        backArrowButton.update()

    if app.gameState.startswith('lv'):
        screen.blit(classroomBg, (0, 0))
        screen.blit(toolBarSurf, toolBarRect)

        for level in levels:
            if app.gameState == level.name:
                for tool in tools:
                    if not end_menu:
                        tool.drag(level.students)
                    tool.draw()
                level.logic()


    if app.gameState == 'options':
        screen.fill(BLACK)
        if backArrowButton.clickStage:
            app.gameState = 'main menu'


        backArrowButton.update()


    mouse.update()
    pygame.display.update()


