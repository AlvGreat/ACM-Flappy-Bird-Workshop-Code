# declare a class like this
class Apple: 
    # this is the constructor and always has to be called __init__
    def __init__(self): 
        # access properties of a class using the self keyword
        self.seeds = 5 

    # you can have functions inside a class, called methods
    def removeSeed(self, amount):
        self.seeds = self.seeds - amount

# initialize an object/instance of a class  
my_apple = Apple()

# access properties of a class like this
print(my_apple.seeds)

# use a function of a class like this
my_apple.removeSeed(2)
print(my_apple.seeds) # check the two seeds were removed