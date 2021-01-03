import pygame


class Write:
	"""docstring for Write"""
	def __init__(self, string, value, y, screen, font=None, color=(255, 255, 255)):
		self.width = screen.get_width() // 2
		pygame.font.init()
		if font == None:
			self.font = pygame.font.SysFont("arial", 25)
		else:
			self.font = font
		self.string = string
		self.count = 0
		self.color = color
		self.value = value
		self.y = y
		self.x = self.width - 5 * len(string)
		self.is_finished = False

	def print(self, screen):
		"""cette fonction est utilisé pour affucher et dans la boucle principal"""
		self.surface = self.font.render(self.string[0: self.count], False, self.color)
		screen.blit(self.surface, (self.x, self.y))

	def print_all(self, screen):
		self.surface = self.font.render(self.string, False, self.color)
		screen.blit(self.surface, (self.x, self.y))

	def event(self, event):
		"""cette fonction permet de calculer le timelaps et utilisé dans la boucle d'evenement"""
		if event.type == self.value:
			self.add()

	def set_event(self, cooldown=70):
		"""utilisé pour définir le temps de cooldown il est par defauts à 100"""
		pygame.time.set_timer(self.value, cooldown)

	def add(self):
		"""cette fonction est utilisé pour ajouter le conteur et inutilsé en dehors d'une autre fonction"""
		if self.count <= len(self.string):
			self.count += 1
		else:
			self.is_finished = True

	def __repr__(self):
		return f"Write('{self.string}'), ({self.x}, {self.y})"


class Queue:
	"""docstring for queue"""
	def __init__(self, liste, separator: int, screen, font=None, skip_font=None):
		liste.append("")
		self.queue = [Write(string, nbr, nbr2, screen, font) for string, nbr, nbr2 in zip(liste, [*range(32782, 32782 + len(liste))], [*range(10, separator*len(liste), separator)])]
		self.counter = 0
		self.is_started = False
		self.current_queue = []
		self.is_finished = False
		self.font = pygame.font.SysFont("arial", 25) if skip_font == None else skip_font
		self.skip_color = (255, 255, 255)
		self.skip = self.font.render("SKIP", False, self.skip_color)
		self.skip_rect = self.skip.get_rect()
		self.skip_rect.y = screen.get_height() - 50
		self.skip_rect.x = screen.get_width() - self.skip.get_width() - 20

	def start(self, screen):
		screen.blit(self.skip, self.skip_rect)
		if self.is_started:
			self.current.print(screen)
			for writer in self.current_queue:
				writer.print_all(screen)
			self.skip = self.font.render("SKIP", False, self.skip_color)
		else:
			self.current = self.queue[self.counter]
			self.current.print(screen)
			for writer in self.current_queue:
				writer.print_all(screen)
			self.skip = self.font.render("SKIP", False, self.skip_color)
			self.current.set_event(40)
			self.is_started = True
		if self.current.is_finished and self.counter != len(self.queue) - 1:
			self.current_queue.append(self.current)
			self.counter += 1
			self.is_started = False
		if self.skip_rect.collidepoint(pygame.mouse.get_pos()):
			self.skip_color = (250, 250, 0)
		else:
			self.skip_color = (255, 255, 255)

	def event(self, event):
		self.queue[self.counter].event(event)
		if event.type == pygame.MOUSEBUTTONDOWN:
			if self.skip_rect.collidepoint(event.pos):
				self.is_finished = True
		if event.type == pygame.K_RIGHT:
			pass



if __name__ == '__main__':
	stat = "in game"
	pygame.init()
	liste = [
		"salut tout le monde",
		"je suis akito le createur du jeu",
		"j'espère que vous vous amuseriez avec mon jeu",
		"bon après ce n'est qu'un petit jeu ",
		"alors ne vous attendez pas à grand chose",
		"peut être que vous le detesteriez...",
		"et vous en avez le droit ^^'",
		"mais rappelez vous d'une seul chose",
		"ne baissez jamais les bras ...",
		"paroles d'un akitologue ^^"
		]

	screen = pygame.display.set_mode((500, 500))
	pygame.display.set_caption("test")
	queue = Queue(liste, 40, screen)

	running = True
	while running:
		if stat == "in game":
			screen.fill((0, 0, 0))
			if not queue.is_finished:
				queue.start(screen)
			else:
				stat = "start"
		elif stat == "start":
			pass
		pygame.display.flip()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				pygame.quit()
			if not queue.is_finished:
				queue.event(event)
