import time
import pyautogui
from pynput             import mouse, keyboard
import pygetwindow      as gw
from PIL                import Image, ImageTk
import tkinter          as tk
import threading


class MouseCoordinates:


    def __init__(self):
        self.window = None
        self.control_pressed = False
        self.root = None  # Add this line to define self.root


    def locate_poker_window(self):
        """Locate the poker client window."""
        windows = gw.getWindowsWithTitle("No Limit")
        for window in windows:
            if "USD" in window.title:
                self.window = window
                print(f"Poker client window found. Size: {self.window.width}x{self.window.height}")
                return
        print("Poker client window not found.")



    def resize_poker_window(self, width, height):
        """Resize the poker client window to the specified width and height."""
        if self.window:
            self.window.resizeTo(width, height)
            print(f"Resized window to: Width={width}, Height={height}")
        else:
            print("Window not located. Please locate the window first.")



    def create_overlay(self):
        """Create an overlay window with an image on the poker client."""
        if not self.window:
            print("Poker client window not located. Cannot create overlay.")
            return

        root = tk.Tk()
        root.withdraw()  # Hide the root window

        # Create the overlay as a Toplevel window and assign it to self.overlay
        self.overlay = tk.Toplevel(root)
        self.overlay.title("Poker Overlay")
        self.overlay.geometry(f'{self.window.width}x{self.window.height}+{self.window.left}+{self.window.top}')

        # Load the image from the 'images/' directory
        image_path = 'images/PokerTable2.png'
        image = Image.open(image_path)
        self.photo = ImageTk.PhotoImage(image, master=self.overlay)

        label = tk.Label(self.overlay, image=self.photo)
        label.pack(fill=tk.BOTH, expand=True)

        self.overlay.overrideredirect(True)
        self.overlay.wm_attributes("-topmost", True)

          # Start the mouse listener thread here
        self.run_mouse_listener_in_thread()

        # Run the mainloop in the main thread
        root.mainloop()


    def overlay_update_method(self):
        # Update anything related to the overlay if needed
        pass



    def on_click(self, x, y, button, pressed):
        """Callback function to handle mouse clicks."""

        if pressed and self.control_pressed:
            relative_x = (x - self.window.left) / self.window.width
            relative_y = (y - self.window.top) / self.window.height

            with open("Mouse_testing/mouse_clicks.txt", "a") as file:
                file.write(f"Button Fold: {relative_x:.3f}, {relative_y:.3f}\n")


            print(f"Player Cards: x={relative_x:.3f}, y={relative_y:.3f}")



    def on_press(self, key):
        if key == keyboard.Key.ctrl_l:
            self.control_pressed = True

    def on_release(self, key):
        if key == keyboard.Key.ctrl_l:
            self.control_pressed = False



    def run_mouse_listener_in_thread(self):
        """Run the mouse listener in a separate thread."""
        listener_thread = threading.Thread(target=self.start_mouse_listener, daemon=True)
        listener_thread.start()



    def start_mouse_listener(self):
        """Start the mouse and keyboard listeners."""
        with mouse.Listener(on_click=self.on_click) as mouse_listener, keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as keyboard_listener:
            mouse_listener.join()
            keyboard_listener.join()



    def display_mouse_relative_position(self):
        """Display the mouse position relative to the poker window."""
        if not self.window:
            print("Window not located. Please locate the window first.")
            return

        try:
            print("Move your mouse over the poker window. Press CTRL+C to stop.")

            while True:

                x, y = pyautogui.position()

                relative_x = (x - self.window.left) / self.window.width
                relative_y = (y - self.window.top) / self.window.height

                print(f"Relative Mouse Position: x={relative_x:.3f}, y={relative_y:.3f}", end='\r')

                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\nStopped tracking mouse position.")


#Resize window 
default_width   = 963
default_height  = 692

mouse_manager = MouseCoordinates()
mouse_manager.locate_poker_window()
mouse_manager.resize_poker_window(default_width, default_height)
mouse_manager.create_overlay()  # Tkinter mainloop runs in the main thread, mouse listener starts before mainloop


# Run script:
# python mouse_coordinates.py

