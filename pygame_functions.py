import pygame

# create a window
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# create a font
STAT_FONT = pygame.font.Font(os.path.join("fonts", "Roboto", "Roboto-Regular.ttf"), 50)

# render(text, boolean for if antialiasing is true/false, font color)
# antialiasing true (1) means that the text will have smoother edges
STAT_FONT.render("hi!", 1, (255, 255, 255))

# create background image
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

# draws background image to pair of coordinates 
win.blit(BG_IMG, (0, 0))

# updates the display to make sure everything is drawn
pygame.display.update()


# create a pygame clock; we can use it to keep track of fps
clock = pygame.time.Clock() 

# 30 ticks means that 30 ticks/loops/frames per second
# this way, our code won't run as fast as possible and only draw to the screen 30 times a second
clock.tick(30) 

# pygame.event.get() returns a list of events for what's happening to the pygame window
for event in pygame.event.get(): # just keeps track of user input
    # the event object has a type variable inside it
    # if it's equal to a value, pygame.QUIT, then we exit the program 
    if event.type == pygame.QUIT:
        quit()

