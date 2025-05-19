import sys
import termios
import tty
import select

def get_keycode():
    """Reads a single key press from the terminal and returns its keycode."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        if select.select([sys.stdin], [], [], 1)[0]:  # Wait up to 1 second for input
            ch = sys.stdin.read(1)
            return ord(ch)
        else:
            return None  # No key pressed within the timeout
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

if __name__ == "__main__":
    print("Press any key (Ctrl+C to exit)...")
    try:
        while True:
            keycode = get_keycode()
            if keycode is not None:
                print(f"Keycode: {keycode}")
            # You can add a small delay here if needed to reduce CPU usage
            # import time
            # time.sleep(0.05)
    except KeyboardInterrupt:
        print("\nExiting.")