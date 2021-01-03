import pygame
from projectile import *
from ennemie import *


class Player(pygame.sprite.Sprite):
	"""docstring for Player"""
	def __init__(self, nbr, keys: list, coor, game, color):
		super().__init__()
		self.nbr = nbr
		self.game = game
		self.K_jump, self.right, self.left, self.switch, self.s_key, self.sp_key, self.spr_key = keys
		self.jump_son = pygame.mixer.Sound('png/jump_07.wav')
		self.default_y = coor[1]
		self.is_jump = 0
		self.image = pygame.Surface((40, 40))
		self.image.fill(color)
		self.original = self.image.copy()
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = coor.copy()
		self.all_projectile = pygame.sprite.Group()
		self.is_possible = True
		self.is_possible_spawn = True
		self.is_sprinting = False
		self.original_x = coor[1]
		self.is_right = True
		self.dico_right = {True: 16, False: -16}
		self.is_sprint_on_wall = False

	def jump(self):
		if self.is_jump == 1:
			self.jump_son.play()
			self.is_jump = 2
		if self.is_jump == 2:
			self.rect.y -= 4
		if self.default_y - self.rect.y > 120:
			self.is_jump = 3
		if self.is_jump == 3:
			self.rect.y - 1
			self.is_jump = 4
		if self.is_jump == 4:
			self.rect.y += 8
		if self.rect.y > self.default_y - 1:
			self.rect.y = self.default_y
			self.is_jump = 0

	def move(self, speed):
		if self.rect.x <= 720 - 40 and speed > 0:
			self.rect.x += speed
			self.is_right = True
		elif 0 <= self.rect.x and speed < 0:
			self.rect.x += speed
			self.is_right = False

	def spawn(self, x=3):
		self.game.all_ennemies.add(*(Squar(self) for i in range(x)))

	def shoot(self):
		self.all_projectile.add(Projectile(self))


	def update(self):
		if self.game.check_collide(self, self.game.all_ennemies):
			self.game.stat = "Game over"
			return self.nbr

	def sprint(self):
		if self.is_sprinting:
			x = self.dico_right[self.is_right]
			if self.rect.x + x >= 680:
				self.is_sprint_on_wall = True
				self.rect.x += 680 - self.rect.x
			if -4 >= self.rect.x + x:
				self.rect.x = 0
				self.is_sprint_on_wall = True
			elif self.is_right:
				self.rect.x += 16
				if self.rect.x >= self.original_x + 64 or self.is_sprint_on_wall:
					self.is_sprinting = False
					self.is_sprint_on_wall = False
			elif not self.is_right:
				self.rect.x -= 16
				if self.rect.x <= self.original_x - 64:
					self.is_sprinting = False
		else:
			self.original_x = self.rect.x
