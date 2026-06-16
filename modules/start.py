from .characters.hero import *
import pygame
# Точка позволяет указать что файл находится на одном и том же уровне
from .settings import screen 
from .map import *
from .image import background
from .items import *

# font.render - позволяет создать объект текста
lose_text = font.render('Вы проиграли', True, 'red')
win_text = font.render('Вы выиграли', True, 'yellow')

def start_game():
    run = True
    win = False
    # pygame.time.Clock - позволяет создать объект для колличества кадров
    fps = pygame.time.Clock()
    rect_win = pygame.Rect(1450, 600, 50, 50)
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    main_hero.is_hold_blaster = not main_hero.is_hold_blaster
        # tick - позволяет задать колличество кадров обновляемое в секунду
        fps.tick(60)
        screen.fill('black')
        
        if main_hero.count_heart > 0 and win == False:
            background.show_image()
            #for rect in map.COLLISION_LIST:
                # pygame.draw.rect - позволяет отобразить прямоугольники на экране
                #pygame.draw.rect(screen, 'green', rect)

            map.show()

            main_hero.move()
            main_hero.show_image()
            main_hero.show_stats()
            
            for enemy in map.enemy_list:
                enemy.animation()
                enemy.show_image()
                
            for item in item_list:
                item.show_image()
                item.check_collect()
                

            if main_hero.hero_rect.colliderect(rect_win) and main_hero.has_key:
                win = True
        elif win == True:
            screen.blit(win_text, (520, 330))
        elif main_hero.count_heart <= 0:
            screen.blit(lose_text, (540, 330))
        
        pygame.display.flip()
        