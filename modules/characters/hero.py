import pygame
from ..settings import *
from .character import *

class Hero(Character):
    def __init__(self, x, y, height, width, name, speed):
        Character.__init__(self, x, y, height, width, name, speed)
        self.list_run = self.create_animations_list("hero/run", 6)
        self.list_run_left = self.create_animations_list("hero/run", 6, True)
        self.list_jump = self.create_animations_list("hero/jump", 2)
        self.list_jump_left = self.create_animations_list("hero/jump", 2, True)
        self.list_breath = self.create_animations_list("hero/breath", 11)
        self.on_ladder = False
        self.list_climb = self.create_animations_list("hero/climb",2)
        self.has_key = False
        
        
        self.is_hold_blaster = False
        self.list_shooting_run = self.create_animations_list('hero/shooting_run', 6)
        self.list_shooting_run_left = self.create_animations_list('hero/shooting_run', 6, True)

        self.count_heart = 3
        self.image_heart = Sprite(0, 25, 50, 50, 'heart.png')
        self.empty_image_heart = Sprite(0, 25, 50, 50, 'empty_heart.png')

        self.list_crawl = self.create_animations_list('hero/crawl', 5)
        self.list_crawl_left = self.create_animations_list('hero/crawl', 5, True)

        self.shoot_counter = 0
        self.bullet = Sprite(0, 0, 20, 20, 'hero/bullet.png')

        self.count_battery = 5
        self.battery = Sprite(25, 30, 40, 40, 'battery/5.png')
        self.battery.list_animation = self.battery.create_animations_list('battery', 6)
    
    def climb(self):
        self.on_ladder = False
        
        for ladder in map.LADDERCOLLISION_LIST:
            if self.hero_rect.colliderect(ladder):
                self.on_ladder = True
                break

        if self.on_ladder:
            if self.list_key[pygame.K_UP] and self.can_stand_up:
                self.y -= 2
                self.play_animation(10, 19, self.list_climb)
            elif self.list_key[pygame.K_DOWN]:
                self.y += 2
                self.play_animation(10, 19, self.list_climb)
    
    def show_stats(self):
        for count in range(3):
            if count < self.count_heart:
                screen.blit(self.image_heart.image, (50 * (count + 2), 25))
            else:
                screen.blit(self.empty_image_heart.image, (50 * (count + 2), 25))
        self.battery.show_image()

    def jump(self):
        if self.list_key[pygame.K_SPACE] and self.can_fall == False and self.can_stand_up == True:
            # Триггер который говорит, что мы можем прыгать
            # Задаёт резкость прыжка
            self.jump_counter = 23

        if self.jump_counter > 0:
            self.jump_counter -= 1
            # Высота прыжка
            self.y -= 8
            if self.direction == 'right':
                self.image = self.list_jump[0]
            else:
                self.image = self.list_jump_left[0]
    
        
    def move(self):
        # get_pressed - метод который возвращает список клавиш
        # [False, True, False] - где каждое значение - нажата ли клавиша
        # K_a, K_d, K_w ... - сохраняют индексы этого списка

        self.list_key = pygame.key.get_pressed()
        self.check_colision()
        self.jump()    

        if self.list_key[pygame.K_s]:
            self.is_crawl = True
        else:
            self.is_crawl = False    
        
        if self.list_key[pygame.K_RIGHT] == True and self.can_move_right:
            self.x = self.x + self.speed
            self.direction = "right"
            if self.is_crawl:
                self.x += self.speed / 3
                self.play_animation(15, 74, self.list_crawl, self.list_crawl_left)
            else:
                self.x += self.speed
                if self.is_hold_blaster:
                    self.play_animation(5, 29, self.list_shooting_run, self.list_shooting_run_left)
                else:
                    self.play_animation(5, 29, self.list_run, self.list_run_left)


        elif self.list_key[pygame.K_LEFT] == True and self.can_move_left:
            self.x = self.x - self.speed
            self.direction = "left"
            if self.is_crawl:
                self.x -= self.speed / 3
                self.play_animation(15, 74, self.list_crawl, self.list_crawl_left)
            else:
                self.x -= self.speed
                if self.is_hold_blaster:
                    self.play_animation(5, 29, self.list_shooting_run, self.list_shooting_run_left)
                else:
                    self.play_animation(5, 29, self.list_run, self.list_run_left)
                
        elif self.jump_counter == 0 and self.can_fall == False:
            if self.is_crawl:
                if self.direction == 'right':
                    self.image = self.list_crawl[0]
                else:
                    self.image = self.list_crawl_left[0]
            else:
                self.play_animation(15, 164, self.list_breath)

        if self.can_fall and self.jump_counter == 0 and self.on_ladder == False:
            self.y += 5
            if self.direction == "right":
                self.image = self.list_jump[1]
            else:
                self.image = self.list_jump_left[1]
        
        self.attack()
        self.climb()
        
    def attack(self):
        if self.list_key[pygame.K_e] and self.is_hold_blaster and self.shoot_counter == 0 and self.count_battery > 0:
            self.count_battery -= 1
            self.battery.image =  self.battery.list_animation[self.count_battery]
            self.shoot_counter = 200
            self.bullet.x = self.x + self.width / 2
            self.bullet.y = self.y + self.height / 2
            self.bullet.direction = self.direction

            if self.bullet.direction == 'right':
                self.bullet.image = self.bullet.load_image('hero/bullet.png')
            else:
                self.bullet.image = self.bullet.load_image('hero/bullet.png', True)
        
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

        for block in map.COLLISION_LIST:
            block_rect = pygame.Rect(block.x, block.y, block.width, block.height)
            if block_rect.colliderect(self.bullet_rect):
                self.shoot_counter = -50
                break

        for enemy in map.enemy_list:
            enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
            if enemy_rect.colliderect(self.bullet_rect):
                # map.enemy_list.remove(enemy)
                enemy.is_death = True
                enemy.image_counter = 0  
                self.shoot_counter = -50




main_hero = Hero(50, 570, 80, 80, "hero.png", 2)
