from enum import Enum


class Wordle:
    word = None
    guesses = []

    def __init__(self, word):
        self.word = word

    def guess(self, guessed_word) -> dict:
        if (len(guessed_word) != len(self.word)):
            raise LengthMismatchError(f"Guessed word '{guessed_word}' is too {'short' if len(guessed_word) < len(self.word) else 'long'}.")
        
        if (guessed_word in self.guesses):
            raise GuessedAlreadyError(f"'{guessed_word}' has already been guessed.")
        
        self.guesses.append(guessed_word)

        return self._match(guessed_word)
    
    def _match(self, guessed_word, output = None, index = 0) -> dict:
        if (output is None):
            output = []

        if (index == len(self.word)):
            return output
        
        if (guessed_word[index] == self.word[index]):
            output.append(LetterState.MATCH.value)
        elif (guessed_word[index] in self.word):
            output.append(LetterState.PARTIAL.value)
        else:
            output.append(LetterState.MISS.value)
        
        return self._match(guessed_word, output, (index + 1))


class LetterState(Enum):
    PARTIAL = "PARTIAL"
    MATCH = "MATCH"
    MISS = "MISS"

class WordleError(Exception):
    """Base exception class for all Wordle game errors."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
    
class LengthMismatchError(WordleError):
    """Raised when the guessed word length doesn't match the target word length."""
    pass

class GuessedAlreadyError(WordleError):
    """Raised when the guessed word has already been guessed."""
    pass
