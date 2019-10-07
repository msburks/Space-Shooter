import sys, logging, os, random, math, open_color, arcade

#check to make sure we are running the right version of Python
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

#turn on logging, in case we have to leave ourselves debugging messages
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 750
SCREEN_TITLE = "Endless Void"
GAME_RUNNING = 1
GAME_OVER = 2



NUM_ENEMIES = 9
STARTING_LOCATION = (400,100)
BULLET_DAMAGE = 10
HIT_DAMAGE = 1
PLAYER_HP = 1
ENEMY_HP = 100
HIT_SCORE = 10
KILL_SCORE = 100
MOVEMENT_SPEED = 10

class Bullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        ''' 
        initializes the bullet
        Parameters: position: (x,y) tuple
            velocity: (dx, dy) tuple
            damage: int (or float)
        '''
        super().__init__("assets/bullet.png", 0.1)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage

    def update(self):
        '''
        Moves the bullet
        '''
        self.center_x += self.dx*2 
        self.center_y += self.dy*2 

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/spaceshipN0.png", 0.1)
        self.hp = PLAYER_HP
        (self.center_x, self.center_y) = STARTING_LOCATION

    def __call__(self):
        return self

        

class Enemy(arcade.Sprite):
    def __init__(self, position):
        '''
        initializes a ship enemy
        Parameter: position: (x,y) tuple
        '''
        super().__init__("assets/EnemySpaceship.png", 0.08)
        self.hp = ENEMY_HP
        (self.center_x, self.center_y) = position
        

class Window(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
       
        self.current_state = GAME_RUNNING
        self.set_mouse_visible(True)
        arcade.set_background_color(open_color.gray_9)
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.player = Player()
        self.player_list.append(self.player)
        self.score = 0
        self.time = 0
        self.total_time = 0.0
        

        


    def setup(self):
        for i in range(NUM_ENEMIES):
            x = 120 * (i+1) + 40
            y = 600
            enemy = Enemy((x,y))
            self.enemy_list.append(enemy)    
        self.total_time = 0.0
        
        

    def update(self, delta_time):
        if self.current_state == GAME_RUNNING:
            self.player_list.update()
            self.bullet_list.update()
            damage1 = arcade.check_for_collision_with_list(self.player, self.enemy_list)
            if len(damage1):
                for p in self.player_list:
                    p.kill()
            for e in self.enemy_list:
                damage = arcade.check_for_collision_with_list(e, self.bullet_list)
                for d in damage:
                    e.hp -= d.damage
                    d.kill()
                    if e.hp <= 0:
                        self.score += KILL_SCORE
                        e.kill()
                    else:
                        self.score += HIT_SCORE
            if (len(self.enemy_list) == 0):
                output = "Game Over: You Win!"
                arcade.draw_text(output, 225, 225, open_color.green_9, 75)
                final_time = self.total_time
                time_taken_formatted = f"{round(final_time, 0)} seconds"
                arcade.draw_text(f"Time taken: {time_taken_formatted}", 400, 150, open_color.green_9, 50)
            if (len(self.player_list) == 0):
                output = "Game Over: You Lose\n             Try Again!"
                final_time = self.total_time
                arcade.draw_text(output, 200, 225, open_color.green_9, 75)
                time_taken_formatted = f"{round(final_time, 0)} seconds"
                arcade.draw_text(f"Time taken: {time_taken_formatted}", 400, 150, open_color.green_9, 50)
            
                

                
        self.total_time += delta_time
        

    def on_draw(self): 
        """ Called whenever we need to draw the window. """
        arcade.start_render()
        arcade.draw_text(str(self.score), 20, SCREEN_HEIGHT - 40, open_color.green_9, 20)
        self.player_list.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()
        # Below is the timer ------
        # Calculate minutes
        minutes = int(self.total_time) // 60
        # Calculate seconds by using a modulus (remainder)
        seconds = int(self.total_time) % 60
        # Figure out our output
        output = f"Time: {minutes:02d}:{seconds:02d}"
        # Output the timer text.
        arcade.draw_text(output, 1160, 700, open_color.green_9, 20)
        if (len(self.enemy_list) == 0):
                output = "Game Over: You Win!"
                arcade.draw_text(output, 225, 225, open_color.green_9, 75)
                final_time = self.total_time
                time_taken_formatted = f"{round(final_time, 0)} seconds"
                arcade.draw_text(f"Time taken: {time_taken_formatted}", 350, 150, open_color.green_9, 50) 
                output_total = f"Total Score: {self.score}"
                arcade.draw_text(output_total, 350, 75, open_color.green_9, 50)
        if (len(self.player_list) == 0):
                output = "Game Over: You Lose\n             Try Again!"
                arcade.draw_text(output, 200, 225, open_color.green_9, 75)
                final_time = self.total_time
                time_taken_formatted = f"{round(final_time, 0)} seconds"
                arcade.draw_text(f"Time taken: {time_taken_formatted}", 350, 150, open_color.green_9, 50) 
                output_total = f"Total Score: {self.score}"
                arcade.draw_text(output_total, 350, 75, open_color.green_9, 50)
    def draw_game_over(self): 
        """
        Draw "Game over" across the screen.
        """
        output = "Game Over"
        arcade.draw_text(output, 650, 375, open_color.white, 50)
        time_taken_formatted = f"{round(self.total.time, 1)} seconds"
        arcade.draw_text(f"Time taken: {time_taken_formatted}", 650, 300, open_color.white, 50)
                         

        output_total = f"Total Score: {self.score}"
        arcade.draw_text(output_total, 10, 10, arcade.color.WHITE, 14)
        
    def draw_game(self):
        arcade.start_render()

        if self.current_state == GAME_RUNNING:
            self.on_draw()
        else:
            self.draw_game_over()

    def on_mouse_motion(self, x, y, dx, dy):
        """ Called to update our objects. Happens approximately 60 times per second."""
        """self.player.center_x = x
        self.player.center_y = y"""

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        """if button == arcade.MOUSE_BUTTON_LEFT:
            x = self.player.center_x
            y = self.player.center_y + 20
            bullet = Bullet((x,y),(0,5),BULLET_DAMAGE)
            self.bullet_list.append(bullet)"""
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass

    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        if key == arcade.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED
        elif key == arcade.key.UP:
            self.player.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = -MOVEMENT_SPEED
        if key == arcade.key.SPACE:
            x = self.player.center_x
            y = self.player.center_y + 40
            bullet = Bullet((x,y),(0,5),BULLET_DAMAGE)
            self.bullet_list.append(bullet)

    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0
        elif key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0

        pass
    


def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()