from dataclasses import dataclass
from enum import Enum
from typing import List, Literal

class LetterState(Enum):
    MATCH = "MATCH"                     # Correct letter in correct position
    PARTIAL_MATCH = "PARTIAL_MATCH"     # Correct letter in wrong position
    MISS = "MISS"                       # Letter not in word

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
    word: str | None = None
    game_status: Literal["IN_PROGRESS", "WON", "LOST"] = "IN_PROGRESS"
    
    def __post_init__(self):
        if len(self.guess) != len(self.feedback):
            raise ValueError("Guess length must match feedback length")
        
        if all(item.state == LetterState.MATCH for item in self.feedback):
            self.game_status = "WON"
        
        if self.attempts_remaining <= 0 and self.game_status == "IN_PROGRESS":
            self.game_status = "LOST"

class Wordle:
    MAX_NUMBER_OF_ATTEMPTS = 6
    
    def __init__(self, word, word_list):
        self.word = word.lower()
        self.guesses = []
        self.number_of_attempts = 0
        self.word_list = word_list

    def guess(self, guessed_word) -> WordleGuessResult:
        guessed_word = guessed_word.lower()
        
        if (len(guessed_word) != len(self.word)):
            raise LengthMismatchError(f"'{guessed_word}' is too {'short' if len(guessed_word) < len(self.word) else 'long'}.")
        
        if (guessed_word in self.guesses):
            raise GuessedAlreadyError(f"'{guessed_word}' has already been guessed.")
        
        if guessed_word not in self.word_list:
            raise InvalidWordError(f"'{guessed_word}' is not a valid word.")
        
        self.guesses.append(guessed_word)
        self.number_of_attempts = self.number_of_attempts + 1

        feedback = self._match(guessed_word)
        attempts_remaining = self.MAX_NUMBER_OF_ATTEMPTS - self.number_of_attempts
        
        result = WordleGuessResult(
            feedback=feedback,
            guess=guessed_word,
            attempts_remaining=attempts_remaining
        )
        
        if result.game_status in ["WON", "LOST"]:
            result.word = self.word
            
        return result
    
    def _match(self, guessed_word) -> List[LetterFeedback]:
        feedback = [None] * len(guessed_word)
        target_letter_counts = {}
        
        # Count letters in target word
        for letter in self.word:
            target_letter_counts[letter] = target_letter_counts.get(letter, 0) + 1
        
        # First pass: Mark exact matches and reduce available counts
        for i in range(len(guessed_word)):
            if guessed_word[i] == self.word[i]:
                feedback[i] = LetterFeedback(guessed_word[i], LetterState.MATCH)
                target_letter_counts[guessed_word[i]] -= 1
        
        # Second pass: Mark partial matches and misses
        for i in range(len(guessed_word)):
            if feedback[i] is None:  # Not already marked as exact match
                letter = guessed_word[i]
                if target_letter_counts.get(letter, 0) > 0:
                    feedback[i] = LetterFeedback(letter, LetterState.PARTIAL_MATCH)
                    target_letter_counts[letter] -= 1
                else:
                    feedback[i] = LetterFeedback(letter, LetterState.MISS)
        
        return feedback

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
