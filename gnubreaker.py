'''
Copyright 2016 Michael Collins

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

'''
GnuBreaker 0.4.6

To Do List:
???
'''

import sys, pygame, time, random, math, operator
from random import randint


# 2DVector class, a vector describes multiple degrees of motion!
class Vec2d(object):
	"""2d vector class, supports vector and scalar operators,
	   and also provides a bunch of high level functions
	   """
	__slots__ = ['x', 'y']

	# Initialises vector with x and y directions
	def __init__(self, x_or_pair, y = None):
		if y == None:
			self.x = x_or_pair[0]
			self.y = x_or_pair[1]
		else:
			self.x = x_or_pair
			self.y = y

	# Return amount of dimensions
	def __len__(self):
		return 2

	# Read vector x and y values, 0 returns x and 1 returns y
	def __getitem__(self, key):
		if key == 0:
			return self.x
		elif key == 1:
			return self.y
		else:
			raise IndexError("Invalid subscript "+str(key)+" to Vec2d")

	#Set vector x and y values
	def __setitem__(self, key, value):
		if key == 0:
			self.x = value
		elif key == 1:
			self.y = value
		else:
			raise IndexError("Invalid subscript "+str(key)+" to Vec2d")
 

class Player:
	def __init__(self,X):
		Y = 600
		self.direction = 0 #left/right -4/+4
		self.object_image = pygame.image.load("./Images/player.png")
		self.object_boundary = self.object_image.get_rect (center=(X,Y))
		self.is_brick = False
		self.health = 3
		#self.sound1 = pygame.mixer.Sound ('yeah.ogg')
		#self.sound2 = pygame.mixer.Sound ('okay.ogg')

class Heart_Symbol:
	def __init__(self,X):
		Y = 630
		self.object_image = pygame.image.load("./Images/heart.png")
		self.object_boundary = self.object_image.get_rect (center=(X,Y))
		self.flash_out = 3

class Health_Symbol:
	def __init__(self):
		health_Y = 630
		health_X = 30
		self.object_image = pygame.image.load("./Images/health.png")
		self.object_boundary = self.object_image.get_rect (center=(health_X,health_Y))

class Dropping_Item:
	def __init__(self,X,Y,vector,special_type):
		self.image_array = ['./Images/heart.png','./Images/mushroom.png']
		self.object_image = pygame.image.load(self.image_array[special_type])
		self.special_type = special_type
		#Types: 0 = heart, 1 = shroom
		self.object_boundary = self.object_image.get_rect (center=(X,Y))
		self.velocity = Vec2d(vector[0],vector[1])
		self.flash_out = 3
		#self.sound1 = pygame.mixer.Sound ('./Audio/boing1.ogg')
		#A magical number shrouded in mystery
		self.dt = 0.01

	def apply_gravity_to_dropping_item(self):
		if self.object_boundary.y < 1:
			self.velocity[1] = -self.velocity[1]
		elif self.object_boundary.y >= 1:
			self.velocity[1] = self.velocity[1] + 9.8*self.dt

	def limit_dropping_speed(self,x_min,x_max,y_min,y_max):
		if self.velocity[1] < y_min:
			self.velocity[1] = y_min
		elif self.velocity[1] > y_max:
			self.velocity[1] = y_max
	
		if self.velocity[0] < x_min:
			self.velocity[0] = x_min
		elif self.velocity[0] > x_max:
			self.velocity[0] = x_max

	def dropping_inside_object(self,object_boundary):
		if self.object_boundary.colliderect(object_boundary):
			return True
		else:
			return False

	def dropping_item_hit_screen_boundary(self,x_limit,y_limit):
		if self.object_boundary.right >= x_limit or self.object_boundary.left <= 0:
			self.velocity = [-(self.velocity[0]),self.velocity[1]]
			#self.sound1.play()
			return False
		elif self.object_boundary.top <= 0:
			self.velocity = [self.velocity[0],abs(self.velocity[1])]
			#self.sound1.play()
			return False
		elif self.object_boundary.bottom > y_limit:
			self.velocity = [0,0]
			#self.sound1.play()
			if len(dropping_array) > 1:
				return True
			elif len(dropping_array) == 1:
				flashing_array.append(dropping_array.pop())
				return False
		return False

	def process_dropping(self,trip_time_out,trip_boolean,colours_alt):
		self.apply_gravity_to_dropping_item()
		self.limit_dropping_speed(-5,5,-5,5)

		destroy_dropping = self.dropping_item_hit_screen_boundary(600,640)

		if destroy_dropping == True:
			dropping_array.remove(self)
			destroy_dropping = False

		if self.object_boundary.y > 570:
			if self.dropping_inside_object(paddle.object_boundary) == True and self.special_type == 0:
				dropping_array.remove(self)
				paddle.health = paddle.health + 1
				hearts_array.append(Heart_Symbol(70 + ((paddle.health - 1) * 20)))
			elif self.dropping_inside_object(paddle.object_boundary) == True and self.special_type == 1:
				dropping_array.remove(self)
				trip_boolean = True
				colours_alt = gen_pos_neg_one(), gen_pos_neg_one(), gen_pos_neg_one()
				pygame.mixer.music.load('./Audio/trip.ogg')
				pygame.mixer.music.play()
				trip_time_out = 350

		self.object_boundary.clamp_ip(screen_rect)

		self.object_boundary = self.object_boundary.move(self.velocity[0],self.velocity[1])
		return trip_time_out,trip_boolean,colours_alt

class Ball:
	def __init__(self,X,Y,vector,colour_int):
		self.image_array = ['./Images/Balls/ball-orange.png','./Images/Balls/ball-yellow.png','./Images/Balls/ball-green.png','./Images/Balls/ball-lightblue.png','./Images/Balls/ball-darkblue.png','./Images/Balls/ball-purple.png','./Images/Balls/ball-magenta.png','./Images/Balls/ball-red.png']
		self.colour_integer = colour_int
		self.object_image = pygame.image.load(self.image_array[self.colour_integer])
		self.object_boundary = self.object_image.get_rect (center=(X,Y))
		self.velocity = Vec2d(vector[0],vector[1])
		self.sound1 = pygame.mixer.Sound ('./Audio/boing1.ogg')
		#A magical number shrouded in mystery
		self.dt = 0.01

	#module increases y velocity according to gravity
	def apply_gravity_to_ball(self):
		if self.object_boundary.y < 1:
			self.velocity[1] = -self.velocity[1]
		elif self.object_boundary.y >= 1:
			self.velocity[1] = self.velocity[1] + 9.8*self.dt

	#This function determines if ball is inside paddle/brick boundary then returns true.
	def ball_inside_object(self,object_boundary):
		if self.object_boundary.colliderect(object_boundary):
			return True
		else:
			return False

	#This function corrects the ball if it is out of bounds, returns the health of the player
	def ball_hit_screen_boundary(self,x_limit,y_limit,health,cut_bool):
		if self.object_boundary.right >= x_limit or self.object_boundary.left <= 0:
			self.velocity = [-(self.velocity[0]),self.velocity[1]]
			self.sound1.play()
			return health, False
		elif self.object_boundary.top <= 0:
			self.velocity = [self.velocity[0],abs(self.velocity[1])]
			self.sound1.play()
			return health, False
		elif self.object_boundary.bottom > y_limit and cut_bool == False:
			self.velocity = [self.velocity[0],-(self.velocity[1]*0.8)]
			self.sound1.play()
			if len(ball_array) > 1:
				return health, True
			elif len(ball_array) == 1:
				health = health - 1
				flashing_array.append(hearts_array.pop())
				time.sleep(1)
				self.velocity[0] = randint(-2,2)
				self.velocity[1] = 1
				self.object_boundary.x = 200
				self.object_boundary.y = 570
				paddle.object_boundary.x = 160
				return health, False
		elif self.object_boundary.bottom > y_limit and cut_bool == True:
				self.velocity = [self.velocity[0],-(self.velocity[1]*0.8)]
				self.sound1.play()
				return health, False
		return health, False

	#examine the balls speed and limit it!
	def limit_ball_speed(self,x_min,x_max,y_min,y_max):
		if self.velocity[1] < y_min:
			self.velocity[1] = y_min
		elif self.velocity[1] > y_max:
			self.velocity[1] = y_max
	
		if self.velocity[0] < x_min:
			self.velocity[0] = x_min
		elif self.velocity[0] > x_max:
			self.velocity[0] = x_max
		
	#This function calculates the new x,y direction for the ball and sets it, only called if collision is true.
	def ball_rebound_calc(self,object_boundary):
		#hits from above or below and is inside corners
		if self.object_boundary.left >= (object_boundary.left)-1 and self.object_boundary.right <= (object_boundary.right)+1:
			#reverse Y velocity!
			self.velocity[1] = -self.velocity[1]
		#hits top left corner
		elif self.object_boundary.left < (object_boundary.left)-1 and self.object_boundary.top < object_boundary.top:
			self.velocity[0] = -(abs(self.velocity[0]))
			self.velocity[1] = -self.velocity[1]
		#hits top right corner
		elif self.object_boundary.right > (object_boundary.right)+1 and self.object_boundary.top < object_boundary.top:
			self.velocity[0] = abs(self.velocity[0])
			self.velocity[1] = -self.velocity[1]
		#hits bottom left corner
		elif self.object_boundary.left < (object_boundary.left)-1 and self.object_boundary.bottom > object_boundary.bottom:
			self.velocity[0] = -(abs(self.velocity[0]))
			self.velocity[1] = -self.velocity[1]
		#hits bottom right corner
		elif self.object_boundary.right > (object_boundary.right)+1 and self.object_boundary.bottom > object_boundary.bottom:
			self.velocity[0] = abs(self.velocity[0])
			self.velocity[1] = -self.velocity[1]
		#hits left/right side
		else:
			self.velocity[0] = -(self.velocity[0])

	#this module stops the ball if its close to the ground and had nearly no velocity
	def stop_non_moving_ball(self):
		if self.object_boundary.bottom == 640 and self.velocity[1] < 1:
			self.velocity = [0,0]

	def process_ball(self, cut_bool):
		#apply gravity to balls y velocity
		self.apply_gravity_to_ball()
		#limit balls speed
		self.limit_ball_speed(-5,5,-11,10)

		#redirect ball it it has hit the boundary, decrement paddle health if needed
		paddle.health,destroy_ball = self.ball_hit_screen_boundary(600,640,paddle.health,cut_bool)

		if destroy_ball == True:
			ball_array.remove(self)
			destroy_ball = False

		#for each brick, if the ball has hit it, calculate rebound then decrement health, delete brick is health too low
		for brick in bricks_array:
			if self.object_boundary.y < 300:
				if self.ball_inside_object(brick.object_boundary) == True:
					self.ball_rebound_calc(brick.object_boundary)
					brick.health = brick.health - 1
					if brick.return_special_bool() == True:
						if brick.special_type == 'ball':
							random_num = randint(0,7)
							ball_array.append(Ball(brick.object_boundary.x,brick.object_boundary.y,[1,1],random_num))
						elif brick.special_type == 'shroom':
							dropping_array.append(Dropping_Item(brick.object_boundary.x,brick.object_boundary.y,[1,1],1))
						elif brick.special_type == 'heart':
							dropping_array.append(Dropping_Item(brick.object_boundary.x,brick.object_boundary.y,[1,1],0))
					if brick.health <= 0:
						flashing_array.append(brick)
						bricks_array.remove(brick)
						brick.sound1.play()
					elif brick.health == 2:
						brick.object_image = pygame.image.load('./Images/Bricks/hard-brick1.png')
						brick.sound1.play()
					elif brick.health == 1:
						brick.object_image = pygame.image.load('./Images/Bricks/hard-brick2.png')
						brick.sound1.play()

		#examine if ball has hit player, adjusts velocity accordingly
		if self.object_boundary.y > 570:
			if self.ball_inside_object(paddle.object_boundary) == True and cut_bool == False:
				if paddle.direction == -8 or paddle.direction == -4:
					self.velocity[0] = self.velocity[0] - 1
					self.velocity[1] = -11
					self.sound1.play()
				elif paddle.direction == 8 or paddle.direction == 4:
					self.velocity[0] = self.velocity[0] + 1
					self.velocity[1] = -11
					self.sound1.play()
				elif paddle.direction == 0:
					self.velocity[1] = -11
					self.sound1.play()

		#Clamp ball inside screen
		self.object_boundary.clamp_ip(screen_rect)
		#Move Ball
		self.object_boundary = self.object_boundary.move(self.velocity[0],self.velocity[1])
		#stop ball if velocity and position too low
		self.stop_non_moving_ball()


class Brick:
	def __init__(self,X,Y,image_file,health):
		self.object_image = pygame.image.load(image_file)
		self.object_boundary = self.object_image.get_rect (center=(X,Y))
		self.is_brick = True
		# 3=fullhealth, 2=2hitsleft, 1=1hitleft, 0=dead
		self.health = health
		# amount of flashes after it dies
		self.flash_out = 2
		self.sound1 = pygame.mixer.Sound ('./Audio/boing1.ogg')
		self.sound2 = pygame.mixer.Sound ('./Audio/brick_shatter.ogg')
		# Boolean stores if brick is special type
		self.is_special = True
		# type is either 'none, 'ball', 'shroom', 'heart
		self.special_type = 'none'

	def set_as_hard(self):
		self.object_image = pygame.image.load('./Images/Bricks/hard-brick0.png')
		self.health = 3

	def set_as_special_ball(self):
		self.object_image = pygame.image.load('./Images/Bricks/ball-brick.png')
		self.is_special = True
		self.special_type = 'ball'

	def set_as_special_shroom(self):
		self.object_image = pygame.image.load('./Images/Bricks/shroom-brick.png')
		self.is_special = True
		self.special_type = 'shroom'

	def set_as_special_heart(self):
		self.object_image = pygame.image.load('./Images/Bricks/heart-brick.png')
		self.is_special = True
		self.special_type = 'heart'

	def return_special_bool(self):
		if self.is_special == True:
			return True
		if self.is_special == False:
			return False

def gen_pos_neg_one():
	boo = randint(0,1)
	if boo == 0:
		return -1
	elif boo == 1:
		return 1

def safely_modify_colours(current_colours, colours_alt):
	#if first colour limit hit
	if current_colours[0] <= 1 or current_colours[0] >= 254:
		colours_alt = -(colours_alt[0]), colours_alt[1], colours_alt[2]
	if current_colours[1] <= 1 or current_colours[1] >= 254:
		colours_alt = colours_alt[0], -(colours_alt[1]), colours_alt[2]
	if current_colours[2] <= 1 or current_colours[2] >= 254:
		colours_alt = colours_alt[0], colours_alt[1], -(colours_alt[2])
	current_colours = (current_colours[0] + colours_alt[0]), (current_colours[1] + colours_alt[1]), (current_colours[2] + colours_alt[2])
	return current_colours, colours_alt


def build_hearts():
	for z in range(paddle.health):
		x_location = 70+(z*20)
		hearts_array.append(Heart_Symbol(x_location))

def increment_flash_and_trip_count(flash_count, trip_count, current_colours, colours_alt, trip_boolean):
	#increment flash count, sets flash pace
	if flash_count == 10:
		#if tripping increment trip count
		if trip_boolean == True:
			trip_count = trip_count + 1
		flash_count = 0
	elif flash_count < 10:
		flash_count = flash_count + 1

	if trip_boolean == True:
		if trip_count % 50 == 0:
			for ball in ball_array:
				ball.colour_integer = ball.colour_integer + 1
				if ball.colour_integer == 8:
					ball.colour_integer = 0
				ball.object_image = pygame.image.load(ball.image_array[ball.colour_integer])

		if trip_count == 101:
			trip_count = 0
			colours_alt = gen_pos_neg_one(), gen_pos_neg_one(), gen_pos_neg_one()
		elif trip_count < 101:
			trip_count = trip_count + 1
			current_colours, colours_alt = safely_modify_colours(current_colours, colours_alt)
			current_colours, colours_alt = safely_modify_colours(current_colours, colours_alt)
	return flash_count, trip_count, current_colours, colours_alt, trip_boolean

def process_user_input(trip_boolean,colours_alt,trip_time_out):
	pass_bool = False
	#First check if a button has been pressed
	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and trip_boolean == False:
				paddle.direction = -8
			elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and trip_boolean == False:
				paddle.direction = 8
			elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and trip_boolean == True:
				paddle.direction = -4
			elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and trip_boolean == True:
				paddle.direction = 4
			elif event.key == pygame.K_w:
				trip_boolean = True
				colours_alt = gen_pos_neg_one(), gen_pos_neg_one(), gen_pos_neg_one()
				pygame.mixer.music.load('./Audio/trip.ogg')
				pygame.mixer.music.play()
				trip_time_out = 350
			elif event.key == pygame.K_s:
				pass_bool = True
		else:
			paddle.direction = 0
	return trip_boolean, colours_alt, trip_time_out, pass_bool

#Builds level 1!
def build_lvl_1():
	object_image_array = ['./Images/Bricks/red-brick.png','./Images/Bricks/orange-brick.png','./Images/Bricks/yellow-brick.png','./Images/Bricks/green-brick.png','./Images/Bricks/blue-brick.png','./Images/Bricks/darkblue-brick.png','./Images/Bricks/purple-brick.png','./Images/Bricks/magenta-brick.png','./Images/Bricks/hard-brick0.png','./Images/Bricks/hard-brick1.png','./Images/Bricks/hard-brick2.png']
	brick_rows = [45,75,105,135,165,195]

	for brick_row in brick_rows:
		brick_col = 90
		for z in range(8):
			bricks_array.append(Brick(brick_col,brick_row,object_image_array[z],1))
			brick_col = brick_col + 60

	for z in range(8):
		bricks_array[(z)].set_as_special_ball()
	for z in range(8):
		bricks_array[(8 + z)].set_as_hard()

	spec1 = randint(24,31)

	bricks_array[spec1].set_as_special_shroom()


#Builds level 2!
def build_lvl_2():
	object_image_array = ['./Images/Bricks/red-brick.png','./Images/Bricks/orange-brick.png','./Images/Bricks/yellow-brick.png','./Images/Bricks/green-brick.png','./Images/Bricks/blue-brick.png','./Images/Bricks/darkblue-brick.png','./Images/Bricks/purple-brick.png','./Images/Bricks/magenta-brick.png','./Images/Bricks/hard-brick0.png','./Images/Bricks/hard-brick1.png','./Images/Bricks/hard-brick2.png']
	brick_rows = [75,105,135,165]

	for brick_row in brick_rows:
		brick_col = 90
		for z in range(8):
			bricks_array.append(Brick(brick_col,brick_row,object_image_array[z],1))
			brick_col = brick_col + 60

	for z in range(8):
		bricks_array[(z)].set_as_hard()

	spec1 = randint(8,23)
	spec2 = spec1
	while spec1 == spec2:
		spec2 = randint(8,23)

	bricks_array[spec1].set_as_special_ball()
	bricks_array[spec2].set_as_special_shroom()

#Builds level 3!
def build_lvl_3():
	object_image_array = ['./Images/Bricks/red-brick.png','./Images/Bricks/orange-brick.png','./Images/Bricks/yellow-brick.png','./Images/Bricks/green-brick.png','./Images/Bricks/blue-brick.png','./Images/Bricks/darkblue-brick.png','./Images/Bricks/purple-brick.png','./Images/Bricks/magenta-brick.png','./Images/Bricks/hard-brick0.png','./Images/Bricks/hard-brick1.png','./Images/Bricks/hard-brick2.png']
	brick_rows = [45,75,105,135,165]

	for brick_row in brick_rows:
		brick_col = 90
		for z in range(8):
			bricks_array.append(Brick(brick_col,brick_row,object_image_array[z],1))
			brick_col = brick_col + 60

	for z in range(8):
		bricks_array[(z)].set_as_hard()

	for z in range(8):
		bricks_array[(32 + z)].set_as_hard()

	spec1 = randint(8,31)
	spec2 = spec1
	while spec1 == spec2:
		spec2 = randint(8,31)
		spec3 = spec2
	while spec3 == spec2 or spec3 == spec1:
		spec3 = randint(8,31)

	bricks_array[spec1].set_as_special_ball()
	bricks_array[spec2].set_as_special_shroom()
	bricks_array[spec3].set_as_special_heart()

#Builds level 4!
def build_lvl_4():
	object_image_array = ['./Images/Bricks/red-brick.png','./Images/Bricks/orange-brick.png','./Images/Bricks/yellow-brick.png','./Images/Bricks/green-brick.png','./Images/Bricks/blue-brick.png','./Images/Bricks/darkblue-brick.png','./Images/Bricks/purple-brick.png','./Images/Bricks/magenta-brick.png','./Images/Bricks/hard-brick0.png','./Images/Bricks/hard-brick1.png','./Images/Bricks/hard-brick2.png']
	brick_rows = [45,75,105,135,165]

	for brick_row in brick_rows:
		brick_col = 90
		for z in range(8):
			bricks_array.append(Brick(brick_col,brick_row,object_image_array[z],1))
			brick_col = brick_col + 60

	for z in range(8):
		bricks_array[(z)].set_as_hard()

	for z in range(8):
		bricks_array[(32 + z)].set_as_hard()

	bricks_array[(8)].set_as_hard()
	bricks_array[(15)].set_as_hard()
	bricks_array[(16)].set_as_hard()
	bricks_array[(23)].set_as_hard()
	bricks_array[(24)].set_as_hard()
	bricks_array[(31)].set_as_hard()

	spec1 = randint(9,14)
	spec2 = randint(17,22)
	spec3 = randint(25,30)

	bricks_array[spec1].set_as_special_ball()
	bricks_array[spec2].set_as_special_shroom()
	bricks_array[spec3].set_as_special_ball()

#Builds level 5!
def build_lvl_5():
	object_image_array = ['./Images/Bricks/red-brick.png','./Images/Bricks/orange-brick.png','./Images/Bricks/yellow-brick.png','./Images/Bricks/green-brick.png','./Images/Bricks/blue-brick.png','./Images/Bricks/darkblue-brick.png','./Images/Bricks/purple-brick.png','./Images/Bricks/magenta-brick.png','./Images/Bricks/hard-brick0.png','./Images/Bricks/hard-brick1.png','./Images/Bricks/hard-brick2.png']
	brick_rows = [45,75,105,135,165]
	hard_bricks = [0,3,4,7,11,19,20,27,32,35,36,39]
	soft_bricks = []

	for brick_row in brick_rows:
		brick_col = 90
		for z in range(8):
			bricks_array.append(Brick(brick_col,brick_row,object_image_array[z],1))
			brick_col = brick_col + 60

	for num in hard_bricks:
		bricks_array[(num)].set_as_hard()

	for y in range(40):
		soft_bricks.append(y)
	for num in hard_bricks:
		soft_bricks.remove(num)
	soft_bricks.remove(12)
	soft_bricks.remove(28)

	spec1 = random.choice(soft_bricks)
	spec2 = spec1
	while spec1 == spec2:
		spec2 = random.choice(soft_bricks)
		spec3 = spec2
	while spec3 == spec2 or spec3 == spec1:
		spec3 = random.choice(soft_bricks)

	bricks_array[spec1].set_as_special_ball()
	bricks_array[spec2].set_as_special_shroom()
	bricks_array[spec3].set_as_special_ball()

def build_level(level_int):
	if level_int == 1:
		build_lvl_1()
	elif level_int == 2:
		build_lvl_2()
	elif level_int == 3:
		build_lvl_3()
	elif level_int == 4:
		build_lvl_4()
	elif level_int == 5:
		build_lvl_5()

def play_game_music(level_int, cut_bool):
	if cut_bool == False:
		if level_int == 1:
			pygame.mixer.music.load('./Audio/badtouch.ogg')
			pygame.mixer.music.play()
		elif level_int == 2:
			pygame.mixer.music.load('./Audio/cena.ogg')
			pygame.mixer.music.play()
		elif level_int == 3:
			pygame.mixer.music.load('./Audio/fuckthepolice.ogg')
			pygame.mixer.music.play()
		elif level_int == 4:
			pygame.mixer.music.load('./Audio/strunk.ogg')
			pygame.mixer.music.play()
		elif level_int == 5:
			pygame.mixer.music.load('./Audio/kungfujesus.ogg')
			pygame.mixer.music.play()
	elif cut_bool == True:
		if level_int == 1:
			pygame.mixer.music.load('./Audio/cut_screen1.ogg')
			pygame.mixer.music.play()
		elif level_int == 2:
			pygame.mixer.music.load('./Audio/cut_screen2.ogg')
			pygame.mixer.music.play()
		elif level_int == 3:
			pygame.mixer.music.load('./Audio/cut_screen3.ogg')
			pygame.mixer.music.play()
		elif level_int == 4:
			pygame.mixer.music.load('./Audio/cut_screen4.ogg')
			pygame.mixer.music.play()


def main_game_loop(level_int, bg0, bg1):
	flash_count = 1
	trip_count = 0
	trip_time_out = 0
	trip_boolean = False
	finished_time_out = 0
	finished_bool = False
	won = False
	cut_bool = False

	colours_alt = 0, 0, 0
	current_colours = randint(0,255), randint(0,255), randint(0,255) 

	if len(ball_array) > 1:
		ball_array.pop()

	ball_array[0].object_boundary.x = 50
	ball_array[0].object_boundary.y = 300
	ball_array[0].velocity[0] = 1
	ball_array[0].velocity[1] = 1

	while len(bricks_array) > 0:
		bricks_array.pop()

	paddle.object_boundary.x = 100

	build_level(level_int)

	play_game_music(level_int, cut_bool)

	in_game = True
	while in_game == True:
		#increments counts, changes ball image if needed!
		flash_count, trip_count, current_colours, colours_alt, trip_boolean = increment_flash_and_trip_count(flash_count, trip_count, current_colours, colours_alt, trip_boolean)

		#examine if player is not out of lifes
		if paddle.health <= 0:
			in_game = False
	
		for ball in ball_array:
			ball.process_ball(cut_bool)

		for dropping in dropping_array:
			trip_time_out,trip_boolean,colours_alt = dropping.process_dropping(trip_time_out,trip_boolean,colours_alt)

		#decrement flash out value for flashing items, remove them if they have 'flashed out'
		for flashing in flashing_array:
			if flashing.flash_out > 0 and flash_count == 9:
				flashing.flash_out = flashing.flash_out - 1
			elif flashing.flash_out == 0 and flash_count ==	 9:
				flashing_array.remove(flashing)

		#clamp player to screen then move player
		paddle.object_boundary.clamp_ip(screen_rect)
		paddle.object_boundary = paddle.object_boundary.move(paddle.direction,0)

		trip_boolean, colours_alt, trip_time_out, pass_bool = process_user_input(trip_boolean, colours_alt, trip_time_out)

		if (len(bricks_array) == 0 or pass_bool == True) and finished_bool == False:
			won = True
			finished_time_out = 150
			finished_bool = True
		if finished_bool == True:
			finished_time_out = finished_time_out - 1
		if finished_bool == True and finished_time_out < 0:
			in_game = False		

		#New screen colour is drawn
		screen.fill(current_colours)
		#Blayer is added to new frame
		if trip_boolean == False:
			screen.blit(bg0, (0,0))

		screen.blit(bg1, (0,0))

		#display all  bricks
		for brick in bricks_array:
			screen.blit(brick.object_image, brick.object_boundary)

		#display flashing bricks
		for flashing in flashing_array:
			if flash_count > 4:
				screen.blit(flashing.object_image, flashing.object_boundary)

		#display ball and player
		for ball in ball_array:	
			screen.blit(ball.object_image, ball.object_boundary)

		screen.blit(paddle.object_image, paddle.object_boundary)

		#shows hearts!
		for heart in hearts_array:
			screen.blit(heart.object_image, heart.object_boundary)

		for dropping in dropping_array:
			screen.blit(dropping.object_image, dropping.object_boundary)

		#New frame is applied
		pygame.display.flip()
		#Timer
		if trip_boolean == False:
			time.sleep(0.005)
		elif trip_boolean == True:
			trip_time_out = trip_time_out - 1
			time.sleep(0.02)
			if trip_time_out <= 0:
				trip_boolean = False
				pygame.mixer.music.load('./Audio/badtouch2.ogg')
				pygame.mixer.music.play()
	return won

def general_cutscreen_loop(level_int,cut_screen_image1,cut_screen_image2):

	while len(bricks_array) > 0:
		bricks_array.pop()

	passthrough = False
	cut_bg1 = pygame.image.load(cut_screen_image1)
	cut_bg2 = pygame.image.load(cut_screen_image2)
	cut_bool = True
	play_game_music(level_int, cut_bool)
	
	while passthrough == False:
		screen.fill([0,0,0])
		screen.blit(cut_bg1, (0,0))
		screen.blit(cut_bg2, (0,0))

		for ball in ball_array:
			ball.process_ball(cut_bool)
			screen.blit(ball.object_image, ball.object_boundary)

		pygame.display.flip()

		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					passthrough = True
		time.sleep(0.01)

def intro_screen():
	passthrough = False
	intro_bg1 = pygame.image.load("./Images/Intro1.png")
	intro_bg2 = pygame.image.load("./Images/Intro2.png")
	pygame.mixer.music.load('./Audio/intro.ogg')
	pygame.mixer.music.play()
	while passthrough == False:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					passthrough = True
		screen.fill([0,0,0])
		screen.blit(intro_bg1, (0,0))
		pygame.display.flip()
		time.sleep(0.5)
		screen.fill([0,0,0])
		screen.blit(intro_bg2, (0,0))
		pygame.display.flip()
		time.sleep(0.5)	

pygame.init()

#Global Variables - permanent static variables or singular 'only ever used at 1 time' variables

size = width, height = 600, 640
ball_array = []
bricks_array = []
hearts_array = []
flashing_array = []
dropping_array = []

#After defining screen, speed and colour values, create the screen
screen = pygame.display.set_mode(size)
screen_rect = screen.get_rect()

#Create player object
paddle = Player(100)
#Create herb object
ball_array.append(Ball(50,300,[1,1],7))
#Create hearts!
build_hearts()

pygame.display.set_caption("GnuBreaker --Alpha 0.4.6--")

level_int = 1
bg0 = pygame.image.load('./Images/background1_0.png')
bg1 = pygame.image.load('./Images/background1_1.png')

intro_screen()
won = main_game_loop(level_int, bg0, bg1)

if won == True:
	cut_screen_image1 = "./Images/cutscreen1_0.png"
	cut_screen_image2 = "./Images/cutscreen1_1.png"
	general_cutscreen_loop(level_int,cut_screen_image1,cut_screen_image2)
	level_int = 2
	bg0 = pygame.image.load('./Images/background2_0.png')
	bg1 = pygame.image.load('./Images/background2_1.png')
	won = main_game_loop(level_int, bg0, bg1)
	if won == True:
		cut_screen_image1 = "./Images/cutscreen2_0.png"
		cut_screen_image2 = "./Images/cutscreen2_1.png"
		general_cutscreen_loop(level_int,cut_screen_image1,cut_screen_image2)
		level_int = 3
		bg0 = pygame.image.load('./Images/background3_0.png')
		bg1 = pygame.image.load('./Images/background3_1.png')
		won = main_game_loop(level_int, bg0, bg1)
		if won == True:
			cut_screen_image1 = "./Images/cutscreen3_0.png"
			cut_screen_image2 = "./Images/cutscreen3_1.png"
			general_cutscreen_loop(level_int,cut_screen_image1,cut_screen_image2)
			level_int = 4
			bg0 = pygame.image.load('./Images/background4_0.png')
			bg1 = pygame.image.load('./Images/background4_1.png')
			won = main_game_loop(level_int, bg0, bg1)
			if won == True:
				cut_screen_image1 = "./Images/cutscreen4_0.png"
				cut_screen_image2 = "./Images/cutscreen4_1.png"
				general_cutscreen_loop(level_int,cut_screen_image1,cut_screen_image2)
				level_int = 5
				bg0 = pygame.image.load('./Images/background5_0.png')
				bg1 = pygame.image.load('./Images/background5_1.png')
				won = main_game_loop(level_int, bg0, bg1)

'''
intro_screen()
won = level_1()
bricks_list = []
if won == True:
	cut_screen1()
	won = level_2()
	bricks_list = []
	if won == True:
		cut_screen2()
		won = level_3()
		if won == True:
			winner_screen()
'''


