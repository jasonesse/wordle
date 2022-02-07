from dataclasses import dataclass, field
from colorama import Fore
from colorama import Style
import sys
import random

@dataclass
class Result():
    yellow_count : int= 0
    gray_count: int=0
    green_count: int=0
    res: list = field(default_factory=list)
    def show(self):
        print(''.join(f'{r.color}{r.letter}' for r in self.res) + f'{Style.RESET_ALL}')
    def show_stat(self):
        print(f'{Fore.GREEN}Green:{self.green_count}\n{Fore.YELLOW}Yellow:{self.yellow_count}\n{Fore.LIGHTRED_EX}Gray:{self.gray_count}\n{Style.RESET_ALL}')

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



def play():

    level = input('Level (easy/hard):')

    with open('English-5.csv', encoding='UTF-8') as wrds:
        words = wrds.readlines()

    answer = words[random.randrange(1,len(words))].replace('\n','')

    invalid_letters =[]

    for _ in range(5):
        valid_input = False
        while(not valid_input):
            guess = input('Guess:')
            guess = guess.upper()
            if len(guess) == 5:
                if (f'{guess}\n' not in words):
                    print('That word isn''t known to me. Try again')
                else:
                    valid_input = True                
            else:
                print('Must be 5 letters.')
            


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
            if result.green_count == 5:
                print('You win!')
                result.show()
                sys.exit()
    
        if level == 'hard':
            result.show_stat()
        
        if level == 'easy':
            result.show()
            result.show_stat()
            print('Guessed letters:', ', '.join(set(invalid_letters)))
    
    print(f'You lost. The word was {Fore.GREEN}{answer.upper()}{Style.RESET_ALL}')
           


if __name__ == '__main__':
    play()