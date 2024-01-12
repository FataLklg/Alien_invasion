import pygame
from pygame.sprite import Sprite
from random import randint, choice

from utils import resource_path


class Star(Sprite):
	"""Класс звезды."""

	def __init__(self, ai_game):
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings

		# Словарь с размерами звёзд.
		STAR_IMG_SIZES = {'small': (30, 30),
						  'medium': (40, 40),
						  'big': (50, 50)}
		star_img = resource_path('images/star.bmp')
		self.image = pygame.image.load(star_img)
		self.image = pygame.transform.scale(self.image,
									  		choice((STAR_IMG_SIZES['small'],
											STAR_IMG_SIZES['medium'],
											STAR_IMG_SIZES['big'])))
		self.rect = self.image.get_rect()

		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		self.x = float(self.rect.x)
		self.y = float(self.rect.y)
