from random import randint


class Settings():
	"""Клас для хранения всех настроек игры Alien Invasion."""

	def __init__(self):
		"""Инициализирует настройки игры."""
		# Параметры экрана
		self.screen_width = 2560
		self.screen_height = 1440
		self.bg_color = (230, 230, 230)

		# Настройки корабля.
		self.ship_limit = 2

		# Параметры снаряда.
		self.bullet_speed = 1.5
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullets_allowed = 3

		# Настройки пришельцев.
		self.fleet_drop_speed = 15

		# Настройки капель воды.
		self.drop_speed = 1.0
		self.drop_width = 10
		self.drop_height = 15

		# Темп ускорения игры.
		self.speedup_scale = 1.1

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""Инициализирует настройки, меняющиеся во время игры."""
		self.ship_speed = 1.5
		self.bullet_speed = 3.0
		self.alien_speed = 1.0

		self.fleet_direction = 1

	def increase_speed(self):
		"""Увеличивает настройки скорости."""
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale
