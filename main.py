import pygame, random, time
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
def control_enemies():
	if start_level == True:
		if len(enemies) <= 2:
			enemies.append( [random.randint(50, 400), random.randint(-100, 0)] ) 
		move_enemies()
def move_enemies():
	if current_level == 1:
		count = 0
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
pygame.init()
 
# Define some color
BLACK = ( 0, 0, 0 )
WHITE = ( 255, 255, 255 )
GREEN = ( 0, 255, 0 )
RED = ( 255, 0 , 0 )
# define gameplay related features
score = 0
FONT = pygame.font.Font(None, 25)
text = FONT.render("PRESS ENTER TO START", True, WHITE)
level1_text = FONT.render("LEVEL 1", True, WHITE)
score_text = FONT.render("Score: "+str(score), True, GREEN)
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
current_level = 0
num_lives = 3
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
    #Game start EVENT
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
  control_enemies()
  score += cleanup_enemies()
# ALL CODE TO DRAW SHOULD GO BELOW
  screen.fill(BLACK)
  display_level(level1_text)
  draw_instructions(num_lives)
  draw_player()
  draw_enemies()
  pygame.display.flip()
 
  clock.tick(20)
pygame.quit()