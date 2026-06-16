from .character import *
from ..map import *

class FriendlyBot(Character):
    def __init__(self, x, y, width, height):
        Character.__init__(self, x, y, width, height, "friendly_bot/breath/1.png", 0)
        self.list_breath = self.create_animations_list("friendly_bot/breath", 2)
        self.list_death = self.create_animations_list("friendly_bot/death", 4)
    
    def animation(self):
        if self.is_death == False:
            self.play_animation(20, 39, self.list_breath)
        else :
            self.play_animation(10, 40, self.list_death)
            if self.image_counter == 39  :
                map.enemy_list.remove(self)
            
bot1 = FriendlyBot(1125, 320, 80, 80)
map.enemy_list.append(bot1)

