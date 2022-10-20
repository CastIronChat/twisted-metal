# Wrote this after one of our first sessions.

print("Ex: If/Elif/Try/except")

print(" ")

print("Guess a number between 1 and 10. Hurry up Red.")
print(" ")
x = input("What's your guess? ")
print(" ")

z = 56

#gonna try this try except thing here incase someone enters not a number

try :
    y = int(x)
except :
    print("Error 404")
    
try :
    if y == z :
        print("56? Fifty-six?? Aww man! Now that's all I can think about!!")
    elif y <= 0 :
        print("That's not even a positive number.")
    elif y <= 10 :
        print("Close.")
    elif y < z :
        print("Lower.")
    elif y <=9999 :
        print("Much lower.")
    else :
        print("Now that's just ridiculous.")
except :
    print("Error 808")

# phew!
print(" ")

try :
    if y == z :
        print("You no good fifty-six'en!! (stab, stab)")
    else :
        print("Try again Red...")
except :
    print("Error. Error. Please enter an Integer next time.")

    #lets see if that works

print(" ")
print("end of line")
