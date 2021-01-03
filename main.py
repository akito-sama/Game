import pygame
from game import Game

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((720, 480))
pygame.display.set_caption("not a game")

game = Game(screen)
white = (255, 255, 255)
clock = pygame.time.Clock()
running = True
surface = game.draw_lines()
surface2 = game.draw_lines(True)
EVENT = pygame.USEREVENT + 2
SURFACEEVENT = pygame.USEREVENT + 3
surface_error = game.write("vous ne pouvez pas switcher")
is_drawed = False
liste_title_screen = [(game.pixel_skip_font.render(text, False, white), (screen.get_width()/3, screen.get_height()/2 - 160)) for text in ["title screen", "play", "help", "config"]]
liste_help_screen = [(game.pixel_skip_font.render(text, False, white), (20, screen.get_height()/3 - 160)) for text in ["faut eviter les obstacles", "sauver toi meme", "fuir des menaces rouge", "appuyer sur haut pour sauter", "appuyer sur droite pour tirer"]]
liste_config_screen = [(game.pixel_skip_font.render(text, False, white), (20, screen.get_height()/3 - 160)) for text in ["pas encore fait"]]
pygame.time.set_timer(32795, 2500)
pygame.time.set_timer(32794, 60)
creat = lambda string: game.pixel_skip_font.render(string, False, white)

