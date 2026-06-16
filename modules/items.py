from .characters import *
from .image import *
import pygame

class Item(Sprite):
    def check_collect(self):
        item_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if main_hero.hero_rect.colliderect(item_rect):
            item_list.remove(self)
            
            if "key" in self.name:
                main_hero.has_key = True
            elif 'battery' in self.name and main_hero.count_battery < 5:
                main_hero.count_battery += 1 
                main_hero.battery.image = main_hero.battery.list_animation[main_hero.count_battery]
            elif "heart" in self.name and main_hero.count_heart < 3:
                main_hero.count_heart += 1 
item_list = [
    Item(425, 625, 25, 25, "heart.png"),
    Item(375, 225, 25, 25, "heart.png"),
    Item(350, 500, 50, 50, "battery1.png"),
    Item(450, 500, 50, 50, "battery2.png"),
    Item(325, 225, 25, 25, "key.png"),
    Item(515, 375, 25, 25, "protect.png")
]