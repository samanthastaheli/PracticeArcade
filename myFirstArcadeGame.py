"""
TODOs:
- text display in window
- number changes when turtle collides with enemie/friend
- when turtle collides with crab, point goes down
- when turtle collides with nemo, point goes up
- when turtle collides with crab/nemo, that character disapears
    - each crab/nemo on screen need to have specific name
- display moves
    - crab/nemo/seaweed y value stays same but x value constant change (current)
    - more crab/nemo/seaweed appear
        - randomly or set?
        - don't want objects to close to each other or overlap
"""

import arcade
from os import path
from random import randint

# window constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_NAME = "My First Arcade Game"

# path to images
RESOURCE_PATH = f"{path.dirname(path.abspath(__file__))}/resources/"

# wall constants
WALL_SCALE = 1
WALL_SIZE = 32 # in pixels
BORDER = 5

# player constants
PLAYER_MOVEMENT_SPEED = 5
PLAYER_START_X = 88
PLAYER_START_Y = 280
PLAYER_SCALE = 1

# friends and enimies constants
CHARACTERS_SCALE = 0.75
CHARACTERS_RANGE = (WALL_SIZE*2, SCREEN_HEIGHT) 
CHARACTERS_DOMAIN = (SCREEN_WIDTH-SCREEN_HEIGHT, SCREEN_WIDTH) 

ENEMY_COUNT = 3
FRIEND_COUNT = 3

# text
FONT_SIZE = WALL_SIZE/3

# physics stuff
# set to -2 if want gravity
GRAVITY = 0
CURRENT = -2

# keys
UP_KEY = arcade.key.UP
W_KEY = arcade.key.W
DOWN_KEY = arcade.key.DOWN
S_KEY = arcade.key.S
LEFT_KEY = arcade.key.LEFT
A_KEY = arcade.key.A
RIGHT_KEY = arcade.key.RIGHT
D_KEY = arcade.key.D