while running:
	screen.fill((0, 0, 0))
	if game.mode == "in secret mode":
		line = 0
		screen.blit(surface2, (0, 0))
		game.draw(screen)
		for ennemie in game.all_ennemies:
			ennemie.move()
		for player in game.all_players:
			player.jump()
			player.sprint()
			winner = player.update()
			for projectile in player.all_projectile:
				projectile.move()
			if pygame.key.get_pressed()[player.right]:
				player.move(4)
			elif pygame.key.get_pressed()[player.left]:
				player.move(-4)
			player.all_projectile.draw(screen)
			if game.stat == "Game over":
				game._return = game.pixel_skip_font.render("return", False, game.color_return)
				player.all_projectile = pygame.sprite.Group()
				game.all_ennemies = pygame.sprite.Group()
				screen.blit(game._return, game._return_rect)
				game.color_return = (250, 250, 0) if game._return_rect.collidepoint(pygame.mouse.get_pos()) else (255, 255, 255)
				if not is_drawed:
					pygame.display.set_caption(f"the winner is {game.dico[winner]}")
					winner_surface = game.write(f"the winner is {game.dico[winner]}")
					game.surfaces[winner_surface] = (360, 10)
					winner_surface2 = game.write2("Copyright akito thanks to respect it")
					game.surfaces[winner_surface2] = (323, 10)
					is_drawed = True
	elif game.mode == "in game":
		screen.blit(surface, (0, 0))
		game.draw(screen)
		for player in game.all_players:
			player.jump()
			winner = player.update()
			for projectile in player.all_projectile:
				projectile.move()
			player.all_projectile.draw(screen)
		for ennemie in game.all_ennemies:
			ennemie.move()
		if game.stat == "Game over":
			game.all_ennemies = pygame.sprite.Group()
			game.update_lost()
			game.player.all_projectile = pygame.sprite.Group()
			screen.blit(game.lost, game.lost_rect)
			game.color_lost = (250, 250, 0) if game.lost_rect.collidepoint(pygame.mouse.get_pos()) else (255, 255, 255)
		screen.blit(creat(f"score : {game.score}"), (0, 0))

	elif game.mode == "help":
		j = 0
		for i in liste_help_screen:
			j += 60
			screen.blit(i[0], (i[1][0], i[1][1] + j))
		game._return = game.pixel_skip_font.render("return", False, game.color_return)
		screen.blit(game._return, game._return_rect)
		game.color_return = (250, 250, 0) if game._return_rect.collidepoint(pygame.mouse.get_pos()) else (255, 255, 255)

	elif game.mode == "cinematique":
		screen.fill((0, 0, 0))
		if not game.queue.is_finished:
			game.queue.start(screen)
		else:
			if not game.music_started:
				game.start_music()
			game.mode = "title screen"
			pygame.mixer.music.play(-1)

	elif game.mode == "title screen":
		j = 0
		for i in liste_title_screen:
			j += 60
			screen.blit(i[0], (i[1][0], i[1][1] + j))
		game.chooser.draw(screen)

		if pygame.key.get_pressed()[pygame.K_a] and pygame.key.get_pressed()[pygame.K_k] and pygame.key.get_pressed()[pygame.K_o]:
			game.secret_mode = True
		if pygame.key.get_pressed()[pygame.K_a] and pygame.key.get_pressed()[pygame.K_k] and pygame.key.get_pressed()[pygame.K_t]:
			game.secret_mode = False

		if game.secret_mode:
			screen.blit(game.pixel_skip_font.render("secret mode activate", False, (255, 255, 255)), (screen.get_width()//5, 50))

	elif game.mode == "config":
		game._return = game.pixel_skip_font.render("return", False, game.color_return)
		screen.blit(game._return, game._return_rect)
		game.color_return = (250, 250, 0) if game._return_rect.collidepoint(pygame.mouse.get_pos()) else (255, 255, 255)
		j = 0
		for i in liste_config_screen:
			j += 60
			screen.blit(i[0], (i[1][0], i[1][1] + j))

	for i, j in game.surfaces.items():
		screen.blit(i, (j[0], j[1] + line))
		line += 30
	clock.tick(60)
	pygame.display.flip()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			pygame.quit()
		if event.type == pygame.KEYDOWN:
			game.chooser.move(event, screen)
			if game.mode == "in secret mode":
				for player in game.all_players:
					if event.key == player.K_jump and player.is_jump == 0:
						player.is_jump = 1
					if event.key == player.spr_key:
						player.is_sprinting = True
					if game.stat == "in game":
						if event.key == player.switch:
							if game.is_switch == True:
								pygame.time.set_timer(game.switch_event, 1000, True)
								surface_tell = game.write("le switch a commencé")
								game.is_affiched = True
								game.surfaces[surface_tell] = (360, 10)
								pygame.time.set_timer(EVENT, 7500, True)
								game.is_switch = False
							else:
								if surface_error not in game.surfaces:
									game.surfaces[surface_error] = (360, 10)
								pygame.time.set_timer(32775, 1000, True)
						if event.key == player.s_key and player.is_possible:
							player.shoot()
							player.is_possible = False
							if player.nbr == 1:
								pygame.time.set_timer(32776, 800, True)
							elif player.nbr == 2:
								pygame.time.set_timer(32777, 800, True)

						if event.key == player.sp_key and player.is_possible_spawn:
							if player.nbr == 1:
								game.player2.spawn()
								pygame.time.set_timer(32778, 1500, True)
							elif player.nbr == 2:
								game.player.spawn()
								pygame.time.set_timer(32779, 1500, True)
							player.is_possible_spawn = False
			elif game.mode == "in game":
				for player in game.all_players:
					if event.key == player.K_jump and player.is_jump == 0:
						player.is_jump = 1
					elif event.key == pygame.K_RIGHT and player.is_possible and game.stat != "Game over":
						player.shoot()
						player.is_possible = False
						pygame.time.set_timer(32776, 800, True)
		if game.mode == "in secret mode" or game.mode == "in game":
			pass
		if game.mode == "in secret mode":
			if event.type == game.switch_event:
				if game.is_affiched:
					game.switch()
					del game.surfaces[surface_tell]
			if event.type == EVENT:
				game.is_switch = True

			if event.type == 32775:
				if game.is_affiched:
					del game.surfaces[surface_error]
			if event.type == 32777:
				game.player2.is_possible = True
			if event.type == 32778:
				game.player.is_possible_spawn = True
			if event.type == 32779:
				game.player2.is_possible_spawn = True

		if event.type == 32776:
			game.player.is_possible = True
		if not game.queue.is_finished:
			game.queue.event(event)
		elif game.mode == "in game":
			if event.type == 32795:
				for player in game.all_players:
					player.spawn(4)
			elif event.type == 32794 and game.stat == "in game":
				game.score += 1
		if event.type == pygame.MOUSEBUTTONDOWN:
			if game.lost_rect.collidepoint(event.pos) and game.stat == 'Game over' and game.mode == "in game":
				game.stat = 'in game'
				game.mode = "title screen"
				game.score = 0
			if game._return_rect.collidepoint(event.pos) and ((game.stat == 'Game over' and game.mode == "in secret mode") or game.mode in ["help", "config"]):
				game.stat = 'in game'
				game.mode = "title screen"


# copyright butterfly
