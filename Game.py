import random
import time
def displayIntro():
    print (‘’You are in a land full of dragons.  In front of you, you see 2 caves. In one cave, the dragon is friendly and will share his treasure with you. The other dragon is greedy and hungry and will eat you on sight.’’)
    print()
def chooseCave():
    cave = ‘’
    while cave != ‘1’ and cave != ‘2’:
        print(‘Which cave will you go into? (1 or 2)’)
        cave = input()
    return cave
def checkCave(chosenCave):
    print(‘You approach the cave…’)
    time.sleep(2)
    print(‘It is dark and spooky…’)
def getGuess (alreadyGuessed):
    #returns the letter the player entered. This function makes sure the player entered a single letter and not something else
    while True:
        print(‘Guess a letter’)
        guess = input()
        guess = guess.lower()
        if len(guess) !=1:
            print(‘Please enter a single letter’)
        elif guess in alreadyGuessed:
            print(‘You have already guessed that letter.  Choose again’)
        elif guess not in ‘abcdefghijklmnopqrstuvwxyz’:
            print(‘Please enter a letter’)
        else:
            return guess
