from random import randrange

print("Welcome to play hangman! At this version you won't lose :) ")
print()


# tuple of some random words to use in hangman
words = ('kamina', 'happipullo', 'oravannahka', 'kahvikuppi', 'juoksukengät', 'kello', 'tarina', 'suurennuslasi')

# create alphabetic list using map
alphabets = list(map(chr, range(97, 123)))

# adding Finnish letters and - character as said in assignment
alphabets.extend(['å', 'ä', 'ö', '-'])

while True:
    # takes one random word out of tuple
    word = words[randrange(len(words))]

    # remove the randomly picked word from words so it won't pop up again
    # if user plays more than one round
    used_words = list(words)
    used_words.remove(word)
    words = tuple(used_words)

    # set removes duplicate chars from random word
    unique_chars = set(word)

    # count of unique characters
    # how many right guesses are needed
    needed_guesses = len(unique_chars)

    # list printable has same size as random word
    printable = ['_'] * len(word)

    # prints every element in list on one line like: _ _ _
    print(*printable)
    print()
    # right guesses
    guesses = 0

    # inner loop rolls as long as all the characters are guessed
    while guesses < needed_guesses:

        """takes care that user input is between a-ö or -"""
        while True:
            user_input = input("Guess a letter: ").lower()
            print()
            if user_input in alphabets:
                break
            else:
                print(user_input, "is not a letter nor '-' symbol ")
                print()
                print(*printable)
                continue

        """
        checks if the given input letter is in word. if so:
        adds one guess
        removes that letter for word's unique letter set
        checks what/which indexes belong to that letter
        adds them to correct position in printable list
        """
        if user_input in unique_chars:
            guesses += 1
            unique_chars.remove(user_input)
            g = [i for i, e in enumerate(word) if e == user_input]
            for i in g:
                printable[i] = user_input

        print(*printable)
        print()

    # if words is empty, player guessed all the words and game is over
    if len(words) == 0:
        print("You guessed right all the words, congratulations!")
        break

    # ask from the user if one wants to quit, otherwise draw new word
    restart = input("To quit the game press Q, otherwise the game will draw new word to guess ")
    if restart == "Q":
        break
