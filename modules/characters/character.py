
from ..image import *
import pygame
from ..settings import *
from ..map import *

class Character(Sprite):
    def __init__(self, x, y, height, width, name, speed, direction = "right"):
        Sprite.__init__(self, x, y, height, width, name)
        self.speed = speed
        self.jump_counter = 0
        self.direction = direction
        self.is_crawl = False
        self.is_death = False
        
        
        
    def check_colision(self):
        self.hero_rect = pygame.Rect(self.x + 15, self.y + 15, self.width - 30, self.height - 15)
        # pygame.draw.rect(screen, 'red', self.hero_rect)
        if self.is_crawl == True:
            self.hero_rect = pygame.Rect(self.x + 15, self.y + 25, self.width - 30, self.height - 25)
        
        self.can_fall = True
        self.can_move_right = True
        self.can_move_left = True
        self.can_stand_up = True

        for platform in map.COLLISION_LIST:
            rect_top = pygame.Rect(platform.x + 8, platform.y, platform.width - 16, 1)
            rect_left = pygame.Rect(platform.x, platform.y + 5, 1, platform.height - 10)
            rect_right = pygame.Rect(platform.x + platform.width, platform.y + 5, 1, platform.height - 10)
            rect_bottom = pygame.Rect(platform.x + 8, platform.y + platform.height, platform.width - 16, 1)
            #pygame.draw.rect(screen, 'blue', rect_top)
            #pygame.draw.rect(screen, 'blue', rect_left)
            #pygame.draw.rect(screen, 'blue', rect_right)
            #pygame.draw.rect(screen, 'blue', rect_bottom)

            # colliderect - метод который позволяет проверить соприкасаются ли два прямоугольника
            if self.hero_rect.colliderect(rect_top):
                self.can_fall = False
                self.y = platform.y - self.height + 1
            if self.hero_rect.colliderect(rect_left):
                self.can_move_right = False
            if self.hero_rect.colliderect(rect_right):
                self.can_move_left = False

            if self.hero_rect.colliderect(rect_bottom):
                self.jump_counter = 0
                self.can_stand_up = False