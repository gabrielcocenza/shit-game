import arcade
import random
import os
import threading

COW_SCALING = 0.2
GOAT_SCALING = 0.07
LETTUCE_SCALING = 0.1
POOP_SCALING = 0.1

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Shit Game"
LETTUCE_COUNT = 15

MOVEMENT_SPEED = 5


class Player(arcade.Sprite):

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1


class Food(arcade.Sprite):
    has_poop = False


class MyGame(arcade.Window):

    def __init__(self, width, height, title):

        super().__init__(width, height, title)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Variables that will hold sprite lists
        self.player_list = None
        self.lettuce_list = None
        self.poop_list = None

        # Set up the player info
        self.player_sprite_1 = None
        self.player_sprite_2 = None
        for number in range(LETTUCE_COUNT):
            lettuce = 'lettuce_sprite_{}'.format(number)
            self.lettuce = None
        self.score_1 = 0
        self.score_2 = 0

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.lettuce_list = arcade.SpriteList()
        self.poop_list = arcade.SpriteList()

        # Score
        self.score_1 = 0
        self.score_2 = 0


        # Set up the player
        self.player_sprite_1 = Player("images/cow.png", COW_SCALING)
        self.player_sprite_2 = Player("images/goat.png", GOAT_SCALING)
        self.player_sprite_1.center_x = 0
        self.player_sprite_1.center_y = 0
        self.player_sprite_2.center_x = 800
        self.player_sprite_2.center_y = 700

        self.player_list.append(self.player_sprite_1)
        self.player_list.append(self.player_sprite_2)


        #Create Food
        for number in range(LETTUCE_COUNT):
            lettuce = 'lettuce_sprite_{}'.format(number)
            self.lettuce = Food("images/lettuce.png", LETTUCE_SCALING)
            self.lettuce.center_x = random.randrange(SCREEN_WIDTH)
            self.lettuce.center_y = random.randrange(SCREEN_HEIGHT)
            self.lettuce_list.append(self.lettuce)


    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()
        self.lettuce_list.draw()
        self.player_list.draw()
        self.poop_list.draw()

        
        score_cow = f"Score Cow: {self.score_1}"
        score_goat = f"Score Goat: {self.score_2}"
        arcade.draw_text(score_cow, 10, 20, arcade.color.WHITE, 14)
        arcade.draw_text(score_goat, 650, 20, arcade.color.WHITE, 14)


    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.player_list.update()
        self.lettuce_list.update()
        self.poop_list.update()

        # Generate a list of all sprites that collided with the player.
        cow_hit_list = arcade.check_for_collision_with_list(self.player_sprite_1, self.lettuce_list)
        goat_hit_list = arcade.check_for_collision_with_list(self.player_sprite_2, self.lettuce_list)
        # poop_hit_list = arcade.check_for_collision_with_list(self.lettuce_list, self.poop_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for lettuce in cow_hit_list:
            lettuce.remove_from_sprite_lists()
            self.score_1 += 1

        for lettuce in goat_hit_list:
            lettuce.remove_from_sprite_lists()
            self.score_2 += 1




    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.player_sprite_1.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite_1.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite_1.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite_1.change_x = MOVEMENT_SPEED
        elif key == arcade.key.SPACE:
             poop = arcade.Sprite("images/poop.png", POOP_SCALING)
             poop.center_x = self.player_sprite_1.center_x
             poop.center_y = self.player_sprite_1.center_y
             self.poop_list.append(poop)


        elif key == arcade.key.W:
            self.player_sprite_2.change_y = MOVEMENT_SPEED
        elif key == arcade.key.S:
            self.player_sprite_2.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.A:
            self.player_sprite_2.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player_sprite_2.change_x = MOVEMENT_SPEED
        elif key == arcade.key.E:
             poop = arcade.Sprite("images/poop.png", POOP_SCALING)
             poop.center_x = self.player_sprite_2.center_x
             poop.center_y = self.player_sprite_2.center_y
             self.poop_list.append(poop)


    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite_1.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite_1.change_x = 0

        elif key == arcade.key.W or key == arcade.key.S:
            self.player_sprite_2.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.player_sprite_2.change_x = 0


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()