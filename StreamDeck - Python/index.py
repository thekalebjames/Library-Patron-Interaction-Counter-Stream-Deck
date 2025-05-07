#imported libraries
from StreamDeck.DeviceManager import DeviceManager
from datetime import datetime
import time
import threading

# Dictionary to store hourly button press counts
press_count = {}
lock = threading.Lock()

def log_counts_to_file():
    """Continuously check and log counts when the hour changes."""
    last_logged_hour = None
    while True:
        time.sleep(60)
        current_hour = datetime.now().strftime('%Y-%m-%d %H:00')

        with lock:
            for hour in list(press_count):
                if hour != current_hour and hour != last_logged_hour:
                    with open("test.txt", "a") as f:
                        f.write(f"{hour}: {press_count[hour]} presses\n")
                    last_logged_hour = hour

def on_key_change(deck, key, state):
    """Callback for button press."""
    if key==4 and state:  # Only count key down (not key release)
        #sets the hours to the current date and time and converts it to a string to print
        hour_key = datetime.now().strftime('%Y-%m-%d %H:00')
        with lock:
            press_count[hour_key] = press_count.get(hour_key, 0) + 1
        print(f"Button {key} pressed at {hour_key}")

def main():
    # Get connected Stream Decks
    decks = DeviceManager().enumerate()
    if not decks:
        print("No Stream Decks found.")
        return

    deck = decks[0]
    deck.open()
    deck.reset()

    deck.set_brightness(30)

    # Set key press callback
    deck.set_key_callback(on_key_change)

    print("Stream Deck is running. Press keys to track.")
    
    # Start background logging thread
    threading.Thread(target=log_counts_to_file, daemon=True).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        deck.reset()
        deck.close()
        print("Stopped.")

if __name__ == "__main__":
    main()
