import logging
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
    TODO: give context on the game of wordle and how the rules work
    
    Returns:
        A confirmation message indicating the game has started.
    """
    global game

    try:
        word = 'AUDIO'
        game = Wordle(word)
        logger.info(f"Wordle game reset, with new word {word}.")
        return "You've started a new game of wordle. Enjoy!"
    except Exception as e:
        logger.error(f"Wordle game failed to start. {e}")
        return f"Error: Could not start a new game of Wordle. Server might not be initialized. {e}"

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