class MyFirstGame(arcade.Window):
    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_NAME)

        self.background = None
        self.resource_path = path
        self.scene = None
        self.physics_engine = None
        self.score = 0
        self.score_display = None
        self.text = None
        self.text_color = arcade.color.APPLE_GREEN

        # velocity
        self.vel_y = 0
        self.enemy_move = 2

        # all sprites in game
        self.turtle_sprite = None
        self.nemo_sprite = None
        self.crab_sprite = None

        # keep track of how many characters are on the screen
        self.enemy_count = 0
        self.friend_count = 0

        # characters lists
        self.enemies = None
        self.friends = None

    def start(self):
        self.setup() # create window
        self.get_players() # create players
        self.get_walls() # create walls

        # create ememies and friends characters
        for _ in range(ENEMY_COUNT):
            self.get_enemies()
            self.get_friends()

        # arcade.schedule(self.add_enemies, 1)
        # arcade.schedule(self.add_friends, 1)

        # game physics
        # self.physics_engine = arcade.PhysicsEngineSimple(
        #     self.turtle_sprite, self.scene.get_sprite_list("Walls")
        # )

        self.physics_engine = arcade.PhysicsEnginePlatformer(
			self.turtle_sprite, self.scene.get_sprite_list("Walls"), 0.5
		)

    def setup(self):
        # Initialize Scene
        self.scene = arcade.Scene()

        # arcade.open_window(self.screen_width, self.screen_height, self.screen_name) # open window
        self.background = arcade.set_background_color(arcade.color.BLEU_DE_FRANCE) # background color

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # add score text
        text_x = SCREEN_WIDTH-WALL_SIZE*2
        text_y = SCREEN_HEIGHT-WALL_SIZE*2
        self.text = arcade.draw_text("SCORE", text_x, text_y, self.text_color, FONT_SIZE)
        score_x = text_x + WALL_SIZE-BORDER*3
        score_y = text_y + BORDER*4
        self.score_display = arcade.draw_text(self.score, score_x, score_y, self.text_color, FONT_SIZE*2)

        # draw the scene
        self.scene.draw()

    def on_update(self, delta_time):
        """ Movement and game logic
        Move the player with the physics engine
        Objects (crabs, nemos, seaweed) move left across screen
        """
        # self.crab_sprite.change_x = CURRENT
        # self.nemo_sprite.change_x = CURRENT
        # self.seaweed.change_x = CURRENT 

        # add characters
        # arcade.schedule(self.add_enemies, 2)
        # arcade.schedule(self.add_friends, 3)
        self.turtle_sprite.center_y += self.vel_y * delta_time

        self.physics_engine.update() #simple pyhcics class

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed"""
        if key == UP_KEY:
            # self.turtle_sprite.change_y = -PLAYER_MOVEMENT_SPEED
            self.vel_y = PLAYER_MOVEMENT_SPEED
        elif key == DOWN_KEY:
            # self.turtle_sprite.change_y = -PLAYER_MOVEMENT_SPEED
            self.vel_y = -PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key"""

        if key == UP_KEY:
            # self.turtle_sprite.change_y = PLAYER_MOVEMENT_SPEED
            self.vel_y = PLAYER_MOVEMENT_SPEED
        elif key == DOWN_KEY:
            # self.turtle_sprite.change_y = -PLAYER_MOVEMENT_SPEED
            self.vel_y = -PLAYER_MOVEMENT_SPEED

    def get_players(self):
        self.player_list = arcade.SpriteList() # add player using built in SpriteList class

        # Set up the players
        self.turtle_sprite = arcade.Sprite(f"{RESOURCE_PATH}img/sea-turtle.png", PLAYER_SCALE)

        # place player on these coordinates
        self.turtle_sprite.center_x = PLAYER_START_X
        self.turtle_sprite.center_y = PLAYER_START_Y

        self.scene.add_sprite("Player", self.turtle_sprite)

    def get_walls(self):
        # Create the ground
        # This shows using a loop to place multiple sprites horizontally
        for x in range(0, 1250, 64):
            sand_block = arcade.Sprite(f"{RESOURCE_PATH}/img/sand-block.png", WALL_SCALE)
            blue_block = arcade.Sprite(f"{RESOURCE_PATH}/img/blue_box.png", WALL_SCALE)

            sand_block.center_x = x
            sand_block.center_y = 32
            blue_block.center_x = x
            blue_block.center_y = SCREEN_HEIGHT + (WALL_SIZE / 2) - BORDER

            self.scene.add_sprite("Walls", sand_block)
            self.scene.add_sprite("Walls", blue_block)

        # Put some objects on the ground
        # This shows using a coordinate list to place sprites
        coordinate_list = [[512, 96], [256, 96], [768, 96]]

        for coordinate in coordinate_list:
            wall = arcade.Sprite(
                f"{RESOURCE_PATH}/img/seaweed.png", WALL_SCALE
            )
            wall.position = coordinate
            self.scene.add_sprite("Walls", wall)

    def get_characters(self):
        # add crabs
        crab_coordinates = [[512, 196], [256, 396], [768, 896]]

        for coordinate in crab_coordinates:
            self.crab_sprite = arcade.Sprite(f"{RESOURCE_PATH}img/crab.png", CHARACTERS_SCALE)
  
            self.crab_sprite.position = coordinate
            self.scene.add_sprite("Crab", self.crab_sprite)

        # add nemos
        nemo_coordinates = [[542, 266], [286, 566], [798, 866]]

        for coordinate in nemo_coordinates:
            self.nemo_sprite = arcade.Sprite(f"{RESOURCE_PATH}img/nemo.png", CHARACTERS_SCALE)
  
            self.nemo_sprite.position = coordinate
            self.scene.add_sprite("Nemo", self.nemo_sprite)

    def get_enemies(self):
        # get a a random coordinate
        x = randint(CHARACTERS_DOMAIN[0], CHARACTERS_DOMAIN[1])
        y = randint(CHARACTERS_RANGE[0], CHARACTERS_RANGE[1])
        coordinate = [x, y]

        # add crabs
        self.crab_sprite = arcade.Sprite(f"{RESOURCE_PATH}img/crab.png", CHARACTERS_SCALE)
        self.crab_sprite.position = coordinate
        self.scene.add_sprite("Enemy", self.crab_sprite)
        self.enemy_count += 1

    def get_friends(self):
        # get a a random coordinate
        x = randint(CHARACTERS_DOMAIN[0], CHARACTERS_DOMAIN[1])
        y = randint(CHARACTERS_RANGE[0], CHARACTERS_RANGE[1])
        coordinate = [x, y]

        # add nemo
        self.nemo_sprite = arcade.Sprite(f"{RESOURCE_PATH}img/nemo.png", CHARACTERS_SCALE)
        self.nemo_sprite.position = coordinate
        self.scene.add_sprite("Friend", self.nemo_sprite)
        self.friend_count += 1

    def add_enemies(self, delta_time):
        """ use animation to add new enemies
        to run this function: 
        arcade.schedule(add_enemies, 5)
        """
        arcade.start_render()
        self.get_enemies()

    def add_friends(self, delta_time):
        """ use animation to add new friends
        to run this function: 
        arcade.schedule(add_friends, 5)
        """
        arcade.start_render()
        self.get_friends()

    def check_collision(self):
        # collision detection
        enemy_collide = arcade.check_for_collision_with_list(
			self.turtle_sprite, self.scene.get_sprite_list("Enemy")
		)
        
        friend_collide = arcade.check_for_collision_with_list(
			self.turtle_sprite, self.scene.get_sprite_list("Friend")
		)

        for enemy in enemy_collide:
            # Checking the top of enemy and bottom of player
            x = int(self.player_sprite.center_y - 14)
            y = int(self.enemy.center_y + 25)
            if x == y:
                self.enemy.remove_from_sprite_lists()
            else:
                # Remove the coin
                self.player_sprite.remove_from_sprite_lists()

def main():
    game = MyFirstGame()
    game.start()
    arcade.run() # display

if __name__ == "__main__":
    main() 