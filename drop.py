import pygame
from pygame.sprite import Sprite
from random import randint


class Drop(Sprite):
    """Класс капель воды."""
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Загрузка изображения капли воды.
        self.image = pygame.image.load('images/drop.bmp')
        self.rect = self.image.get_rect()
        # Устанавливает разный размер каплям.
        self.image_size = (randint(5, 15), randint(10, 20))
        self.image = pygame.transform.scale(self.image, self.image_size)

        # Координаты появления капли.
        self.rect.x = randint(-100, 100)
        self.rect.y = randint(-500, -10)

        # Сохранение точной горизонтальной позиции капли.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """Перемещение капли вниз по экрану."""
        self.y += self.settings.drop_speed
        self.rect.y = self.y
    
    def check_edges(self):
        """Возвращает True, если капля достигла нижней части экрана."""
        screen_rect = self.screen.get_rect()
        if self.rect.top >= screen_rect.bottom:
            return True
