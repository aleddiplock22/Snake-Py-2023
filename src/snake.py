"""
Contains classes for tracking the snake
"""

import numpy as np
import copy
import keyboard
import time
import random


class Vector2D():
    def __init__(self, x, y):
        """
        np grid works like 
        (y,x)    (y, x+1)    (y, x+2)
        (y+1, x) (y+1, x+1)  (y+1, x+2)
        (y+2, x) .......
        """
        self.x = x
        self.y = y

    def __add__(self, v2):
        return Vector2D(self.x + v2.x, self.y + v2.y)
    
    def __sub__(self, v2):
        return Vector2D(self.x - v2.x, self.y - v2.y)

    def __iadd__(self, v2):
        self.x += v2.x
        self.y += v2.y
        return self
    
    def __isub__(self, v2):
        self.x -= v2.x
        self.y -= v2.y
        return self
    
    def __str__(self):
        return f'({self.x},{self.y})'
    
    def __eq__(self, v2):
        return (self.x==v2.x and self.y==v2.y)

class Snake():
    """
    Just for keeping track of the snake
    """
    UP = Vector2D(0,-1)
    DOWN = Vector2D(0,1)
    LEFT = Vector2D(-1,0)
    RIGHT = Vector2D(1,0)

    def __init__(self):
        self.snake_body = [Vector2D(16,16), Vector2D(15,16), Vector2D(14,16)]  # Start in middle facing right
        self.current_dir = Snake.RIGHT   # []-[]-[next]-[next]-[head]-[]-[]
        self.snake_head_pos = self.snake_body[0]  # Start in the middle

    def print_snake(self):
        print('<:', end=' ')
        for block in self.snake_body: print(block, end=' ')
        print('>>>')
    
    def snake_body_as_tuple_list(self):
        lst = []
        for block in self.snake_body:
            lst.append((block.x, block.y))
        return lst

    def get_length(self):
        return len(self.snake_body)
    
    def move(self, dir : Vector2D, adding_block=False):
        """
        moves the snake in chosen direction.
        optional adding_block lets us add a block in while moving
        (this avoided having to know which direction all the individual blocks were going)
        """
        # Dont go backwards
        if self.current_dir == Snake.RIGHT and dir == Snake.LEFT:
            return
        if self.current_dir == Snake.LEFT and dir == Snake.RIGHT:
            return
        if self.current_dir == Snake.UP and dir == Snake.DOWN:
            return
        if self.current_dir == Snake.DOWN and dir == Snake.UP:
            return
        # Set new current direction
        self.current_dir = dir

        # First rest of the blocks to move to where the block in front was 
        for idx in range(self.get_length()).__reversed__():
            if idx != 0:
                if adding_block and idx==self.get_length()-1:
                    # Get value of the end of the snake if we're adding one on.
                    old_end = copy.deepcopy(self.snake_body[-1])
                    tmp = copy.deepcopy(self.snake_body[idx-1])
                    self.snake_body[idx] = tmp
                    self.snake_body.append(old_end)
                else:
                    tmp = copy.deepcopy(self.snake_body[idx-1])
                    self.snake_body[idx] = tmp
        # Then move head
        self.snake_body[0] += dir
    
    def detect_collision(self):
        for i in range(self.get_length()):
            for j in range(self.get_length()):
                if i != j:
                    if self.snake_body[i] == self.snake_body[j]:
                        print("COLLISION WITH SELF, GAME OVER")
                        return True
            
class Berry():
    def __init__(self, snake : Snake):
        self.loc = Vector2D(random.randint(2,30), random.randint(2,30))
        self.consumption_energy = False
        self.consumed = False
        self.can_respawn = False
        self.snake = snake

    def tuple_representation(self):
        loc_tuple = (self.loc.x, self.loc.y)
        return loc_tuple
    
    def check_consumption(self):
        if self.snake.snake_head_pos == self.loc:
            self.consumed = True
            self.consumption_energy = True
            self.can_respawn = True
    
    def respawn(self):
        self.loc = Vector2D(random.randint(2,30), random.randint(2,30))
        self.consumed = False
        self.can_respawn = False
        self.consumption_energy = False
        


class SnakeGame():
    """
    - Keeps track of the grid
    - Takes input for controlling snake
    """

    def __init__(self, snake : Snake, size=(32,32)):
        self.snake = snake
        self.active = True

    def move(self, dir : Vector2D, adding_block=False):
        self.snake.move(dir, adding_block)
        head = self.snake.snake_head_pos
        if head.x == 32 or head.x == 0 or head.y == 32 or head.y == 0:
            print("COLLISION WITH WALL, GAMEOVER")
            self.active = False
        elif self.snake.detect_collision():
            self.active = False
    
    def play(self, speed : float, adding_block=False):
        time.sleep(speed)
        if keyboard.is_pressed('UP'):
            self.move(Snake.UP, adding_block)
        elif keyboard.is_pressed('DOWN'):
            self.move(Snake.DOWN, adding_block)
        elif keyboard.is_pressed('LEFT'):
            self.move(Snake.LEFT, adding_block)
        elif keyboard.is_pressed('RIGHT'):
            self.move(Snake.RIGHT, adding_block)
        elif keyboard.is_pressed('q'):
            self.active = False
        else:
            self.move(self.snake.current_dir, adding_block)
        
        self.snake.print_snake()
            


if __name__ == "__main__":
    s = Snake()
    game = SnakeGame(s)
    game.play()

