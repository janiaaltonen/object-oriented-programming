from random import randrange

word = None
printable = []
guesses = 0
corrects = set()
missed = set()
hangintree = ('koroke', 'pystypuu', 'tukirauta', 'poikkipuu', 'köysi', 'pää', 'torso', 'kädet', 'jalat')
used_words = []


def readWords(filename='hangman_words.txt'):
    """
    * function reads guessable words from txt. file and returns them in a tuple
    """
    file = None
    words = []
    try:
        file = open(filename, 'r', encoding="utf-8")
        for row in file:
            row = row.strip()
            if len(row) > 0:
                words.append(row)
        file.close()
    except (FileNotFoundError, IOError) as error:
        print(f'Tiedostoa {filename} ei voitu lukea: {error}')
    finally:
        if file is not None:
            file.close()
    return tuple(words)


def generate():
    """
    * function takes random word out of tuple(words)
    * used words are placed in used_words[] so they won't pop up again
    """
    global word, used_words
    while True:
        word = words[randrange(len(words))]
        if word not in used_words:
            used_words.append(word)
            break


def show():
    """
    * function prints right guessed letters and '_' in place of letters that are not guessed
    """
    global printable
    if len(printable) > 0:
        print(*printable)
        print()
    else:
        printable = ['_'] * len(word)
        print(*printable)
        print()


def guess():
    """
    * verify that user_input is letter or '-' sign
    * checks that letter is not guessed before
    * returns user_input
    """
    while True:
        user_input = input("Guess a letter: ").lower()
        if len(user_input) == 1 and user_input.isalpha() or user_input == '-':
            if user_input not in corrects and user_input not in missed:
                return user_input


def check(letter):
    """
    * function checks if the input_letter is in random word, updates corrects set() and returns True
    * if not in random word updates missed set() and returns False
    * updates guesses
    * places input_letter to correct position(s) in printable[]
    """
    global guesses, corrects, missed
    index_places = [i for i, e in enumerate(word) if e == letter]
    if len(index_places) > 0:
        corrects.add(letter)
        for i in index_places:
            printable[i] = letter
            guesses += 1
        return True
    else:
        missed.add(letter)
        return False


def isContinue():
    """
    * function asks from user if one wants to continue with new word
    * if yes, reset variables: printable, guesses, missed and corrects and returns True
    * else returns False
    """
    global printable, guesses, corrects, missed
    letter = input('Continue with a new word [y/Y]?:\t')
    if len(letter) > 0 and letter.isalpha() and letter[0].lower() == 'y':
        printable = []
        guesses = 0
        corrects = set()
        missed = set()
        return True
    else:
        return False


def play():
    """
    mainfunction that initializes game variables and implements game loop
    """
    global words
    words = readWords()
    print('Hangman - guess word letter by letter. Wrong guesses may hang you.')
    while True:
        generate()
        while True:
            show()
            if check(guess()):
                if guesses == len(word):
                    print(f'{word.upper()}', 'is correct! Well done!!', sep='\n')
                    break
            else:
                print(f'Sorry, wrong guess - that is {len(missed)}. part {hangintree[len(missed)-1]} in your hangintree')
                if len(missed) == len(hangintree):
                    print(f'HANGED!!', 'You failed to guess ', f'{word.upper()}', sep='\n')
                    break
        if not isContinue():
            break


if __name__ == '__main__':
    play()
