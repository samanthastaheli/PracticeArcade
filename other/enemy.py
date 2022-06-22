# Importing arcade module
import arcade

# Creating MainGame class
class MainGame(arcade.Window):
	def __init__(self):
		super().__init__(600, 600,
						title="Player Movement")

		# Initializing a variable to store
		# the velocity of the player
		self.vel_x = 0

		# Creating variable for Camera
		self.camera = None

		# Creating variable to store current score
		self.score = 0

		# Creating variable to move the enemy
		self.enemy_move = 2

		# Creating variable for enemy sprite
		self.enemy = None

		# Creating scene object
		self.scene = None

		# Creating variable to store player sprite
		self.player = None

		# Creating variable for our game engine
		self.physics_engine = None

	# Creating on_draw() function to draw on the screen
	def on_draw(self):
		arcade.start_render()

		# Drawing the text
		arcade.draw_text('Score :- '+str(self.score),
						self.player_sprite.center_x - 500 / 2,
						self.player_sprite.center_y + 200,
						arcade.color.WHITE, 30, 5000, 'left')

		# Using the camera
		self.camera.use()
		
		# Drawing our scene
		self.scene.draw()

	def setup(self):
		
		# Initialize Scene object
		self.scene = arcade.Scene()
		
		# Using Camera() function
		self.camera = arcade.Camera(600, 600)

		# Loading enemy sprite
		self.enemy = arcade.Sprite("Enemy.png", 1)

		# Initializing the starting coordinates
		self.enemy.center_x = 500
		self.enemy.center_y = 110

		# Adding the enemy sprite in the scene
		self.scene.add_sprite("Enemy", self.enemy)

		# Creating different sprite lists
		self.scene.add_sprite_list("Player")
		self.scene.add_sprite_list("Platforms",
								use_spatial_hash=True)

		# Adding player sprite
		self.player_sprite = arcade.Sprite("Player.png", 1)

		# Adding coordinates for the center of the sprite
		self.player_sprite.center_x = 64
		self.player_sprite.center_y = 90

		# Adding Sprite in our scene
		self.scene.add_sprite("Player", self.player_sprite)

		# Adding platform sprite according to level
		platform = arcade.Sprite(f"Platform.png", 1)
		
		# Adding coordinates for the center of the platform
		platform.center_x = 300
		platform.center_y = 32
		self.scene.add_sprite("Platforms", platform)

		# Creating Physics engine
		self.physics_engine = arcade.PhysicsEnginePlatformer(
			self.player_sprite, self.scene.get_sprite_list("Platforms"), 0.5
		)

	# Creating on_update function to
	# update the x coordinate

	def on_update(self, delta_time):

		# Moving the position of enemy
		self.enemy.center_x += self.enemy_move

		# Changing the direction of enemy movement
		if self.enemy.center_x > 500 or self.enemy.center_x < 160:
			self.enemy_move *= -1

		# Checking if the enemy is colliding with player or not
		enemy_collide = arcade.check_for_collision_with_list(
			self.player_sprite, self.scene.get_sprite_list("Enemy")
		)

		# Looping through each enemy and removing the player if colliding
		for enemy in enemy_collide:

			# Checking the top of enemy and bottom of player
			x = int(self.player_sprite.center_y - 14)
			y = int(self.enemy.center_y + 25)
			if x == y:
				self.enemy.remove_from_sprite_lists()
			else:
				# Remove the coin
				self.player_sprite.remove_from_sprite_lists()

		# Changing x coordinate of player
		self.player_sprite.center_x += self.vel_x * delta_time
		
		# Updating the physics engine to move the player
		self.physics_engine.update()

		# Calling the camera_move function
		self.camera_move()

	# Creating function to change the velocity
	# when button is pressed
	def on_key_press(self, symbol, modifier):

		# Checking the button pressed
		# and changing the value of velocity
		if symbol == arcade.key.LEFT:
			self.vel_x = -300
		elif symbol == arcade.key.RIGHT:
			self.vel_x = 300
		elif symbol == arcade.key.UP:
			if self.physics_engine.can_jump():
				self.player_sprite.change_y = 15

	# Creating function to change the velocity
	# when button is released
	def on_key_release(self, symbol, modifier):

		# Checking the button released
		# and changing the value of velocity
		if symbol == arcade.key.LEFT:
			self.vel_x = 0
		elif symbol == arcade.key.RIGHT:
			self.vel_x = 0

	def camera_move(self):

		# Getting the x coordinate for the center of camera
		screen_x = self.player_sprite.center_x - \
			(self.camera.viewport_width / 2)

		# Getting the y coordinate for the center of camera
		screen_y = self.player_sprite.center_y - \
			(self.camera.viewport_height / 2)

		# Moving the camera
		self.camera.move_to([screen_x, screen_y])


# Calling MainGame class
game = MainGame()
game.setup()
arcade.run()