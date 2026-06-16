from .character import *
from .hero import *
from ..map import *

class StaticEnemy(Character):
    def __init__(self, x, y, height, width, direction):
        Character.__init__(self, x, y, height, width, "enemy2/attack/0.png", 0)
        self.direction = direction
        self.list_death = self.create_animations_list("enemy2/death", 6)
        self.list_death_left = self.create_animations_list("enemy2/death", 6, True) 
        
        self.list_attack = self.create_animations_list('enemy2/attack', 6)
        self.list_attack_left = self.create_animations_list('enemy2/attack', 6, True)

    def animation(self):
        if self.is_death == False:
            if self.image_counter > 0:
                self.play_animation(10, 59, self.list_attack, self.list_attack_left)
            else:
                if self.direction == 'right':
                    self.image = self.list_attack[0]
                else:
                    self.image = self.list_attack_left[0]

            self.attack()
        else:
            self.play_animation(10 , 60, self.list_death, self.list_death_left)
            if self.image_counter == 59:
                map.enemy_list.remove(self)
    
    def attack(self):
        if self.direction == "right":
            enemy_rect = pygame.Rect(self.x + self.width / 2, self.y, self.width * 0.75, self.height)
        else:
            enemy_rect = pygame.Rect(self.x - self.width / 4, self.y, self.width * 0.75, self.height)

        # pygame.draw.rect(screen, "yellow", enemy_rect)

        if main_hero.hero_rect.colliderect(enemy_rect) and self.image_counter == 0:
            self.image_counter = 1
        
        if self.image_counter == 58 and main_hero.hero_rect.colliderect(enemy_rect):
            main_hero.count_heart -= 1

        

static_enemy1 = StaticEnemy(730, 320, 80, 80, 'left')
map.enemy_list.append(static_enemy1)

static_enemy1 = StaticEnemy(500, 570, 80, 80, 'right')
map.enemy_list.append(static_enemy1)