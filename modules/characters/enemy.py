from .character import *
from ..map import *
import pygame
from .hero import *

class Enemy(Character):
    def __init__(self, x, y, height, width, speed, finish_x):
        Character.__init__(self, x, y, width, height, "enemy3/move/0.png", speed)
        self.list_move = self.create_animations_list("enemy3/move", 5)
        self.list_move_left = self.create_animations_list('enemy3/move', 5, True)
        self.finish_x = finish_x
        self.start_x = x
        
        self.shoot_counter = 0
        self.bullet = Sprite(0, 0, 20, 20, 'enemy3/bullet.png')

        self.list_death = self.create_animations_list("enemy3/death" , 4)

    def move(self):
        self.check_colision()
        if self.can_move_right and self.direction == 'right':
            self.x += self.speed
        elif self.can_move_left and self.direction == 'left':
            self.x -= self.speed
            
        if self.direction == 'right':
            if self.x >= self.finish_x or not self.can_move_right:
                self.direction = 'left'
        elif self.direction == 'left':
            if self.x <= self.start_x or not self.can_move_left:
                self.direction = 'right'

    def animation(self):
        if self.is_death == False:
            self.move()
            self.attack()
            self.play_animation(7, 34, self.list_move, self.list_move_left)
        else:
            self.play_animation(10 , 40 , self.list_death)
            if self.image_counter == 39:
                map.enemy_list.remove(self)
                
    def attack(self):
        if self.direction == "right":
            enemy_view_rect = pygame.Rect(self.x + self.width , self.y , self.width * 3 , self.height)
        else:
            enemy_view_rect = pygame.Rect(self.x - self.width * 3 , self.y , self.width * 3 , self.height)

        # pygame.draw.rect(screen , "yellow" , enemy_view_rect)
        # if main_hero.hero_rect.colliderect(enemy_view_rect):
        #     print("shoot")

        if main_hero.hero_rect.colliderect(enemy_view_rect) and self.shoot_counter == 0:
            self.shoot_counter = 200
            self.bullet.x = self.x + self.width / 2
            self.bullet.y = self.y + self.height / 2

            self.bullet.direction = self.direction
            if self.bullet.direction == 'right':
                self.bullet.image = self.bullet.load_image('enemy3/bullet.png')
            else:
                self.bullet.image = self.bullet.load_image('enemy3/bullet.png', True)
            
        if self.shoot_counter > 0:
            self.move_bullet()
        
        if self.shoot_counter < 0:
            self.shoot_counter += 1

    def move_bullet(self):
        if self.bullet.direction == 'right':
            self.bullet.x += 8
        else:
            self.bullet.x -= 8
        
        self.bullet.show_image()
        self.shoot_counter -= 1

        self.bullet_rect = pygame.Rect(self.bullet.x, self.bullet.y, self.bullet.width, self.bullet.height)
        
        if main_hero.hero_rect.colliderect(self.bullet_rect):
            main_hero.count_heart -= 1

            self.shoot_counter = -50
        
        for block in map.COLLISION_LIST:
            block_rect = pygame.Rect(block.x, block.y, block.width, block.height)
            if block_rect .colliderect(self.bullet_rect):
                self.shoot_counter = -50
                break

enemy1 = Enemy(800, 570, 80, 80, 2, 1350)
map.enemy_list.append(enemy1)