import keyboard
import time

def on_key_press(event):
    if event.name == 'esc':
        # Stop the program when the 'esc' key is pressed
        keyboard.unhook_all()
    else:
        # Print the key name and the elapsed time since the program started
        print(f"Key: {event.name}, Time: {time.time() - start_time:.3f} seconds")

# Register the key release event handler
keyboard.on_press(on_key_press)

# Start time when the program begins
start_time = time.time()

# Keep the program running until the 'esc' key is pressed
keyboard.wait('esc')