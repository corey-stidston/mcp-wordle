import json
import logging
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from wordle import Wordle, WordleGuessResult

mcp = FastMCP("mcp-wordle")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
game: Wordle

@mcp.tool()
def start_game() -> str:
    """
    Starts a new game, resetting the wordle game state and loading a new word.
    Wordle is a word puzzle where players have six attempts to guess a hidden five-letter word. 
    Each guess must be a valid five-letter word. 

    After submitting a guess, the game provides feedback:
    a) MATCH (green) means the letter is correct and in the right position,
    b) PARTIAL (yellow) means the letter is in the word but in the wrong position, and 
    c) MISS (grey) means the letter is not in the word at all
    
    Returns:
        A confirmation message indicating the game has started.
    """
    global game

    try:
        word = 'AUDIO'
        game = Wordle(word, get_word_list())
        logger.info(f"Wordle game reset, with new word {word}.")
        return "You've started a new game of wordle. Enjoy!"
    except Exception as e:
        logger.error(f"Wordle game failed to start. {e}")
        return f"Error: Could not start a new game of Wordle. Server might not be initialized. {e}"

def get_word_list() -> set[str]:
    script_dir = Path(__file__).parent
    word_list_path = script_dir / 'word_list.json'
    with open(word_list_path, 'r') as f:
        return set(json.load(f)['words'])

@mcp.tool()
def guess(guessed_word: str) -> WordleGuessResult:
    """
    Makes a guess in the current game of wordle.
    
    Args:
        guessed_word: the player's guess of the wordle word
    Returns:
        A dictionary containing the feedback of the guessed word, which letters were a match, partial match or miss.
        Additionally, the guseed word, the number of attempts remaining and the game status which is either:
        a) IN_PROGRESS, meaning there is a current game with >0 number of attempts left,
        b) WON, meaning you have guessed the correct word and the game is now over - congratulations! and,
        c) LOST, you were unable to guess the wordle word and you have run out of guesses - unlucky, try again!
    """
    global game
    return game.guess(guessed_word)
