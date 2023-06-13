# import random

# # generate a random number between 1 and 100
# secret_number = random.randint(1, 100)

# # set the initial number of guesses to 0
# num_guesses = 34

# # loop until the user guesses the correct number
# while True:
#     # ask the user to guess the number
#     guess = int(input("Guess the secret number between 1 and 100: "))
    
#     # increment the number of guesses
#     num_guesses += 1
    
#     # check if the guess is correct
#     if guess == secret_number:
#         print("Congratulations! You guessed the secret number in", num_guesses, "guesses!")
#         break
    
#     # provide feedback on the guess
#     if guess < secret_number:
#         print("Too low! Guess again.")
#     else:
#         print("Too high! Guess again.")
