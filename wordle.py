import array
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Literal

class LetterState(Enum):
    MATCH = "MATCH"         # Correct letter in correct position
    PARTIAL = "PARTIAL"     # Correct letter in wrong position
    MISS = "MISS"           # Letter not in word

@dataclass
class LetterFeedback:
    """Represents feedback for a single letter in a guess."""
    letter: str
    state: LetterState

@dataclass
class WordleGuessResult:
    """Represents the complete feedback for a Wordle guess."""
    feedback: List[LetterFeedback]
    guess: str
    attempts_remaining: int
    game_status: Literal["IN_PROGRESS", "WON", "LOST"] = "IN_PROGRESS"
    
    def __post_init__(self):
        if len(self.guess) != len(self.feedback):
            raise ValueError("Guess length must match feedback length")
        
        if all(item.state == LetterState.MATCH for item in self.feedback):
            self.game_status = "WON"
        
        if self.attempts_remaining <= 0 and self.game_status == "IN_PROGRESS":
            self.game_status = "LOST"
    
    def to_dict(self) -> dict:
        """Convert to a dictionary suitable for JSON serialization."""
        return {
            "feedback": [
                {"letter": item.letter, "state": item.state.value} 
                for item in self.feedback
            ],
            "guess": self.guess,
            "attempts_remaining": self.attempts_remaining,
            "game_status": self.game_status
        }


class Wordle:
    MAX_NUMBER_OF_ATTEMPTS = 6

    def __init__(self, word):
        self.word = word
        self.guesses = []
        self.number_of_attempts = 0

    def guess(self, guessed_word) -> WordleGuessResult:
        if (len(guessed_word) != len(self.word)):
            raise LengthMismatchError(f"Guessed word '{guessed_word}' is too {'short' if len(guessed_word) < len(self.word) else 'long'}.")
        
        if (guessed_word in self.guesses):
            raise GuessedAlreadyError(f"'{guessed_word}' has already been guessed.")
        
        self.guesses.append(guessed_word)
        self.number_of_attempts = self.number_of_attempts + 1

        feedback = self._match(guessed_word)

        return WordleGuessResult(
            feedback = feedback,
            guess = guessed_word,
            attempts_remaining = self.MAX_NUMBER_OF_ATTEMPTS - self.number_of_attempts
        )
    
    def _match(self, guessed_word, output = None, index = 0) -> List[LetterFeedback]:
        if (output is None):
            output = []

        if (index == len(self.word)):
            return output
        
        if (guessed_word[index] == self.word[index]):
            output.append(LetterFeedback(guessed_word[index], LetterState.MATCH))
        elif (guessed_word[index] in self.word):
            output.append(LetterFeedback(guessed_word[index], LetterState.PARTIAL))
        else:
            output.append(LetterFeedback(guessed_word[index], LetterState.MISS))
        
        return self._match(guessed_word, output, (index + 1))


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

class InvalidWordError(WordleError):
    """Raised when the guessed word is not a valid word."""
    pass
