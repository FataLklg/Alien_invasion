import sys
from time import sleep

import pygame
from random import randint

from alien import Alien
from bullet import Bullet
from button import Button
from drop import Drop
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship
from star import Star


class AlienInvasion():
	"""Класс управления ресурсами и поведением игры."""

	def __init__(self):
		"""Инициализирует игру и создаёт игровые ресурсы."""
		pygame.init()
		self.settings = Settings()

		self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Alien Invasion")
		# Создание экземпляров для хранения статистики и панели результатов.
		self.stats = GameStats(self)
		self.sb = Scoreboard(self)

		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()
		self.stars = pygame.sprite.Group()
		self.drops = pygame.sprite.Group()

		self._create_drops_x()
		self._create_stars_sky()
		self._create_fleet()

		# Создание кнопки Play.
		self.play_button = Button(self, "Play")

	def run_game(self):
		"""Запуск основного цикла игры."""
		while True:
			self._check_events()

			if self.stats.game_active:
				self._update_drops()
				self.ship.update()
				self._update_bullets()
				self._update_aliens()

			self._update_screen()

	def _check_events(self):
		"""Обрабатывает нажатия клавиш клавиатуры и мыши."""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)

	def _check_play_button(self, mouse_pos):
		"""Запускает новую игру при нажатии кнопки Play."""
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			# Сброс игровых настроек.
			self.settings.initialize_dynamic_settings()
			self._start_game()
	
	def _start_game(self):
		"""Запускает игру."""
		# Сброс игровой статистики.
		self.stats.reset_stats()
		self.stats.game_active = True

		# Очистка списка пришельцев и снарядов.
		self.aliens.empty()
		self.bullets.empty()

		# Создание нового флота и размещение корабля в центре.
		self._create_fleet()
		self.ship.center_ship()

		# Скрывает указатель мыши.
		pygame.mouse.set_visible(False)

	def _check_keydown_events(self, event):
		"""Реагирует на нажатие клавиш."""
		if event.key == pygame.K_RETURN and not self.stats.game_active:
			self._start_game()
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		elif event.key == pygame.K_UP:
			self.ship.moving_up = True
		elif event.key == pygame.K_DOWN:
			self.ship.moving_down = True
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()
		elif event.key == pygame.K_ESCAPE:
			sys.exit()

	def _check_keyup_events(self, event):
		"""Реагирует на отпускание клавиш."""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False
		elif event.key == pygame.K_UP:
			self.ship.moving_up = False
		elif event.key == pygame.K_DOWN:
			self.ship.moving_down = False

	def _fire_bullet(self):
		"""Создание нового снаряда и включение его в группу bullets."""
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		"""Обновляет позиции снарядов и удаляет старые снаряды."""
		# Обновление позиции снарядов.
		self.bullets.update()

		# Удаление снарядов, вышедших за край экрана.
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)
		
		self._check_bullet_alien_collision()

	def _check_bullet_alien_collision(self):
		"""Обработка коллизий снарядов с пришельцами."""
		# Проверка попаданий в пришельцев.
		# При обнаружении попадания удаляет снаряд и пришельца.
		collisions = pygame.sprite.groupcollide(
			self.bullets, self.aliens, True, True
		)

		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len(aliens)
			self.sb._prep_score()

		# Если весь флот пришельцев уничтожен:
		# Уничтожает существующие снаряды и создаёт новый флот.
		if not self.aliens:
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()

	def _create_fleet(self):
		"""Создание флота пришельцев."""
		# Создание первого ряда пришельцев.
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		available_space_x = self.settings.screen_width - (1.7 * alien_width)
		number_aliens_x = available_space_x // (1.7 * alien_width)

		# Определяет кол-во рядов, помещающихся на экране.
		ship_height = self.ship.rect.height
		available_space_y = (self.settings.screen_height - (7 * alien_height) - ship_height)
		number_rows = available_space_y // (2 * alien_height)

		# Создание флота вторжения.
		for row_number in range(int(number_rows)):
			for alien_number in range(int(number_aliens_x)):
				self._create_alien(alien_number, row_number)			

	def _create_alien(self, alien_number, row_number):
		"""Создание пришельца и размещение его в ряду."""
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.x = alien_width + 1.7 * alien_width * alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
		self.aliens.add(alien)
	
	def _check_aliens_bottom(self):
		"""Проверяет, добрались ли пришельцы до нижнего края экрана."""
		screen_rect =self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				self._ship_hit()
				break
	
	def _check_fleet_edges(self):
		"""Реагирует на достижение пришельцем края экрана."""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break
	
	def _change_fleet_direction(self):
		"""Опускает весь флот и меняет направление флота."""
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1
	
	def _update_aliens(self):
		"""
		Проверяет, достиг ли флот края экрана и
		обновляет позицию всех пришельцев во флоте.
		"""
		self._check_fleet_edges()
		self.aliens.update()

		# Проверка коллизий "корабль - пришельцы".
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()
		
		# Проверить, добрались ли пришельцы до нижнего края экрана.
		self._check_aliens_bottom()

	def _create_star(self, star_number, row_number):
		"""Создание звезды и определение местоположения звезды."""
		star = Star(self)
		star_width, star_height = star.rect.size
		star.x = star_width + randint(3, 7) * star_width * star_number
		star.rect.x = star.x
		star.rect.y = star.rect.height + randint(3, 7) * star.rect.height * row_number
		self.stars.add(star)			

	def _create_stars_sky(self):
		"""Создаёт звёздное небо."""
		star = Star(self)
		star_width, star_height = star.rect.size
		available_space_x = self.settings.screen_width
		available_space_y = self.settings.screen_height
		number_stars_x = available_space_x // (star_width)
		number_rows = available_space_y // (star_height)

		for number_row in range(int(number_rows)):
			for star_number in range(int(number_stars_x)):
				self._create_star(star_number, number_row)
	
	def _create_drop(self, number_drop):
		"""Создаёт каплю и определяет местоположение капель."""
		drop = Drop(self)
		drop_width, drop_height = self.settings.drop_width, self.settings.drop_height
		drop.rect.width = self.settings.drop_width
		drop.rect.height = self.settings.drop_height
		drop.x = drop_width * drop_width * number_drop
		drop.rect.x = drop.x
		self.drops.add(drop)

	def _create_drops_x(self):
		"""Создаёт ряд капель в верхней части экрана."""
		drop = Drop(self)
		drop_width = drop.rect.width
		availible_space_x = self.settings.screen_width
		number_drops_x = availible_space_x // (drop_width)

		for number_drop in range(int(number_drops_x)):
			self._create_drop(number_drop)

	def _check_drops_edges(self):
		"""Проверяет достигли ли капли воды нижнего края экрана и удаляет вышедшие за край."""
		for drop in self.drops.sprites():
			if drop.check_edges():
				self.drops.remove(drop)

		# Если кол-во капель на экране = 0: добавляет новый ряд капель.
		if not self.drops:
			self._create_drops_x()

	def _update_drops(self):
		"""Обновляет позицию капель воды на экране."""
		self._check_drops_edges()
		self.drops.update()
	
	def _ship_hit(self):
		"""Обрабатывает столкновение корабля с пришельцами."""
		# Уменьшает значение ship_left.
		if self.stats.ships_left > 0:
			self.stats.ships_left -= 1

			# Очистка списка пришельцев и снарядов.
			self.aliens.empty()
			self.bullets.empty()

			# Создание нового флота и размещение корабля в центре.
			self._create_fleet()
			self.ship.center_ship()

			# Пауза.
			sleep(0.5)
		else:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)

	def _update_screen(self):
		"""Обновляет изображения на экране и отображает новый экран."""
		self.screen.fill(self.settings.bg_color)
		self.stars.draw(self.screen)
		self.drops.draw(self.screen)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.aliens.draw(self.screen)

		# Вывод информации о счёте
		self.sb.show_score()

		# Кнопка Play отображается в том случае, если игра неактивна.
		if not self.stats.game_active:
			self.play_button.draw_button()

		pygame.display.flip()

if __name__ == '__main__':
	# Создание экземпляра и запуск игры.
	ai = AlienInvasion()
	ai.run_game()
