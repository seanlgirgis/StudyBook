import sys
import os
import json
import pyperclip
from pynput import keyboard
import time
from PyQt6.QtCore import QThread, pyqtSignal, QObject, Qt
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QLineEdit, QPushButton, QHBoxLayout,
    QMessageBox, QLabel, QScrollArea, QFrame, QDialog, QDialogButtonBox, QTextEdit
)

# =============================================================================
# DATA STORAGE (How the app remembers your snippets)
# =============================================================================

# Get the absolute path of the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Define the absolute path to the data file
DATABASE_PATH = os.path.join(SCRIPT_DIR, 'clipboard_data.json')
SETTINGS_PATH = os.path.join(SCRIPT_DIR, 'settings.json')

# Hotkey presets. Keep a fallback for each action in case a shortcut is already
# reserved by another app on the system.
DEFAULT_SHOW_WINDOW_HOTKEYS = [
    '<ctrl>+<shift>+s',  # Primary: Show/hide picker window
    '<ctrl>+<alt>+s',    # Fallback
]

DEFAULT_CAPTURE_CLIPBOARD_HOTKEYS = [
    '<f11>',             # Primary: Save current clipboard text into manager
    '<ctrl>+<alt>+a',    # Fallback
]


def load_settings():
    """
    Loads hotkey settings from settings.json.
    Falls back to defaults if the file is missing or malformed.
    """
    defaults = {
        "show_window_hotkeys": list(DEFAULT_SHOW_WINDOW_HOTKEYS),
        "capture_clipboard_hotkeys": list(DEFAULT_CAPTURE_CLIPBOARD_HOTKEYS),
    }
    try:
        with open(SETTINGS_PATH, 'r') as f:
            raw_settings = json.load(f)
            if not isinstance(raw_settings, dict):
                return defaults
    except (FileNotFoundError, json.JSONDecodeError):
        return defaults

    def normalize_hotkeys(value, fallback):
        if isinstance(value, str):
            value = [value]
        if not isinstance(value, list):
            return list(fallback)

        cleaned = []
        for item in value:
            if isinstance(item, str):
                hotkey = item.strip().lower()
                if hotkey:
                    cleaned.append(hotkey)
        return cleaned if cleaned else list(fallback)

    return {
        "show_window_hotkeys": normalize_hotkeys(
            raw_settings.get("show_window_hotkeys"),
            DEFAULT_SHOW_WINDOW_HOTKEYS
        ),
        "capture_clipboard_hotkeys": normalize_hotkeys(
            raw_settings.get("capture_clipboard_hotkeys"),
            DEFAULT_CAPTURE_CLIPBOARD_HOTKEYS
        ),
    }


def ensure_settings_file():
    """Create settings.json with defaults if it does not exist yet."""
    if os.path.exists(SETTINGS_PATH):
        return
    default_settings = {
        "show_window_hotkeys": DEFAULT_SHOW_WINDOW_HOTKEYS,
        "capture_clipboard_hotkeys": DEFAULT_CAPTURE_CLIPBOARD_HOTKEYS,
    }
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(default_settings, f, indent=4)

