from dataclasses import dataclass, field
from colorama import Fore
from colorama import Style
import sys
import random
import os

@dataclass
class Result():
    yellow_count : int= 0
    gray_count: int=0
    green_count: int=0
    res: list = field(default_factory=list)
    def save(self):
        return (' '.join(f'{r.color}{r.letter}' for r in self.res) + f'{Style.RESET_ALL}') 
    def show(self):
        print(self.save())
    def show_stat(self):
        print(f'{Fore.GREEN}Correct:{self.green_count}\n{Fore.YELLOW}Wrong place:{self.yellow_count}\n{Fore.LIGHTRED_EX}No match:{self.gray_count}{Style.RESET_ALL}')

class Letter:
    def __init__ (self,letter, color=Fore.YELLOW):
        self.letter = letter
        self.color = color
    
    def set_correct(self):
        self.color = Fore.GREEN
    
    def set_unmatched(self):
        self.color = Fore.LIGHTRED_EX

    def __str__(self):
        return f'{self.color}{self.letter}{Style.RESET_ALL}'


def get_scrabble_score(w: str):
    score = 0
    if w.upper() in {'A', 'E', 'I', 'O', 'U', 'L', 'N', 'S', 'T', 'R'}:
        score += 1
    if w.upper() in {'D', 'G'}:
        score += 2
    if w.upper() in {'B', 'C', 'M', 'P'}:
        score =+ 3
    if w.upper() in {'F', 'H', 'V', 'W', 'Y'}:
        score =+ 4
    if w.upper() in ('K'):
        score =+ 5
    if w.upper() in {'J', 'X'}:
        score =+ 8
    if w.upper() in {'Q', 'Z'}:
        score =+ 10

    return score
  

def get_words_difficulty_level(scrabble_threshold, words, level):
    _level_words = []
        #calculate the scrabble score and return only hard words.
    for word_def in words:
        word = word_def.split(',')[0].replace('\n','')
        scrabble_score = 0
        for w in word:
            scrabble_score = scrabble_score + get_scrabble_score(w)
        if level == 'Hard' and scrabble_score > scrabble_threshold:
            _level_words.append(f'{word},' + word_def.split(',')[1].replace('\n',''))
        if level == 'Easy' and scrabble_score <= scrabble_threshold:
            _level_words.append(f'{word},' + word_def.split(',')[1].replace('\n',''))
    return _level_words

def play():
    level_chosen = False
    while not level_chosen:
        hard_mode = input('Do you want to play on Hard mode? (Y/N):')
        if hard_mode.upper() in ['Y', 'N']:
            level_chosen = True

    with open('English-5.csv', encoding='UTF-8') as wrds:
        words = wrds.readlines()
    
    if(hard_mode.upper()=='Y'):
        words = get_words_difficulty_level(10,words,'Hard')
    else:
        words = get_words_difficulty_level(10,words,'Easy')




    #parse out words and definitions
    #wordlist = [w.split(',')[0] for w in words]

    idx = random.randrange(1,len(words))
    answer = words[idx].split(',')[0].replace('\n','')
    definition = words[idx].split(',')[1].replace('\n','')

    hint_chosen = False
    hint = 'N'
    while not hint_chosen and hard_mode.upper() == 'N':
        hint = input('Do you want the definition? (Y/N):')
        if hint.upper() in ['Y', 'N']:
            hint_chosen = True

    if hint.upper() == 'Y':
        print(definition)


    #print(answer)

    invalid_letters =[]
    all_guesses = []
    num_turns = 5
    for turn in range(num_turns):
        valid_input = False
        while(not valid_input):
            guess = input(f'Guess ({turn+1}/{num_turns}):')
            guess = guess.upper()
            if len(guess) == len(answer):
                #if (f'{guess}' not in wordlist) and level == 'hard':
                #    print('That word isn''t known to me. Try again')
                #TODO check against letters that were missed? 
                #else:
                valid_input = True                
            else:
                print(f'Must be {len(answer)} letters.')
        os.system('cls' if os.name == 'nt' else 'clear')

        result = Result()
        for i in range(5):
            unmatched = False
            guess_letter = Letter(guess[i])
            #print(guess_letter.letter)
            for x in range(5):
                if i == x and guess[i] == answer[x]:
                    guess_letter.set_correct()
                    result.green_count +=1
                elif guess_letter.letter not in answer:
                    unmatched = True
                    invalid_letters.append(guess_letter.letter)

            if unmatched:
                guess_letter.set_unmatched()
                result.gray_count +=1
            result.yellow_count = 5 - (result.green_count + result.gray_count)
            result.res.append(guess_letter)

        all_guesses.append(result.save())
        for a in all_guesses:
            print(a)

        if hint.upper() == 'Y':
            result.show_stat()

        if hard_mode.upper() == 'N':
            result.show_stat()
            print('Guessed letters:', ', '.join(set(invalid_letters)))

        if result.green_count == len(answer):
            print(f'You win! {Fore.GREEN}{answer.upper()}{Style.RESET_ALL} : {definition}')
            another_turn_chosen = False
            while not another_turn_chosen:
                play_again = input('Do you want to play on again? (Y/N):')
                if play_again.upper() in ['Y', 'N']:
                    another_turn_chosen = True
                    return play_again.upper() == 'Y'

        if hint.upper() == 'Y':
            print(f'Definition: {definition}')

    print(f'You lost. The word was {Fore.GREEN}{answer.upper()}{Style.RESET_ALL}')
    another_turn_chosen = False
    while not another_turn_chosen:
        play_again = input('Do you want to play on again? (Y/N):')
        if play_again.upper() in ['Y', 'N']:
            another_turn_chosen = True
            return play_again.upper() == 'Y'


           


if __name__ == '__main__':
    
    end_game = True
    while end_game:
        end_game = play()
    print('Thanks for playing wordle!')
    sys.exit()