from .character import *
from .hero import *
from ..map import *

class FlyEnemy(Character):
    def __init__(self, x, y, width, height, finish_x, speed):
        Character.__init__(self, x, y, width, height, 'enemy1/fly/0.png', speed)
        self.list_fly = self.create_animations_list('enemy1/fly', 2)
        self.list_fly_left = self.create_animations_list('enemy1/fly', 2, True)
        self.finish_x = finish_x
        self.start_x = x
        # создаем изначальное изображенние бочки
        self.barrel = Sprite(0, 0, 50, 50, 'barrel/0.png')
        # создаем список анимации
        self.barrel.list_explosion = self.barrel.create_animations_list('barrel', 8)
        # создаем щетчик атак
        self.attack_counter = 0
        # создаем переключатель для взрыва бочки
        self.is_explosion = False

        self.list_death = self.create_animations_list("enemy1/death" , 5, True)
        self.list_death_left = self.create_animations_list("enemy1/death" , 5)

    def fly(self):
        if self.direction == 'right':
            self.x += self.speed
            if self.x >= self.finish_x:
                self.direction = 'left'
        else:
            self.x -= self.speed
            if self.x <= self.start_x:
                self.direction = 'right'
        self.play_animation(15, 29, self.list_fly, self.list_fly_left)
        
    def animation(self):
        if self.is_death == False:
            self.fly()
            self.attack()
        else:
            self.play_animation(10 , 49, self.list_death, self.list_death_left)
            self.y += 4
            if self.y >= 700:
                map.enemy_list.remove(self)
        
    def attack(self):
        # создание колизии для летающего иноплонетянина
        # self.x + self.width / 2 - 1 - позволяет расположить луч посередине тарелки
        rect = pygame.Rect(self.x + self.width / 2 - 1, self.y + self.height * 0.75, 2, 700)
        pygame.draw.rect(screen, 'red', rect)
        
        # условие для проверки соприковосновение с лучом
        if main_hero.hero_rect.colliderect(rect) and self.attack_counter == 0:
            self.barrel.x = self.x + 45
            self.barrel.y = self.y + self.height * 0.75
            # устанавливаем счетчик атаки (запускаем бочку)
            self.attack_counter = 150
            
        self.move_barrel()
    
    
    def move_barrel(self):
        # проверка что счетчик атаки запустился
        if self.attack_counter > 0:
            self.attack_counter -= 1
            self.barrel.y += 4
            self.barrel.show_image()
            
            # создаем колизию для бочки
            self.barrel_rect = pygame.Rect(self.barrel.x, self.barrel.y, self.barrel.width, self.barrel.height)        
            
            # проверяем косается ли бочки гллавный герой
            if main_hero.hero_rect.colliderect(self.barrel_rect):
                main_hero.count_heart -= 2
                
                #  устанавливается переключатель взрыва на True
                self.is_explosion = True
                self.attack_counter = -40
            
            # перебераем все блоки нашей карты
            for block in map.COLLISION_LIST:
                block_rect = pygame.Rect(block.x, block.y, block.width, block.height)
                if block_rect.colliderect(self.barrel_rect):
                    self.attack_counter = -40
                    self.is_explosion = True
                    # если коснулась блока то выходим из цикла
                    break
                
        # если атака ушла в минус
        if self.attack_counter < 0:
            self.attack_counter += 1

        # условие для проверки взрыва
        if self.is_explosion:
            self.barrel.show_image()
            # если кадр ровняется 38 выключаем переключатель взрыва
            if self.barrel.image_counter == 38:
                self.is_explosion = False
            # запускаем анимацию бочки
            self.barrel.play_animation(5, 39, self.barrel.list_explosion)
           
        

fly_enemy1 = FlyEnemy(100, 50, 140, 140, 1300, 3)
map.enemy_list.append(fly_enemy1)