def load_clipboard_data():
    """
    Tries to open 'clipboard_data.json' and read the list of snippets.
    If the file doesn't exist yet, it just returns an empty list [].
    """
    try:
        with open(DATABASE_PATH, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If file is missing or broken, start fresh with nothing
        return []

def save_clipboard_data(data):
    """
    Takes the current list of snippets and writes them into 'clipboard_data.json'
    so that they are still there the next time you open the app.
    """
    with open(DATABASE_PATH, 'w') as f:
        json.dump(data, f, indent=4)

# =============================================================================
# KEYBOARD LISTENER (How the app "hears" your hotkeys)
# =============================================================================

class HotkeySignals(QObject):
    """
    This is like a 'messenger'. When a key is pressed, it sends a message
    to the main app window to do something (like show/hide).
    """
    toggle_visibility = pyqtSignal()   # Message: "Hey, show or hide yourself!"
    add_from_clipboard = pyqtSignal()  # Message: "Take what's in the system clipboard and save it!"

class HotkeyThread(QThread):
    """
    This runs in the 'background' of the app, constantly watching the keyboard
    without freezing the window you see on screen.
    """
    def __init__(self, signals, show_hotkeys, capture_hotkeys):
        super().__init__()
        self.signals = signals
        self.listener = None
        self.show_hotkeys = show_hotkeys
        self.capture_hotkeys = capture_hotkeys

    def run(self):
        # We define which keys do what here
        hotkeys = {}
        for hk in self.show_hotkeys:
            hotkeys[hk] = self.signals.toggle_visibility.emit
        for hk in self.capture_hotkeys:
            hotkeys[hk] = self.signals.add_from_clipboard.emit
        # Start listening to the keyboard globally
        with keyboard.GlobalHotKeys(hotkeys) as listener:
            self.listener = listener
            listener.join()

    def stop(self):
        """Turn off the keyboard listener when the app closes."""
        if self.listener:
            self.listener.stop()

# =============================================================================
# SNIPPET CARD (The 'box' for each single piece of text)
# =============================================================================

class SnippetCard(QFrame):
    """
    This represents one row (one box) in your list. 
    It has the text and three buttons: Copy, Edit, and Delete (X).
    """
    def __init__(self, text, index, parent_window):
        super().__init__()
        self.text_content = text # The actual hidden text
        self.index = index      # Where it lives in the list
        self.parent_window = parent_window # The main window this box belongs to
        
        # Make the box look nice with borders and colors
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
            SnippetCard {
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-bottom: 5px;
            }
            QLineEdit {
                border: none;
                background: transparent;
                font-size: 14px;
                color: #333;
            }
            QPushButton {
                background-color: #e0e0e0;
                border: none;
                border-radius: 3px;
                padding: 4px 8px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
            #copyBtn { color: #0055aa; }  /* Blue-ish */
            #editBtn { color: #555555; }  /* Gray */
            #delBtn { color: #cc0000; }   /* Red */
        """)

        # Items in this box will be side-by-side (Horizontal)
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)

        # 1. THE TEXT DISPLAY: A simple box showing the text.
        # It is 'ReadOnly' so you can't type over it directly.
        self.text_display = QLineEdit(text)
        self.text_display.setReadOnly(True)
        self.text_display.setCursorPosition(0)
        layout.addWidget(self.text_display)

        # 2. THE COPY BUTTON: Clicking this copies the text and hides the app.
        self.copy_btn = QPushButton("Copy")
        self.copy_btn.setObjectName("copyBtn")
        self.copy_btn.clicked.connect(self.on_copy)
        
        # 3. THE EDIT BUTTON: Opens a popup to change the text.
        self.edit_btn = QPushButton("Edit")
        self.edit_btn.setObjectName("editBtn")
        self.edit_btn.clicked.connect(self.on_edit)
        
        # 4. THE DELETE BUTTON (X): Irreversibly removes this snippet.
        self.del_btn = QPushButton("✕")
        self.del_btn.setObjectName("delBtn")
        self.del_btn.setFixedWidth(30)
        self.del_btn.clicked.connect(self.on_delete)

        # Add buttons to the layout
        layout.addWidget(self.copy_btn)
        layout.addWidget(self.edit_btn)
        layout.addWidget(self.del_btn)

        self.setLayout(layout)

    def on_copy(self):
        """What happens when you click 'Copy'."""
        self.parent_window.paste_snippet(self.text_content)

    def on_edit(self):
        """What happens when you click 'Edit'."""
        self.parent_window.edit_snippet(self.index)

    def on_delete(self):
        """What happens when you click the 'X'."""
        self.parent_window.delete_snippet(self.index)

# =============================================================================
# SNIPPET DIALOG (The popup window for typing)
# =============================================================================

class SnippetDialog(QDialog):
    """
    This is a small 'popup' window that appears when you want to ADD or EDIT text.
    It has a big text area and OK / CANCEL buttons.
    """
    def __init__(self, parent=None, initial_text=""):
        super().__init__(parent)
        self.setWindowTitle("Snippet Editor") # Title of the popup
        layout = QVBoxLayout()
        
        # Big text editor box
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(initial_text)
        layout.addWidget(self.text_edit)
        
        # OK and Cancel buttons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept) # Close popup and save
        buttons.rejected.connect(self.reject) # Close popup and forget
        layout.addWidget(buttons)
        
        self.setLayout(layout)
    
    def get_text(self):
        """Get the text you typed after you hit OK."""
        return self.text_edit.toPlainText().strip()

# =============================================================================
# MAIN WINDOW (The controller of everything)
# =============================================================================

class ClipboardManagerApp(QMainWindow):
    """
    The main app you see. It manages the list of snippets and the overall look.
    """
    def __init__(self):
        super().__init__()
        ensure_settings_file()
        self.settings = load_settings()
        self.show_hotkeys = self.settings["show_window_hotkeys"]
        self.capture_hotkeys = self.settings["capture_clipboard_hotkeys"]
        self.setWindowTitle("Universal Clipboard Manager")
        self.setGeometry(100, 100, 450, 600) # (X, Y, Width, Height)

        # The 'Central Widget' holds everything inside the window
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget) # Vertical (Top to Bottom)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        # 1. THE SCROLL AREA: If you have 50 snippets, this lets you scroll down.
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop) # Stick boxes to the top
        self.scroll_area.setWidget(self.scroll_content)
        
        self.main_layout.addWidget(self.scroll_area)

        # 2. THE BOTTOM BAR: Buttons at the very bottom.
        self.bottom_bar = QHBoxLayout()
        
        # 'Add New' button (Green)
        self.add_btn = QPushButton("Add New Snippet")
        self.add_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-weight: bold; border-radius: 5px;")
        self.add_btn.clicked.connect(self.add_new_snippet)
        
        # 'Close' button (Gray) - Just hides the window, doesn't quit the program!
        self.close_btn = QPushButton("Close")
        self.close_btn.setStyleSheet("background-color: #666; color: white; padding: 10px; border-radius: 5px;")
        self.close_btn.clicked.connect(self.hide)

        self.bottom_bar.addWidget(self.add_btn)
        self.bottom_bar.addWidget(self.close_btn)
        
        self.main_layout.addLayout(self.bottom_bar)

        # Quick shortcut reminder so it's clear which action each hotkey runs.
        self.shortcuts_hint = QLabel(
            "Show/Hide: " + ", ".join(self.show_hotkeys) + "  |  "
            "Capture Clipboard: " + ", ".join(self.capture_hotkeys)
        )
        self.shortcuts_hint.setStyleSheet("color: #666; font-size: 11px;")
        self.main_layout.addWidget(self.shortcuts_hint)

        # 3. INITIAL DATA: Load snippets from the file and show them.
        self.items = load_clipboard_data()
        self.refresh_snippets()

        # 4. HOTKEYS SETUP: Start the background listener.
        self.hotkey_signals = HotkeySignals()
        self.hotkey_thread = HotkeyThread(
            self.hotkey_signals,
            self.show_hotkeys,
            self.capture_hotkeys
        )
        # Connect signals (messages) to our functions
        self.hotkey_signals.toggle_visibility.connect(self.toggle_visibility)
        self.hotkey_signals.add_from_clipboard.connect(self.add_from_clipboard)
        self.hotkey_thread.start()
        
        # Show the app when it first runs
        self.show()

    def closeEvent(self, event):
        """
        Special function: When you click the 'X' on top right, 
        we 'ignore' the close message and just 'hide' the window.
        """
        event.ignore()
        self.hide()

    def refresh_snippets(self):
        """
        Clears the whole visible list and redraws all boxes based on 'self.items'.
        """
        # Delete old visual boxes
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Create new visual boxes for every piece of data
        for i, text in enumerate(self.items):
            card = SnippetCard(text, i, self)
            self.scroll_layout.addWidget(card)

    def add_new_snippet(self):
        """
        Opens the popup to type a new snippet. 
        If you hit OK, it saves it and refreshes the list.
        """
        dialog = SnippetDialog(self)
        if dialog.exec():
            new_text = dialog.get_text()
            if new_text:
                self.items.insert(0, new_text) # Put it at the very top
                save_clipboard_data(self.items)
                self.refresh_snippets()

    def edit_snippet(self, index):
        """
        Opens the popup with existing text so you can change it.
        """
        if 0 <= index < len(self.items):
            old_text = self.items[index]
            dialog = SnippetDialog(self, old_text)
            if dialog.exec():
                new_text = dialog.get_text()
                if new_text:
                    self.items[index] = new_text
                    save_clipboard_data(self.items)
                    self.refresh_snippets()

    def delete_snippet(self, index):
        """
        Asks 'Are you sure?' then removes the snippet if you say Yes.
        """
        if 0 <= index < len(self.items):
            confirm = QMessageBox.question(
                self, "Confirm Delete",
                "Are you sure you want to delete this snippet?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirm == QMessageBox.StandardButton.Yes:
                del self.items[index]
                save_clipboard_data(self.items)
                self.refresh_snippets()

    def paste_snippet(self, text):
        """
        1. Copies the text to your invisible system clipboard.
        2. Hides this app window.
        3. Waits a split second, then tells Windows to press 'Ctrl + V' (Paste).
        """
        pyperclip.copy(text)
        self.hide()
        
        # Wait for the window to fully disappear before pasting
        QApplication.processEvents() 
        time.sleep(0.2)
        
        # Simulate pressing the keys
        keyboard_controller = keyboard.Controller()
        with keyboard_controller.pressed(keyboard.Key.ctrl):
            keyboard_controller.press('v')
            keyboard_controller.release('v')
            
    def add_from_clipboard(self):
        """
        Grabs whatever you've recently copied outside this app 
        and adds it to the list automatically!
        """
        clipboard_text = pyperclip.paste().strip()
        if clipboard_text and (not self.items or clipboard_text != self.items[0]):
            self.items.insert(0, clipboard_text)
            save_clipboard_data(self.items)
            self.refresh_snippets()

    def toggle_visibility(self):
        """
        Flips between hidden and visible when you hit the hotkey.
        """
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.raise_() # Bring to absolute front
            self.activateWindow() # Make it the focus

# =============================================================================
# STARTING THE ENGINE
# =============================================================================

if __name__ == '__main__':
    # Small delay to ensure Windows Desktop is ready
    time.sleep(1)
    
    # Start the system foundation
    app = QApplication(sys.argv)
    
    # Create our app window
    window = ClipboardManagerApp()
    
    def on_app_exit():
        """Clean up when we actually shut down the whole computer/process."""
        if window.hotkey_thread:
            window.hotkey_thread.stop()
            window.hotkey_thread.wait()

    # Link the exit function
    app.aboutToQuit.connect(on_app_exit)
    
    # Run the app until the user kills it manually
    sys.exit(app.exec())
