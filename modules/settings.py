import pygame

# Позволяет инициализировать шрифты, звуки и т.д
# без этой строчки будет ошибка: pygame.error: font not initialized
pygame.init()


# pygame.font.Font(None, 100) - позволяет подкючить шрифты
# первый параметр это шрифт, в нашем случае это None
font = pygame.font.Font(None, 100)

screen = pygame.display.set_mode((1500, 700))
pygame.display.set_caption("game")
