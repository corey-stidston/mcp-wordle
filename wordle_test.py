# Test scenarios:
# Correct guess
# Incorrect guess
# Partial match guess
# Repeated word guess
# Invalid word guess
# Win scenario
# Loss scenario

# Give me a simple unit test scaffold using unittest for the Win scenario in a wordle game. Only implement that one test so i can do the others.

import unittest

from wordle import GuessedAlreadyError, LengthMismatchError, Wordle

class TestWordleGame(unittest.TestCase):

    def test_wordtoolong(self):
        game = Wordle('AUDIO')
        with self.assertRaises(LengthMismatchError) as context:
            game.guess('THISWORDISTOOLONG')

        self.assertEqual("Guessed word 'THISWORDISTOOLONG' is too long.", str(context.exception))

    def test_wordtooshort(self):
        game = Wordle('AUDIO')
        with self.assertRaises(LengthMismatchError) as context:
            game.guess('HI')

        self.assertEqual("Guessed word 'HI' is too short.", str(context.exception))

    def test_correctguess(self):
        game = Wordle('AUDIO')
        result = game.guess('ALIEN')
        self.assertEqual(result, [
            'MATCH', 'MISS', 'PARTIAL', 'MISS', 'MISS'
        ])

    def test_repeatedword(self):
        game = Wordle('AUDIO')
        game.guess('ALIEN')

        with self.assertRaises(GuessedAlreadyError) as context:
            game.guess('ALIEN')
        
        self.assertEqual("'ALIEN' has already been guessed.", str(context.exception))

    def test_win(self):
        game = Wordle('AUDIO')
        result = game.guess('AUDIO')
        
        self.assertEqual(result, [
            'MATCH', 'MATCH', 'MATCH', 'MATCH', 'MATCH'
        ])

    # def test_lose(self):
    #     game = Wordle('AUDIO')
    #     result = game.guess('AUDIO')
        
    #     self.assertEqual(result, [
    #         'MATCH', 'MATCH', 'MATCH', 'MATCH', 'MATCH'
    #     ]) 
        
if __name__ == '__main__':
    unittest.main()