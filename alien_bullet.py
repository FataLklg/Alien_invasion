import pygame
from pygame.sprite import Sprite
from random import choice


class AlienBullet(Sprite):
	"""Класс управления снарядами, выпущенными кораблём."""

	def __init__(self, ai_game):
		"""Создаёт объект снарядов в текущей позиции корабля."""
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.color = ai_game.settings.bullet_color
		
		# Создание снаряда в позиции (0, 0) и назначение правильной позиции.
		self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
		self.rect.midtop = choice(ai_game.aliens.sprites()).rect.midbottom
		self.y = float(self.rect.y)

	def update(self):
		"""Перемещает снаряд вверх по экрану."""
		# Обновление позиции снаряда в вещественном формате.
		self.y += self.settings.alien_bullet_speed
		# Обновление позиции прямоугольника.
		self.rect.y = self.y

	def draw_bullet(self):
		"""Вывод снаряда на экран."""
		pygame.draw.rect(self.screen, self.color, self.rect)