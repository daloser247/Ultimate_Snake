# By Ivan Nesevski and Bilal Majeed on June 2/2013
# These are the classes for the AI for the snake game, this file
# is called from the multiai.py file

#IMPORT THE NEEDED MODULES
import pygame, sys, os, random
from pygame.locals import *

os.environ['SDL_VIDEODRIVER']='windib' #required for winXP

#CONSTANTS
right, left, up, down = 20, -20, 10, -10
scoreColor = 0, 0, 0
block_size = 20
size = width, height = 1000, 740

class Food:
    """ This class is used for making a food item for each snake """

    def __init__(self, screen, snake, snake2, diffFood=False, delay=80):    
        self.delay = delay
        self.snake = snake
        self.snake2 = snake2
        self.diffFood = diffFood
        self.screen = screen
        self.image_reg = pygame.image.load('images/food.bmp').convert()
        self.image_fast = pygame.image.load('images/fastfood.bmp').convert()
        self.image_slow = pygame.image.load('images/slowfood.bmp').convert()
        self.image_points = pygame.image.load('images/pointsfood.bmp').convert()
        self.spawn()
   
    def spawn(self):
        """ generates the food for the snakes to eat """
        
        generate = True

        while generate:
           
            foodType = random.randrange(0, 101)
            if self.diffFood == False:
                if foodType < 20: #makes the fast food
                    self.image = self.image_fast
                elif foodType >= 20 and foodType < 40: #makes the slow food
                    self.image = self.image_slow
                elif foodType >= 40 and foodType < 50:
                    self.image = self.image_points #makes the random points food
                else:    
                    self.image = self.image_reg #makes the normal food
            else:
                self.image = self.image_reg
                
            #randomly assigns a x and y position to the food
            pos_x = random.randrange(0, width, block_size)
            pos_y = random.randrange(40, height, block_size)

            generate = False 

            #checks if the x,y position for food is not the same as
            #a part in the snake's body

            #for snake1
            for part in self.snake.parts:
                if part.position.x == pos_x and part.position.y == pos_y:
                    generate = True
                    break

            #for snake2
            for part in self.snake2.parts:
                if part.position.x == pos_x and part.position.y == pos_y:
                    generate = True
                    break
                     
        self.position = self.image.get_rect().move(pos_x, pos_y)
        self.update() #shows the food on the screen

    def speed_increase(self):
        """ increases the speed of the snake """
        if self.image == self.image_fast:
            if self.delay is not 40:
                self.delay -= 40

    def speed_decrease(self):
        """ decreases the speed of the snake """
        if self.image == self.image_slow:
            if self.delay is not 120:
                self.delay += 40

    def random_points(self):
        """ gives the player/computer 20 to 50 points """
        if self.image == self.image_points:
            amount = random.randrange(20, 51, 10)
        else:
            amount = 10

        return amount

    def update(self):
        """ displays the food to the screen """
        self.screen.blit(self.image, self.position)

class Score:
    """ displays and increases the score """
    def __init__(self, screen, end=False, score=0):
        self.score = score
        self.end = end
        self.screen = screen
        self.font = pygame.font.SysFont('Helvetica', 25)
        self.update(scoreColor)
         
    def increase(self, inc):
        """ inceases the score """
        self.score += inc
        self.update(scoreColor)

    def update(self, color):
        """ displays the score"""
        self.label_scoreText = self.font.render("Score:", True, color)
        self.label_score = self.font.render(str(self.score), True, color)
        if self.end == False:
            self.screen.blit(self.label_scoreText, (20, 10))
            self.screen.blit(self.label_score, (90, 10))
        else:
            self.screen.blit(self.label_scoreText, (width - 120, 10))
            self.screen.blit(self.label_score, (width - 40, 10))        
        
class Part:
    """ this class is responsible adding a part to the snake """
    
    def __init__(self, snakeImage, x=0, y=0, direction=right):
        self.direction = direction
        self.image_head = snakeImage
        self.image = pygame.image.load(self.image_head).convert()
        self.position = self.image.get_rect().move(x, y)
        self.speed = block_size

    def change_direction(self, direction):
        """ changes the direction of the snake """
        if self.direction + direction == 0:
            return

        self.direction = direction

    def move(self):
        """ moves the snake around the screen """

        #IF THE SNAKE MOVES TO EDGE OF THE SCREEN, IT WRAPS AROUND 
        if self.position.x >= width - block_size and self.direction == right:
            self.position.x = 0
            return True
        if self.position.y >= height - block_size and self.direction == down:
            self.position.y = 40
            return True
        if self.position.x <= 0 and self.direction == left:
            self.position.x = width - block_size
            return True
        if self.position.y <= 40 and self.direction == up:
            self.position.y = height - block_size
            return True

        #MOVES THE SNAKE UP, DOWN, LEFT, RIGHT
        if self.direction == up:
            self.position = self.position.move(0, -self.speed)
        elif self.direction == down:
            self.position = self.position.move(0, self.speed)
        elif self.direction == right:
            self.position = self.position.move(self.speed, 0)
        elif self.direction == left:
            self.position = self.position.move(-self.speed, 0)

        return True
    
class Snake:
    """ this class is responsible keeping track of the direction,
        and the different parts of the snake, making the snake bigger
        and displaying the snake to the screen """
    
    def __init__(self, screen, x, y, snakeImage, direction = right):
        self.screen = screen
        self.snakeImage = snakeImage
        self.head = Part(self.snakeImage, x, y)
        self.direction = direction
        self.parts = []
        self.parts.append(self.head)
        self.extend_snake = False

    def change_direction(self, direction):
        """ changes the direction of the snake """
        self.direction = direction

    def move(self, food, food2, score):
        """" extends the snake, changes the direction, moves the snake
            and increases/decreases the speed """
        new_direction = self.direction
        old_direction = None
        new_part = None

        if self.extend_snake:
            last_part = self.parts[-1]
            new_part = Part(self.snakeImage, last_part.position.x, last_part.position.y, last_part.direction)

        for part in self.parts:
            old_direction = part.direction
            part.change_direction(new_direction)

            if not part.move():
                return False

            new_direction = old_direction

        if self.extend_snake:
            self.extend(new_part)

        for each in self.parts[1:]:
            #if the snake eats itself
            if (each.position.x == self.head.position.x and
                each.position.y == self.head.position.y):
                return False

        #if the snakes eats the food  
        if (food.position.x == self.head.position.x and
            food.position.y == self.head.position.y):

            score.increase(food.random_points()) #increases the scoree
            food.speed_increase() #increase/decrease the speed
            food.speed_decrease()
            food.spawn() #spawns a new food
            self.extend_snake = True 

        if (food2.position.x == self.head.position.x and
            food2.position.y == self.head.position.y):

            score.increase(food2.random_points()) #increases the score
            food2.speed_increase() #increase/decrease the speed
            food2.speed_decrease()
            food2.spawn() #spawns a new food
            self.extend_snake = True
        
        return True

    def extend(self, part):
        """ adds a new part to the snake """
        self.parts.append(part)
        self.extend_snake = False

    def update(self):
        """ displays the snake to the screen"""
        for part in self.parts:
            self.screen.blit(part.image, part.position)
