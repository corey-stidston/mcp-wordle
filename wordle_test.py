import unittest

from wordle import GuessedAlreadyError, InvalidWordError, LengthMismatchError, LetterFeedback, Wordle, WordleGuessResult, LetterState

class TestWordleGame(unittest.TestCase):
    def test_wordtoolong(self):
        game = Wordle('audio')
        with self.assertRaises(LengthMismatchError) as context:
            game.guess('thiswordistoolong')

        self.assertEqual("Guessed word 'thiswordistoolong' is too long.", str(context.exception))

    def test_wordtooshort(self):
        game = Wordle('audio')
        with self.assertRaises(LengthMismatchError) as context:
            game.guess('hi')

        self.assertEqual("Guessed word 'hi' is too short.", str(context.exception))

    def test_correctguess(self):
        game = Wordle('audio')
        guessed_word = 'alien'
        result = game.guess(guessed_word)
        
        self.assertIsInstance(result, WordleGuessResult)
        self.assertEqual(result.guess, guessed_word)
        self.assertEqual(result.game_status, "IN_PROGRESS")
        self.assertEqual(len(result.feedback), len(guessed_word))

        self.assertEqual(result.feedback, [
            LetterFeedback('a', LetterState.MATCH),
            LetterFeedback('l', LetterState.MISS),
            LetterFeedback('i', LetterState.PARTIAL),
            LetterFeedback('e', LetterState.MISS),
            LetterFeedback('n', LetterState.MISS)
        ])

    def test_repeatedword(self):
        game = Wordle('audio')
        game.guess('alien')

        with self.assertRaises(GuessedAlreadyError) as context:
            game.guess('alien')
        
        self.assertEqual("'alien' has already been guessed.", str(context.exception))

    def test_win(self):
        game = Wordle('audio')
        guessed_word = 'audio'
        result = game.guess(guessed_word)
        
        self.assertIsInstance(result, WordleGuessResult)
        self.assertEqual(result.guess, guessed_word)
        self.assertEqual(result.game_status, "WON")
        self.assertEqual(len(result.feedback), len(guessed_word))
        
        for i, feedback in enumerate(result.feedback):
            self.assertEqual(feedback.state, LetterState.MATCH)
            self.assertEqual(feedback.letter, guessed_word[i])
    
    def test_lose(self):
        game = Wordle('audio')
        game.guess('tests')
        game.guess('texts')
        game.guess('tents')
        game.guess('thigh')
        game.guess('thaws')
        result = game.guess('thank')

        self.assertIsInstance(result, WordleGuessResult)
        self.assertEqual(result.game_status, "LOST")

    def test_invalidword(self):
        test_cases = ['rxrxd', '12345', 'argh!']
        game = Wordle('audio')

        for word in test_cases:
            with self.subTest(word=word):
                with self.assertRaises(InvalidWordError) as context:
                    game.guess(word)
                self.assertEqual(f"'{word}' is not a valid word.", str(context.exception))

    # TODO: double letters, partial mismatch

if __name__ == '__main__':
    unittest.main()