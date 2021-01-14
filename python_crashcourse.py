# comments can be declared like this
"""
multiple line comments 
like this
"""

# declare variables like this
x = 5 
y = 10

# print like so
print(x) 
print(y)
print("Hello world!")

""" Variable types """
# types of variables: 
integer = 1
decimal = 1.0 # called a float
boolean = True # true/false values are called booleans
string = "hi!" # strings are a sequence of characters

# python lists 
lst = [1, 2, 3] # this is a list!
print(lst[0])
print(lst[2])
print(len(lst)) # how long the list is

""" If-statements """
z = 5
if(z == 5): # compare with ==
    print("z is 5")
elif(z == 5):
    print("this won't print!")
else: 
    print("z is not equal to 5")

# mathematical operators work in python
if(z + 2 < 10): 
    print("z + 2 is less than 10")

""" Loops """
# notice how i starts at 0
i = 0
while(i < 3):
    print("hi!")
    # set i to be equal to one greater than itself
    i = i + 1 

# range(x) returns a list from [0, x)
for i in range(3):
    # join strings together with the + sign
    # str() turns i (a number) into a string 
    print("Current number: " + str(i)) 
 
print("Loops are over!")

""" Functions """
# returns True if x is greater than y
def is_greater(x, y): 
    return x > y

def multiply(x, y):
    return x * y

# is 5 > 3??
print(is_greater(5, 3)) 

# you can also store the result in a variable
multiplied_num = multiply(4, 6)
print(multiplied_num)