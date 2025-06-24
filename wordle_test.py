import unittest

from wordle import GuessedAlreadyError, InvalidWordError, LengthMismatchError, LetterFeedback, Wordle, WordleGuessResult, LetterState

class TestWordleGame(unittest.TestCase):
    def setUp(self):
        self.game = Wordle('audio', {"audio", "alien", "tests", "texts", "tents", "thigh", "thaws", "thank"})

    def test_wordtoolong(self):
        with self.assertRaises(LengthMismatchError) as context:
            self.game.guess('thiswordistoolong')

        self.assertEqual("'thiswordistoolong' is too long.", str(context.exception))

    def test_wordtooshort(self):
        with self.assertRaises(LengthMismatchError) as context:
            self.game.guess('hi')

        self.assertEqual("'hi' is too short.", str(context.exception))

    def test_match_partial_miss(self):
        guessed_word = 'alien'
        result = self.game.guess(guessed_word)
        
        self.assertIsInstance(result, WordleGuessResult)
        self.assertEqual(result.guess, guessed_word)
        self.assertEqual(result.game_status, "IN_PROGRESS")
        self.assertEqual(len(result.feedback), len(guessed_word))
        self.assertIsNone(result.word)
        self.assertEqual(result.feedback, [
            LetterFeedback('a', LetterState.MATCH),
            LetterFeedback('l', LetterState.MISS),
            LetterFeedback('i', LetterState.PARTIAL),
            LetterFeedback('e', LetterState.MISS),
            LetterFeedback('n', LetterState.MISS)
        ])

    def test_repeatedword(self):
        self.game.guess('alien')

        with self.assertRaises(GuessedAlreadyError) as context:
            self.game.guess('alien')
        
        self.assertEqual("'alien' has already been guessed.", str(context.exception))

    def test_win(self):
        guessed_word = 'audio'
        result = self.game.guess(guessed_word)
        
        self.assertIsInstance(result, WordleGuessResult)
        self.assertEqual(result.guess, guessed_word)
        self.assertEqual(result.game_status, "WON")
        self.assertEqual(len(result.feedback), len(guessed_word))
        self.assertEqual(result.word, 'audio')
        
        for i, feedback in enumerate(result.feedback):
            self.assertEqual(feedback.state, LetterState.MATCH)
            self.assertEqual(feedback.letter, guessed_word[i])
    
    def test_lose(self):
        self.game.guess('tests')
        self.game.guess('texts')
        self.game.guess('tents')
        self.game.guess('thigh')
        self.game.guess('thaws')
        result = self.game.guess('thank')

        self.assertIsInstance(result, WordleGuessResult)
        self.assertEqual(result.game_status, "LOST")
        self.assertEqual(result.word, 'audio')

    def test_invalidword(self):
        test_cases = ['rxrxd', '12345', 'argh!']

        for word in test_cases:
            with self.subTest(word=word):
                with self.assertRaises(InvalidWordError) as context:
                    self.game.guess(word)
                self.assertEqual(f"'{word}' is not a valid word.", str(context.exception))

    def test_doubleletterguess_partialmatch(self):
        """
        Given a guess containing two of the same letter. If the wordle word contains only 1 of those letters,
        if neither letter is in the correct position, only the first letter should represent a partial match and the second a miss.
        """
        guessed_word = 'pasta'
        game = Wordle('audio')

        result = self.game.guess(guessed_word)

        self.assertIsInstance(result, WordleGuessResult)
        self.assertEqual(result.guess, guessed_word)
        self.assertEqual(result.feedback, [
            LetterFeedback('p', LetterState.MISS),
            LetterFeedback('a', LetterState.PARTIAL),
            LetterFeedback('s', LetterState.MISS),
            LetterFeedback('t', LetterState.MISS),
            LetterFeedback('a', LetterState.MISS)
        ])

    def test_doubleletterguess_match(self):
        """
        Given a guess containing two of the same letter. If the wordle word contains only 1 of those letters,
        if one of the letters is in the correct position, the first letter should repesent a miss.
        """
        guessed_word = 'algae'
        game = Wordle('audio')

        result = self.game.guess(guessed_word)

        self.assertIsInstance(result, WordleGuessResult)
        self.assertEqual(result.guess, guessed_word)
        self.assertEqual(result.feedback, [
            LetterFeedback('a', LetterState.MATCH),
            LetterFeedback('l', LetterState.MISS),
            LetterFeedback('g', LetterState.MISS),
            LetterFeedback('a', LetterState.MISS),
            LetterFeedback('e', LetterState.MISS)
        ])

if __name__ == '__main__':
    unittest.main()