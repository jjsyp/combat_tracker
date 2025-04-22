import tkinter as tk
from tkinter import ttk, messagebox

class RoundCounter:
    def __init__(self, parent, gui_ref=None):
        # Main container frame
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.X, padx=5, pady=5)
        self.gui_ref = gui_ref  # Reference to main GUI for character access

        # Start Combat button
        self.start_combat_button = ttk.Button(self.frame, text="Start Combat", command=self.start_combat)
        self.start_combat_button.pack(fill=tk.X, pady=(0, 10))

        # Create round counter frame
        self.round_frame = ttk.Frame(self.frame)
        self.round_frame.pack(fill=tk.X)
        
        # Create a label for "Round:"
        self.round_label = ttk.Label(self.round_frame, text="Round:")
        self.round_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Create buttons frame for round control
        self.round_buttons_frame = ttk.Frame(self.round_frame)
        self.round_buttons_frame.pack(side=tk.LEFT)
        
        # Create decrement button
        self.decrement_button = ttk.Button(self.round_buttons_frame, text="-", width=2,
                                         command=self.decrement_round)
        self.decrement_button.pack(side=tk.LEFT)
        
        # Create a label to display the round number
        self.round_number = tk.StringVar(value="1")
        self.round_display = ttk.Label(self.round_buttons_frame, textvariable=self.round_number,
                                      width=3, anchor=tk.CENTER)
        self.round_display.pack(side=tk.LEFT, padx=3)
        
        # Create increment button
        self.increment_button = ttk.Button(self.round_buttons_frame, text="+", width=2,
                                         command=self.increment_round)
        self.increment_button.pack(side=tk.LEFT)
        
        # Create turn control frame
        self.turn_frame = ttk.Frame(self.frame)
        self.turn_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Create a label for "Turn:"
        self.turn_label = ttk.Label(self.turn_frame, text="Turn:")
        self.turn_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Create buttons frame for turn control
        self.turn_buttons_frame = ttk.Frame(self.turn_frame)
        self.turn_buttons_frame.pack(side=tk.LEFT)
        
        # Create previous turn button
        self.prev_turn_button = ttk.Button(self.turn_buttons_frame, text="Previous", width=8, command=self.previous_turn)
        self.prev_turn_button.pack(side=tk.LEFT)
        
        # Create next turn button
        self.next_turn_button = ttk.Button(self.turn_buttons_frame, text="Next", width=8, command=self.next_turn)
        self.next_turn_button.pack(side=tk.LEFT, padx=(5, 0))
        
        # Create current turn display
        self.current_turn_frame = ttk.Frame(self.turn_frame)
        self.current_turn_frame.pack(side=tk.LEFT, padx=(15, 0))
        
        # Label for "Current Turn:"
        self.current_turn_label = ttk.Label(self.current_turn_frame, text="Current Turn:")
        self.current_turn_label.pack(side=tk.LEFT)
        
        # Display current character name
        self.current_character = tk.StringVar(value="-")
        self.current_character_label = ttk.Label(self.current_turn_frame, textvariable=self.current_character)
        self.current_character_label.pack(side=tk.LEFT, padx=(5, 0))

        # Track combat state
        self.combat_started = False

        
    def set_round(self, round_num):
        """Set the round number"""
        self.round_number.set(str(round_num))

    def start_combat(self):
        """Handle start combat button press"""
        characters = []
        if self.gui_ref:
            characters = getattr(self.gui_ref, 'characters', [])
        if not characters:
            messagebox.showwarning("No Characters", "You can't start combat without characters!")
            return
        # Set current character to the first in list
        self.set_current_character(characters[0].name if hasattr(characters[0], 'name') else str(characters[0]))
        self.combat_started = True
        self.start_combat_button.pack_forget()

    def set_current_character(self, name):
        self.current_character.set(name)

    def next_turn(self):
        """Advance to the next character in the list, cycling to the top if at the end. Increment round if cycling."""
        if not self.combat_started or not self.gui_ref:
            return
        characters = getattr(self.gui_ref, 'characters', [])
        if not characters:
            return
        current_name = self.current_character.get()
        current_idx = None
        for idx, char in enumerate(characters):
            if getattr(char, 'name', None) == current_name:
                current_idx = idx
                break
        # If not found (should only happen if something is out of sync), start at the top
        if current_idx is None:
            self.set_current_character(getattr(characters[0], 'name', str(characters[0])))
            return
        # Move to next character, or cycle to top
        next_idx = (current_idx + 1) % len(characters)
        if next_idx == 0:
            self.increment_round()
        self.set_current_character(getattr(characters[next_idx], 'name', str(characters[next_idx])))

        
    def previous_turn(self):
        """Go to the previous character in the list, cycling to the bottom if at the top. Decrement round if cycling (not below 1)."""
        if not self.combat_started or not self.gui_ref:
            return
        characters = getattr(self.gui_ref, 'characters', [])
        if not characters:
            return
        current_name = self.current_character.get()
        current_idx = None
        for idx, char in enumerate(characters):
            if getattr(char, 'name', None) == current_name:
                current_idx = idx
                break
        # If not found, start at the bottom
        if current_idx is None:
            self.set_current_character(getattr(characters[-1], 'name', str(characters[-1])))
            return
        # Move to previous character, or cycle to bottom
        prev_idx = (current_idx - 1) % len(characters)
        if prev_idx == len(characters) - 1:
            self.decrement_round()
        self.set_current_character(getattr(characters[prev_idx], 'name', str(characters[prev_idx])))

    def get_round(self):
        """Get the current round number"""
        return int(self.round_number.get())
        
    def increment_round(self):
        """Increment the round number"""
        current = self.get_round()
        self.set_round(current + 1)
        
    def decrement_round(self):
        """Decrement the round number, not going below 1"""
        current = self.get_round()
        if current > 1:
            self.set_round(current - 1)
