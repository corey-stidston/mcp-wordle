import unittest

from wordle import GuessedAlreadyError, InvalidWordError, LengthMismatchError, LetterFeedback, Wordle, WordleGuessResult, LetterState

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
        guessed_word = 'ALIEN'
        result = game.guess(guessed_word)
        
        self.assertIsInstance(result, WordleGuessResult)
        self.assertEqual(result.guess, guessed_word)
        self.assertEqual(result.game_status, "IN_PROGRESS")
        self.assertEqual(len(result.feedback), len(guessed_word))

        self.assertEqual(result.feedback, [
            LetterFeedback('A', LetterState.MATCH),
            LetterFeedback('L', LetterState.MISS),
            LetterFeedback('I', LetterState.PARTIAL),
            LetterFeedback('E', LetterState.MISS),
            LetterFeedback('N', LetterState.MISS)
        ])

    def test_repeatedword(self):
        game = Wordle('AUDIO')
        game.guess('ALIEN')

        with self.assertRaises(GuessedAlreadyError) as context:
            game.guess('ALIEN')
        
        self.assertEqual("'ALIEN' has already been guessed.", str(context.exception))

    def test_win(self):
        game = Wordle('AUDIO')
        guessed_word = 'AUDIO'
        result = game.guess(guessed_word)
        
        self.assertIsInstance(result, WordleGuessResult)
        self.assertEqual(result.guess, guessed_word)
        self.assertEqual(result.game_status, "WON")
        self.assertEqual(len(result.feedback), len(guessed_word))
        
        for i, feedback in enumerate(result.feedback):
            self.assertEqual(feedback.state, LetterState.MATCH)
            self.assertEqual(feedback.letter, guessed_word[i])
    
    def test_lose(self):
        game = Wordle('AUDIO')
        game.guess('TESTS')
        game.guess('TEXTS')
        game.guess('TENTS')
        game.guess('THIGH')
        game.guess('THAWS')
        result = game.guess('THANK')

        self.assertIsInstance(result, WordleGuessResult)
        self.assertEqual(result.game_status, "LOST")

    def test_invalidword(self):
        test_cases = ['RXRXD', '12345', 'ARGH!']
        game = Wordle('AUDIO')

        for word in test_cases:
            with self.subTest(word=word):
                with self.assertRaises(InvalidWordError) as context:
                    game.guess(word)
                self.assertEqual("Guessed word 'THISWORDISTOOLONG' is too long.", str(context.exception))

if __name__ == '__main__':
    unittest.main()