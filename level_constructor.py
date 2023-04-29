import pygame


standimg = pygame.image.load('resources/student_stand.png').convert_alpha()


class Level:
    def __init__(self, students):
        self.students == 0


studentsGroup = pygame.sprite.Group()
class Student(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = standimg
        self.rect = self.image.get_rect(center=pos)

        studentsGroup.add(self)
