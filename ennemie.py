import pygame
import random


class Ennemie(pygame.sprite.Sprite):
	"""docstring for Ennemie"""
	def __init__(self, image, player):
		super().__init__()
		self.player = player
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = random.randint(720, 1200)
		self.rect.y = player.default_y + 40 - self.image.get_height()


	def spawn(self, screen):
		screen.blit(self.image, self.rect)


class Squar(Ennemie):
	"""docstring for Squar"""
	def __init__(self, player):
		image = pygame.Surface(random.choice(((20, 20), (35, 35), (50, 50))))
		image.fill((250, 128, 114))
		super().__init__(image, player)
		self.game = self.player.game
		self.velocity =  random.randint(4, 6)

	def move(self):
		self.rect.x -= self.velocity
