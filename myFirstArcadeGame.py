import arcade
from os import path

# window constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
SCREEN_NAME = "My First Arcade Game"

# path to images
RESOURCE_PATH = f"{path.dirname(path.abspath(__file__))}/resources/"

# player constants
PLAYER_MOVEMENT_SPEED = 5
PLAYER_START_X = 64
PLAYER_START_Y = 128
PLAYER_SCALE = 1

# wall constants
WALL_SCALE = 1

class MyFirstGame(arcade.Window):
    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_NAME)

        self.background = None
        self.resource_path = path
        self.scene = None
        self.player_sprite = None
        self.physics_engine = None

    def start(self):
        self.setup() # create window
        self.get_players() # create players
        self.get_walls() # create walls

        # arcade.start_render() # start drawing
        # self.scene.draw() # draw the stuff added to the scene
        # arcade.finish_render() # finish drawing

        # game physics
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.scene.get_sprite_list("Walls")
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

        # Draw our Scene
        self.scene.draw()


    def get_players(self):
        self.player_list = arcade.SpriteList() # add player using built in SpriteList class

        # Set up the player
        self.player_sprite = arcade.Sprite(f"{RESOURCE_PATH}img/sea-turtle.png", PLAYER_SCALE)

        # place player on these coordinates
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y

        self.scene.add_sprite("Player", self.player_sprite)

    def get_walls(self):
        # Create the ground
        # This shows using a loop to place multiple sprites horizontally
        for x in range(0, 1250, 64):
            wall = arcade.Sprite(f"{RESOURCE_PATH}/img/sand-block.png", WALL_SCALE)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)

        # Put some objects on the ground
        # This shows using a coordinate list to place sprites
        coordinate_list = [[512, 96], [256, 96], [768, 96]]

        for coordinate in coordinate_list:
            wall = arcade.Sprite(
                f"{RESOURCE_PATH}/img/seaweed.png", WALL_SCALE
            )
            wall.position = coordinate
            self.scene.add_sprite("Walls", wall)

    def draw_ground(self):
        # Draw the ground in the bottom third
        arcade.draw_lrtb_rectangle_filled(0,
                                        SCREEN_WIDTH,
                                        64,
                                        0,
                                        arcade.color.SAND)
        # self.scene.add_sprite("Ground", ground)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            print("up arrow pressed")
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            print("down arrow pressed")
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            print("up left pressed")
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            print("right arrow pressed")
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP or key == arcade.key.W:
            print("up arrow released")
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            print("down arrow released")
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            print("left arrow released")
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            print("right arrow released")
            self.player_sprite.change_x = 0


    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()


def main():
    game = MyFirstGame()

    game.start()

    arcade.run() # display

if __name__ == "__main__":
    main() 


