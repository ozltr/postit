import pyautogui
import pyperclip

from pprint import pprint
import time
from pathlib import Path
import random

# Get path to assets directory
asset_path = Path(__file__).parent.parent / 'assets'
history_path = Path(__file__).parent.parent / 'history'

# Battle.net client
battle_net_icon_path = asset_path.joinpath('battle_net_icon.png')
battle_net_play_button_path = asset_path.joinpath('battle_net_play_button.png')
battle_net_wow_classic_path = asset_path.joinpath('battle_net_wow_classic_icon.png')
battle_net_anniversary_path = asset_path.joinpath('battle_net_anniversary_realm.png')
battle_net_anniversary_button_path = asset_path.joinpath('battle_net_anniversary_realm_button.png')

# Character screen
wow_in_game_character_screen_postitnotes_path = asset_path.joinpath('wow_character_screen_postitnotes.png')

# Auction house and auctionator
wow_in_game_auctionator_close_results_path = asset_path.joinpath('wow_in_game_auctionator_close_results.png')
wow_in_game_auctionator_daytrade_search_path = asset_path.joinpath('wow_in_game_auctionator_daytrade_search.png')
wow_in_game_auctionator_export_results_path = asset_path.joinpath('wow_in_game_auctionator_export_results.png')
wow_in_game_auctionator_load_more_results_path = asset_path.joinpath('wow_in_game_auctionator_load_more_results.png')
wow_in_game_auctionator_shopping_path = asset_path.joinpath('wow_in_game_auctionator_shopping.png')
wow_in_game_menu_exit_game_path = asset_path.joinpath('wow_in_game_menu_exit_game.png')

# In-game auctioneer NPCs
wow_in_game_auctioneer_wabang_path = asset_path.joinpath('wow_in_game_auctioneer_wabang.png')
wow_in_game_auctioneer_thathung_path = asset_path.joinpath('wow_in_game_auctioneer_thathung.png')

def random_float_in_range(start: float = 0.8, end: float = 2.1) -> float:
    """Generate a random float between start and end."""
    return start + (end - start) * random.random()

def find(icon_path: Path, move_duration: int = 3, confidence: float = 0.9):
    icon = pyautogui.locateOnScreen(str(icon_path.resolve()), confidence=confidence)
    if icon is not None:
        loc = pyautogui.center(icon)
        # Move the mouse to the center of the Battle.net icon
        x = icon.left + icon.width - 10
        pyautogui.moveTo((x, loc.y), duration=move_duration)
    else:
        print(f"{icon_path} icon not found on the screen.")
        exit(1)

def find_and_click(icon_path: Path, move_duration: int = 3, confidence: float = 0.9):
    icon = pyautogui.locateOnScreen(str(icon_path.resolve()), confidence=confidence)
    if icon is not None:
        loc = pyautogui.center(icon)
        # Move the mouse to the center of the Battle.net icon
        pyautogui.moveTo(loc, duration=move_duration)
        pyautogui.click(loc)
    else:
        print(f"{icon_path} icon not found on the screen.")
        exit(1)

def find_and_click_twice(icon_path: Path, move_duration: int = 3, confidence: float = 0.9):
    icon = pyautogui.locateOnScreen(str(icon_path.resolve()), confidence=confidence)
    if icon is not None:
        loc = pyautogui.center(icon)
        # Move the mouse to the center of the Battle.net icon
        pyautogui.moveTo(loc, duration=move_duration)
        pyautogui.click(loc)
        time.sleep(0.2)
        pyautogui.click(loc)
    else:
        print(f"{icon_path} icon not found on the screen.")
        exit(1)

def find_and_right_click(icon_path: Path, move_duration: int = 3, confidence: float = 0.9):
    icon = pyautogui.locateOnScreen(str(icon_path.resolve()), confidence=confidence)
    if icon is not None:
        loc = pyautogui.center(icon)
        # Move the mouse to the center of the Battle.net icon
        pyautogui.moveTo(loc, duration=move_duration)
        pyautogui.rightClick(loc)
    else:
        print(f"{icon_path} icon not found on the screen.")
        exit(1)

def find_and_click_daytrade_search_icon(icon_path: Path, move_duration: int = 3, confidence: float = 0.9):
    icon = pyautogui.locateOnScreen(str(icon_path.resolve()), confidence=confidence)
    if icon is not None:
        loc = pyautogui.center(icon)
        # Move the mouse to the center of the Battle.net icon
        x = icon.left + icon.width - 10
        loc = (x, loc.y)
        pyautogui.moveTo(loc, duration=move_duration)
        pyautogui.click(loc)
    else:
        print(f"{icon_path} icon not found on the screen.")
        exit(1)

