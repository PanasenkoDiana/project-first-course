import pygame, os, pytmx
from .settings import *

class Map():
    def __init__(self, name: str):
        path = os.path.join(__file__, '..', '..', 'tilemaps', name)
        path = os.path.abspath(path)
        # load_pygame - помогает загрузить карту в pytmx
        self.TILEMAP = pytmx.load_pygame(path)
        self.HEIGHT = self.TILEMAP.tileheight
        self.WIDTH = self.TILEMAP.tilewidth
        self.create_collision()
        self.enemy_list = []
        
    def show(self):
        for layer in self.TILEMAP.visible_layers:
            if layer.name != 'Collision'and layer.name != "LadderCollision" :
                for x,y, tile in layer:
                    if tile != 0:
                        # get_tile_image_by_gid - функция которая получает изображение по номеру
                        image = self.TILEMAP.get_tile_image_by_gid(tile)
                        screen.blit(image, (x * self.WIDTH, y * self.HEIGHT))
    
    def create_collision(self):
        self.COLLISION_LIST = []
        # get_layer_by_name - функция которая позволяет получить слой за названием
        layer = self.TILEMAP.get_layer_by_name('Collision')
        for object in layer:
            # pygame.Rect - класс который используется для создания прямоугольника в pygame
            rect = pygame.Rect(object.x, object.y, object.width, object.height)
            self.COLLISION_LIST.append(rect)        
        self.LADDERCOLLISION_LIST = []    
            
        for ladder in self.TILEMAP.get_layer_by_name("LadderCollision"):
            self.LADDERCOLLISION_LIST.append(pygame.Rect(ladder.x , ladder.y , ladder.width , ladder.height)
            )
            
            
map = Map('level1.tmx')