import pygame

class Projectile(pygame.sprite.Sprite):

	def __init__(self, player):
		super().__init__()
		self.player = player
		self.image = pygame.image.load('png/projectile.png')
		self.image = pygame.transform.scale(self.image, (10, 10))
		self.rect = self.image.get_rect()
		self.rect.x = self.player.rect.x + 45
		self.rect.y =  self.player.rect.y + 30
		self.original_image = self.image
		self.angle = 0

	def rotate(self):
		self.angle += 20
		self.image = pygame.transform.rotate(self.original_image, self.angle)
		self.rect = self.image.get_rect(center=self.rect.center)

	def move(self):
		if not self.rect.x >= 720:
			self.rect.x += 5
		else:
			self.player.all_projectile.remove(self)
		self.rotate()
		for player in self.player.game.all_players:
			if self.player.game.check_collide(self, player.game.all_ennemies, True):
				self.player.all_projectile.remove(self)
