import pygame, random, time, os	
from threading import Timer
'''
All functions should be moved elsewhere but this is a single file project so yea
'''
def draw_instructions(lives):
  if started == False:
  	screen.blit(text, [250,250])
  else:
  	draw_scoreboard(lives)
def draw_scoreboard(num_lives):
	new_text = FONT.render("Score: "+str(score), False, GREEN)
	lives = FONT.render("Lives: ", False, GREEN)
	icon = pygame.transform.scale(player_img, (20, 20))
	screen.blit(new_text, [5,5])
	screen.blit(lives, [150,5])
	draw_lives(icon, num_lives)
def draw_player():
	if started == True:
		screen.blit(player_img, player_coords)
def draw_lives(icon, num_lives):
	lives = num_lives
	x_coord = 205
	while lives > 0:
		screen.blit(icon, (x_coord, 5))
		x_coord += 25
		lives -= 1
def display_game_over():
	screen.blit(game_over_text, [250, 250])		
def display_level(texts):
	if show_level == True:
		screen.blit(texts, [250,250])
def turn_on_level_label():
	show_level = True
def turn_off_level_label(show_level):
	show_level = False
def cleanup_enemies():
	points = 0
	for each in enemies:
		if each[1] > 500:
			points += 5
			enemies.remove(each)
	return points
def control_enemies(lives, hit):
	new_lives = lives
	if start_level == True:
		if len(enemies) <= 2:
			enemies.append( [random.randint(50, 400), random.randint(-100, 0)] ) 
		new_lives = move_enemies(lives, hit)
	return new_lives
def check_collision(enemy_coords, name):
	left1, left2 = enemy_coords[0], player_coords[0]
	right1, right2 = enemy_coords[0]+50, player_coords[0]+75
	top1, top2 = enemy_coords[1], player_coords[1]
	bottom1, bottom2 = enemy_coords[1]+50, player_coords[1]+75
	
	if bottom1 < top2:
		return 0
	if top1 > bottom2:
		return 0
	if right1 < left2:
		return 0
	if left1 > right2:
		return 0
	if name == 'flyer':
		
		return 1	
def move_enemies(lives, hit_sound):
	if current_level == 1:
		count = 0
		new_lives = lives
		for each in enemies:
			count += 1
			'''THE LEVEL 1 EFFECT
				makes the second enemy fall down and across the screen faster
				forces enemies to 'jerk' at times when quick enemies are being removed
			'''
			if count == 2:
				if each[0] > 0:
					each[0] += 7
				elif each[0] < 700:
					each[0] -= 7	
				each[1] += 15
			else:
				each[1] += 9
			#there is a collision
			if check_collision(each, 'flyer') == 1:
				enemies.remove(each)
				new_lives -= 1
				hit_sound.play()
		return new_lives
				
		
def draw_enemies():
	for each in enemies:
		screen.blit(enemy_img, each)
def move_up():
	player_coords[1] -= y_speed
	moving = True
def move_down():
	player_coords[1] += y_speed
	moving = True
def move_left():
	player_coords[0] -= x_speed
	moving = True
def move_right():
	player_coords[0] += x_speed
	moving = True
def stop_move():
	moving = False
def increase_score(score, value):
	new_score = score + value
	return new_score
pygame.mixer.pre_init(44100, -16,2, 2048)
pygame.init()
 
# Define some color
BLACK = ( 0, 0, 0 )
WHITE = ( 255, 255, 255 )
GREEN = ( 0, 255, 0 )
RED = ( 255, 0 , 0 )
# define gameplay related features
score = 0
pygame.mixer.music.load(os.path.join('sound', 'stardust.ogg'))
hit = pygame.mixer.Sound(os.path.join('sound', 'hit.wav'))
over = pygame.mixer.Sound(os.path.join('sound', 'over.wav'))
FONT = pygame.font.Font(None, 25)
text = FONT.render("PRESS ENTER TO START", True, WHITE)
level1_text = FONT.render("LEVEL 1", True, WHITE)
score_text = FONT.render("Score: "+str(score), True, GREEN)
game_over_text = FONT.render("GAME OVER!", True, RED)
# Set the width and height of the window
size = (700,500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Play Dodger")
 
#Loop until user clicks close
done = False
clock = pygame.time.Clock()
player_coords = [450, 400]
x_speed = 11
y_speed = 10
moving = False
player_img = pygame.image.load("img/player.png")
enemy_img = pygame.image.load("img/flyer.png")
enemies = []
# Game management flags
started = False 
show_level = False
start_level = False
game_over = False
current_level = 0
num_lives = 3
pygame.mixer.music.play(-1)
while done == False:
  # ALL EVENT PROCESSING SHOULD GO BELOW
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
    	done = True
    if event.type == pygame.KEYUP:
    	if event.key == pygame.K_DOWN:
    		stop_move()
    	elif event.key == pygame.K_RIGHT:
    		stop_move()
    	elif event.key == pygame.K_LEFT:
    		stop_move()
    #Level 1 Start EVENT
    if event.type == pygame.USEREVENT+1:
		show_level = False
		start_level = True
	  	current_level = 1
  keys_pressed = pygame.key.get_pressed()
  if keys_pressed[pygame.K_UP]:
  	move_up()
  elif keys_pressed[pygame.K_DOWN]:
  	move_down()
  elif keys_pressed[pygame.K_LEFT]:
  	move_left()
  elif keys_pressed[pygame.K_RIGHT]:
  	move_right()
  elif keys_pressed[pygame.K_RETURN]:
	if started == False:
  		started = True
  		show_level = True
		pygame.time.set_timer(pygame.USEREVENT+1,1500)
  
# ALL GAME LOGIC SHOULD GO BELOW
  num_lives = control_enemies(num_lives, hit)
  if num_lives == 0:
  	pygame.mixer.music.fadeout(1000)
  	game_over = True
  	over.play()
  score += cleanup_enemies()
# ALL CODE TO DRAW SHOULD GO BELOW
  screen.fill(BLACK)
  if game_over == True:
  	display_game_over()
  else:
	  display_level(level1_text)
	  draw_instructions(num_lives)
	  draw_player()
	  draw_enemies()
  pygame.display.flip()
 
  clock.tick(20)
pygame.quit()