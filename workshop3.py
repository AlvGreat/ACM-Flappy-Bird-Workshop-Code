"""
Workshop 3 Code
"""

import pygame
import neat # documentation: https://neat-python.readthedocs.io/en/latest/config_file.html
import time
import os 
import random 
pygame.font.init() # we have to do this for fonts

# size of the window. Note that all caps in python signals a constant
WIN_WIDTH = 500
WIN_HEIGHT = 800
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# pygame.transform.scale2x() makes an image 2x larger
# pygame.image.load() loads an image
# os.path.join() joins together directories/files automatically (used because it works with cross-platform)

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

STAT_FONT = pygame.font.Font(os.path.join("fonts", "Roboto", "Roboto-Regular.ttf"), 50)

# ----- we'll create a class for each of the main objects:

class Bird: 
    """
    The bird class represents the flappy bird.
    """
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25 # how much bird rotates in flaps
    ROT_VEL = 20 # rotation velocity, how much we rotate/frame 
    ANIMATION_TIME = 5 # how long to show each bird animation

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0 # starts with 0 tilt
        self.tick_count = 0
        self.vel = 0 # velocity starts at 0
        self.height = self.y
        self.img_count = 0 # what image we're currently showing for animations
        self.img = self.IMGS[0] # start with first img

    def jump(self): 
        self.vel = -10.5 # this means that when jumping, move 10.5px up, since (0,0) is top left corner
        self.tick_count = 0
        self.height = self.y

    def move(self): 
        self.tick_count += 1

        # physics equation sigh... calculates displacement
        #  x = v_x * t + a * t^2 (acceleration is constant at 1.5 in this case)
        displacement = self.vel*self.tick_count + 1.5 * self.tick_count**2

        # don't move too fast
        if displacement >= 16:
            displacement = 16

        # if it's already jumping, make it jump higher
        if displacement < 0: 
            displacement -= 2

        # add the displacement to it
        self.y += displacement

        # if we're still moving up, then we want to make sure we don't tilt too much
        if (displacement < 0 or self.y < self.height + 50):
            if self.tilt < self.MAX_ROTATION: 
                self.tilt = self.MAX_ROTATION
        else:
            # we want to tilt it all the way down when falling
            if self.tilt > -90: 
                self.tilt -= self.ROT_VEL 

    def draw(self, win): 
        self.img_count += 1 # track how many times we've shown an img

        # this gives the animation- looks like the bird flaps
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # if it's already looking down, then just make it look down
        if self.tilt <= -80: 
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2 # skips to the correct frame

        # rotates the image according to tilt
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        # this just makes sure that we rotate the image at its center instead of the top left (default)
        new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe: 
    """
    Represents a pipe object.
    """
    GAP = 200 # gap between pipes
    VEL = 5

    def __init__(self, x): 
        self.x = x
        self.height = 0

        # where the top and bottom of the pipe is
        self.top = 0
        self.bottom = 0

        # the PIPE_TOP stores the flipped image of the original pipe
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()
    
    def set_height(self): 
        self.height = random.randrange(50, 450) # generate random height 
        # calculate the heights of where the pipes go
        self.top = self.height - self.PIPE_TOP.get_height() 
        self.bottom = self.height + self.GAP
    
    def move(self): 
        self.x -= self.VEL
    
    def draw(self, win): 
        # .blit to draw the pipe to the screen
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    # this method uses masks in order to have pixel perfect collisions
    # masks are in 2d arrays, and the method checks if actual pixels (not invisible parts of a png image) are overlapping
    def collide(self, bird, win):
        bird_mask = bird.get_mask() 
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        # calculate how far away the corners are away from each other
        top_offset = (self.x - bird.x, self.top - round(bird.y)) # the rounding is just so there's no decimals
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        # this function from pygame returns none if there is no collision
        b_point = bird_mask.overlap(bottom_mask, bottom_offset) 
        t_point = bird_mask.overlap(top_mask,top_offset)

        # if they are colliding, something will be there, so return true for the collision
        if b_point or t_point:
            return True

        return False
 
class Base: 
    """
    Represnts the moving floor of the game.
    """
    VEL = 5 # same as pipe, how fast it moves
    WIDTH = BASE_IMG.get_width() 
    IMG = BASE_IMG

    # what we are doing is essentially drawing two different bases
    # we can keep making the background look like it's moving to the left by keeping track of the two imgs with x1 and x2
    
    # if the blocks look like this, where the screen is in []:    [(----)](----)  
    # then once the first block moves all the way to the left like this:    (----)[(----)]
    # we will move the first block to the end, thus creating a cycle

    def __init__(self, y): 
        self.y = y
        self.x1 = 0 
        self.x2 = self.WIDTH

    def move(self): 
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        # if the first image is off the sceen and < 0, then we want to move that to the very right 
        if (self.x1 + self.WIDTH < 0): 
            self.x1 = self.x2 + self.WIDTH
        
        # same for second image once we start cycling
        if (self.x2 + self.WIDTH < 0): 
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win): 
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

def draw_window(win, bird, pipes, base, score): 
    """
    Draws everything to the window
    """ 
    # blit is a method from pygame to draw something on the screen
    win.blit(BG_IMG, (0,0)) 
    
    for pipe in pipes: 
        pipe.draw(win) # draw pipes
    
    # set the text to be equal to the score
    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    # draw the score- this just checks to make sure that the text is never off the screen 
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10)) 
    
    base.draw(win) # draw base

    bird.draw(win) # draw bird
    pygame.display.update() # refreshes the window

# main loop of game
def main():
    bird = Bird(230, 350) #where it starts
    base = Base(730) # the height is 800, so put the base at 730 since it's 70px tall
    pipes = [Pipe(600)]
    clock = pygame.time.Clock() # create a clock in order to keep track of how many ticks per second we do
    score = 0 # keep track of the user score (+1 every passed pipe)

    run = True
    while run:
        clock.tick(30) # means we do 30 ticks per second at max 
        for event in pygame.event.get(): # just keeps track of user input
            if event.type == pygame.QUIT:
                run = False # quit the game
        
        #bird.move() # move the bird
        
        rem = [] # list of pipes to remove
        add_pipe = False
        for pipe in pipes: 
            if pipe.collide(bird, win): 
                pass
            
            # if the pipe is off of the screen, then we need to add new pipes
            if (pipe.x + pipe.PIPE_TOP.get_width() < 0):
                rem.append(pipe) 
            
            # if we passed the pipe
            if(not pipe.passed and pipe.x < bird.x): 
                pipe.passed = True
                add_pipe = True

            pipe.move()

        # then we have to add a score and a new pipe
        if add_pipe: 
            score += 1
            pipes.append(Pipe(600)) # add new pipe

        #remove everything in the array of pipes to be removed 
        for r in rem: 
            pipes.remove(r)

        # check collision between bird and floor
        if (bird.y + bird.img.get_height() >= 730):
            pass

        base.move() # move the base
        draw_window(win, bird, pipes, base, score)
    
    pygame.quit()
    quit()

main() # call main method