def wait(seconds: int, reason: str = ''):
    print(f"Waiting {seconds} seconds {reason}")
    time.sleep(seconds)

def start_wow_classic():
    """Start World of Warcraft Classic."""

    # Open battle.net client
    find_and_click(battle_net_icon_path, move_duration=random_float_in_range())
    wait(5, "after starting battle.net")

    # Pick World of Warcraft Classic tab
    find_and_click(battle_net_wow_classic_path, move_duration=random_float_in_range())
    wait(0.5, "after clicking wow classic")

    # Pick realms
    find_and_click(battle_net_anniversary_path, move_duration=random_float_in_range())
    wait(0.5, "after clicking realm picker")

    # Pick anniversary realm
    find_and_click(battle_net_anniversary_button_path, move_duration=random_float_in_range())
    wait(0.5, "after clicking anniversary realm")

    # Click play button
    find_and_click(battle_net_play_button_path, move_duration=random_float_in_range())
    wait(30, "after clicking wow classic play button")

def extract_auctionator_results():
    """
    Extract auctionator results\n
    Saves to CSV file in history directory, YYYY-MM-DD-HH-MM.csv\n
    Returns the clipboard content
    """

    # Pick character
    find_and_click_twice(wow_in_game_character_screen_postitnotes_path, move_duration=random_float_in_range(), confidence=0.5)
    wait(45, "after clicking character screen postitnotes")

    # Open auction house
    find_and_right_click(wow_in_game_auctioneer_thathung_path, move_duration=random_float_in_range(), confidence=0.6)
    wait(1, "after clicking auctioneer wabang")

    # Select auctionator shopping tab
    find_and_click(wow_in_game_auctionator_shopping_path, move_duration=random_float_in_range(), confidence=0.8)
    wait(1, "after clicking auctionator shopping")

    # Start querying daytrade list
    find_and_click_daytrade_search_icon(wow_in_game_auctionator_daytrade_search_path, move_duration=random_float_in_range(), confidence=0.8)
    wait(15, "after clicking auctionator daytrade search")

    # Load more results, to get supply
    find_and_click(wow_in_game_auctionator_load_more_results_path, move_duration=random_float_in_range())
    wait(40, "after clicking auctionator load more")

    # Open export results window
    find_and_click(wow_in_game_auctionator_export_results_path, move_duration=random_float_in_range())
    wait(1, "after clicking auctionator export results")

    # Simulates Ctrl+C, copies auctionator results
    pyautogui.hotkey('ctrl', 'c')
    wait(1, "after copying auctionator results to clipboard")

    # Dump clipboard content to CSV
    clipboard_content = pyperclip.paste()
    save_to_csv(clipboard_content)

    # Close export results window
    find_and_click(wow_in_game_auctionator_close_results_path, move_duration=random_float_in_range())
    wait(1, "after clicking auctionator close results")

    # Cose auction house
    pyautogui.hotkey('esc')
    wait(1, "after exiting auction house")

    # De-target auctioneer npc
    pyautogui.hotkey('esc')
    wait(1, "after de targeting auctioneer")

    # Open in-game menu
    pyautogui.hotkey('esc')
    wait(1, "after opening in-game menu")

    # Exit game
    find_and_click(wow_in_game_menu_exit_game_path, move_duration=random_float_in_range())
    wait(1, "after clicking exit game")

    return clipboard_content


def save_to_csv(data):
    # Get current timestamp
    timestamp = time.strftime("%Y-%m-%d-%H-%M")
    price_history_file_path = history_path.joinpath(f"{timestamp}.csv")

    # Write the auction data to a csv file
    with open(price_history_file_path, 'w', encoding='utf-8') as file:
        for line in data.splitlines():
            # Remove any leading or trailing whitespace
            line = line.strip()
            # Write the line to the file
            file.write(f"{line}\n")

if __name__ == "__main__":
    while True:
        time.sleep(5)

        # Start the game
        # start_wow_classic()

        # Autogui inside the game
        auction_data = extract_auctionator_results()

        # Close battle.net client
        find_and_click(battle_net_icon_path, move_duration=2, confidence=0.7)
        wait(1, "after closing battle.net")

        time.sleep(random_float_in_range(600, 1800))