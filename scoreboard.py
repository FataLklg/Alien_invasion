import pygame.font
from pygame.sprite import Group

from ship import Ship


class Scoreboard():
    """Класс для вывода игровой информации."""
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Настройка шрифта для вывода счёта.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        # Подготовка исходного изображения.
        self._prep_score()
        self._prep_high_score()
        self.prep_level()
        self.prep_ships()

    def _prep_score(self):
        """Преобразует текущий счёт в графическое изображение."""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str,
                                            True,
                                            self.text_color,
                                            self.settings.bg_color)
        
        # Вывод счёта в правой верхней части экрана.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
    
    def _prep_high_score(self):
        """Преобразует рекордный счёт в графическое изображение."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str,
                                                 True,
                                                 self.text_color,
                                                 self.settings.bg_color)

        # Выравнивает рекорд по центру в верхней части экрана.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
    
    def check_high_score(self):
        """Проверяет, появился ли новый рекорд."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self._prep_high_score()
    
    def prep_level(self):
        """Преобразует уровень в графическое изображение."""
        level_str = f"Уровень: {str(self.stats.level)}"
        self.level_image = self.font.render(level_str,
                                            True,
                                            self.text_color,
                                            self.settings.bg_color)
    
        # Уровень выводится под текущим счётом.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10
    
    def prep_ships(self):
        """Сообщает кол-во оставшихся кораблей."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.image = pygame.transform.scale(ship.image, (50, 50))
            ship.rect.x = 10 + ship_number * ship.image.get_size()[0]
            ship.rect.y = 10

            self.ships.add(ship)

    def show_score(self):
        """Выводит счёт, уровень и кол-во оставшихся кораблей на экран."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
