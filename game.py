import pygame
from player import Player
from queue_ import Queue


class Game:
	"""docstring for Game"""
	def __init__(self, screen):
		pygame.mixer.init()
		self.pixel_font = pygame.font.Font("font/karma future.ttf", 23)
		self.pixel_skip_font = pygame.font.Font("font/Beef'd.ttf", 17)
		self.mode = "cinematique"
		self.player = Player(1, [pygame.K_UP, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_DOWN, pygame.K_p, pygame.K_m, pygame.K_x], [30, 200], self, (5, 216, 255))
		self.all_players = pygame.sprite.Group(self.player)
		self.all_ennemies = pygame.sprite.Group()
		self.switch_event = pygame.USEREVENT + 10
		self.font = pygame.font.SysFont('impact', 25, bold=False)
		self.font2 = pygame.font.SysFont('arial', 24, bold=False)
		self.surfaces = {} 
		self.chooser = Chooser(self)
		self.is_switch = True
		self.stat = "in game"
		self.dico = {1: "green", 2: "blue"}
		self.is_played_sound = True
		self.is_affiched = False
		self.liste = ["salut je suis akito",
		"j'espère que vous vous amuseriez avec mon jeu",
		"après il n'est pas terminé",
		"et ce n'est qu'un prototype",
		"mais je veux que vous le testeriez quand même",
		"et soyez détériminé",
		"c'est la seule chose que je peux vous dire"
		]
		self.queue = Queue(self.liste, 60, screen, font=self.pixel_font, skip_font=self.pixel_skip_font)
		self.music_started = False
		self.color_lost = (255, 255, 255)
		self.lost = self.pixel_skip_font.render("tu as perdu", False, self.color_lost)
		self.lost_rect = self.lost.get_rect()
		self.lost_rect.x, self.lost_rect.y = (720 - self.lost.get_width() - 30, 0 + self.lost.get_height() + 120)
		self.secret_mode = False
		self.color_return = (255, 255, 255)
		self._return = self.pixel_skip_font.render("return", False, self.color_return)
		self._return_rect = self._return.get_rect()
		self._return_rect.x, self._return_rect.y = (screen.get_width() - 50 - self._return.get_width(), screen.get_height() - 50 - self._return.get_height())
		self.score = 0


	def update_lost(self):
		self.lost = self.pixel_skip_font.render("tu as perdu", False, self.color_lost)

	def draw(self, screen):
		self.all_players.draw(screen)
		self.all_ennemies.draw(screen)

	def draw_lines(self, two=False):
		surface = pygame.Surface((720, 480))
		surface.fill((0, 0, 0))
		pygame.draw.line(surface, (255, 255, 255), (0, surface.get_height()/2), (surface.get_width(), surface.get_height()/2))
		if two:
			pygame.draw.line(surface, (255, 255, 255), (0, surface.get_height() - 10), (surface.get_width(), surface.get_height() - 10))
		return surface

	def switch(self):
		self.player.rect, self.player2.rect = self.player2.rect, self.player.rect
		self.player.default_y, self.player2.default_y = self.player2.default_y, self.player.default_y
		self.player.is_jump, self.player2.is_jump = self.player2.is_jump, self.player.is_jump

	def check_collide(self, sprite, group, remove=False):
		return pygame.sprite.spritecollide(sprite, group, remove, pygame.sprite.collide_mask)

	def write(self, string):
		return self.font.render(string, False, (255, 255, 255))

	def write2(self, string):
		return self.font2.render(string, False, (124, 255, 25))

	def start_music(self):
		pygame.mixer.music.load("png/Reset.mp3")
		pygame.mixer.music.set_volume(0.3)
		pygame.mixer.music.play(-1)
		self.music_started = True

	def reset_queue(self, screen):
		self.queue = Queue(self.liste, 60, screen, font=self.pixel_font, skip_font=self.pixel_skip_font)

	def secret(self):
		self.player2 = Player(2, [pygame.K_z, pygame.K_d, pygame.K_q, pygame.K_s, pygame.K_b, pygame.K_n, pygame.K_v], [30, 430], self, (119, 216, 144))
		self.all_players.add(self.player2)


class Chooser:
	"""docstring for chooser"""
	def __init__(self, game):
		self.image = pygame.transform.scale(pygame.image.load("png/chooser.png"), (32, 32))
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = (200, 140)
		self.pos = 1
		self.game = game
		self.dico_pos = {k: v for k, v in zip(tuple(range(1, 5)), ((200, 140), (200, 200), (200, 260), (200, 320)))}
		self.dico_val = {k: v for k, v in zip(tuple(range(1, 5)), ("cinematique", "in game", "help", "config"))}

	def draw(self, screen):
		screen.blit(self.image, self.rect)

	def move(self, event, screen):
		if self.game.mode == "title screen":
			if event.key == pygame.K_UP and self.pos - 1 != 0:
				self.pos -= 1
				self.rect.x, self.rect.y = self.dico_pos[self.pos]
			elif event.key == pygame.K_DOWN and self.pos + 1 != 5:
				self.pos += 1
				self.rect.x, self.rect.y = self.dico_pos[self.pos]
			if event.key == pygame.K_SPACE:
				if self.dico_val[self.pos] == "cinematique":
					self.game.reset_queue(screen)
					pygame.mixer.music.stop()
				elif self.dico_val[self.pos] == "in game" and self.game.secret_mode:
					self.game.secret()
					self.game.mode = "in secret game"
				elif self.dico_val[self.pos] == "in game" and len(self.game.all_players) == 2:
					self.game.all_players.remove(self.game.player2)
					self.game.player.rect.x = 30
				self.game.mode = self.dico_val[self.pos] if not self.game.mode == "in secret game" else "in secret mode"
