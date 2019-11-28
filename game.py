import arcade
import os
import random
import sys
import time
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
    name = None

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
    food_exists = False


class MyGame(arcade.Window):

    def __init__(self, width, height, title):

        super().__init__(width, height, title)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.player_list = None
        self.lettuce_list = None
        self.poop_list = None

        self.player_sprite_1 = None
        self.player_sprite_2 = None
        self.food_sprite = None
        self.food_exists = None


        self.score_1 = 0
        self.score_2 = 0

        self.physics_engine_1 = None
        self.physics_engine_2 = None
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):

        self.player_list = arcade.SpriteList()
        self.lettuce_list = arcade.SpriteList()
        self.poop_list = arcade.SpriteList()

        self.score_1 = 0
        self.score_2 = 0

        #player information
        self.player_sprite_1 = Player("images/cow.png", COW_SCALING)
        self.player_sprite_1.name = 'cow'

        self.player_sprite_2 = Player("images/goat.png", GOAT_SCALING)
        self.player_sprite_2.name = 'goat'

        self.physics_engine_1 = arcade.PhysicsEngineSimple(self.player_sprite_1, self.poop_list)
        self.physics_engine_2 = arcade.PhysicsEngineSimple(self.player_sprite_2, self.poop_list)

        self.player_sprite_1.center_x = 0
        self.player_sprite_1.center_y = 0

        self.player_sprite_2.center_x = 800
        self.player_sprite_2.center_y = 700

        self.player_list.append(self.player_sprite_1)
        self.player_list.append(self.player_sprite_2)

        self.food_exists
        self.lock = threading.Lock()
        
        # thread begins
        self.thread = threading.Thread(target=self.food_timer)
        self.thread.start()


    def food_timer(self):
        while True:
            time.sleep(2)
            with self.lock:
                if not self.food_exists:                    
                    self.food_exists = True
            while True:
                time.sleep(2)
                with self.lock:
                    if not self.food_exists:
                        break



    def on_draw(self):

        arcade.start_render()
        self.lettuce_list.draw()
        self.player_list.draw()
        self.poop_list.draw()
      
        score_cow = f"Score Cow: {self.score_1}"
        score_goat = f"Score Goat: {self.score_2}"
        arcade.draw_text(score_cow, 10, 20, arcade.color.WHITE, 14)
        arcade.draw_text(score_goat, 650, 20, arcade.color.WHITE, 14)

        if self.score_1 == 5 or self.score_2 == 5:
            if self.score_1 == 5:
                arcade.draw_text("COW WINS!",280,400,arcade.color.RED, 40)
            else:
                arcade.draw_text("GOAT WINS!",280,400,arcade.color.RED, 40)



    def on_update(self, delta_time):

        self.physics_engine_1.update()
        self.physics_engine_2.update()

        if not self.food_sprite:
            with self.lock:
                if self.food_exists:
                    self.food_sprite = Food("images/lettuce.png", LETTUCE_SCALING)   
                    self.food_sprite.center_x = random.randrange(SCREEN_WIDTH)
                    self.food_sprite.center_y = random.randrange(SCREEN_HEIGHT)
                    self.lettuce_list.append(self.food_sprite)
        #
        if self.food_sprite:    
        
            hit_list = arcade.check_for_collision_with_list(self.food_sprite,self.player_list)
            
            if len(hit_list):
                if len(hit_list)==2:
                    i = random.randint(0, 1)
                    if i==0:
                        self.score_1 += 1
                        self.food_sprite.kill()
                        self.food_sprite = None
                        with self.lock:
                            self.food_exists = False
                    else:
                        self.score_2 += 1
                        self.food_sprite.kill()
                        self.food_sprite = None
                        with self.lock:
                            self.food_exists = False
                else:
                    if hit_list[0].name=='cow':
                        self.score_1 += 1
                        self.food_sprite.kill()
                        self.food_sprite = None
                        with self.lock:
                            self.food_exists = False
                    else:
                        self.score_2 += 1
                        self.food_sprite.kill()
                        self.food_sprite = None
                        with self.lock:
                            self.food_exists = False

        self.player_list.update()
        self.poop_list.update()
        if self.food_sprite:
            self.lettuce_list.update()



    def on_key_press(self, key, modifiers):
        #Player movements

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
        # To stop moviments after release an key
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite_1.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite_1.change_x = 0

        elif key == arcade.key.W or key == arcade.key.S:
            self.player_sprite_2.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.player_sprite_2.change_x = 0


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()