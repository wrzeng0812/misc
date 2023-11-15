from PyDictionary import PyDictionary
import enchant
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

class Boggle:
    def __init__(self, grid = None):
        self.grid = grid
        self.row = len(self.grid)
        self.column = len(self.grid[0])
        self.dictionary = enchant.Dict("en_US")
        self.minimum_length = 3
        
    def is_valid_word(self, word):
        return self.dictionary.check(word)

    def find_word_in_grid(self):
        def dfs(row, col, word):
            if row < 0 or row >= self.row or col < 0 or col >= self.column:
                return
            
            letter = self.grid[row][col]
            if letter == '*':
                return
            
            new_word = word + letter
            
            if len(new_word) >= self.minimum_length and self.is_valid_word(new_word):
                valid_words.add(new_word)
            
            original_letter, self.grid[row][col] = self.grid[row][col], '*'
            
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    dfs(row + dr, col + dc, new_word)
            
            self.grid[row][col] = original_letter
            
        valid_words = set()

        for row in range(self.row):
            for col in range(self.column):
                dfs(row, col, "")
                
        return valid_words

def get_meaning(word):
    webster = PyDictionary()
    try: 
        meaning = webster.meaning(word)
    except Exception as e:
        meaning = None
        logger.error(e)

    return meaning

if __name__ == '__main__':
    grid = [
        ['E', 'E', 'I', 'L'],
        ['T', 'QU', 'N', 'P'],
        ['A', 'O', 'N', 'T'],
        ['L', 'N', 'C', 'E']
    ]
    boggle = Boggle(grid = grid)
    
    words = boggle.find_word_in_grid()
    
    boggle_result = pd.DataFrame(data = {'word': list(words)})
    boggle_result['meaning'] = boggle_result['word'].apply(get_meaning)
    
