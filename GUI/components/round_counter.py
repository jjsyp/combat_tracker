import tkinter as tk
from tkinter import ttk

class RoundCounter:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Create a label for "Round:"
        self.round_label = ttk.Label(self.frame, text="Round:")
        self.round_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Create buttons frame
        self.buttons_frame = ttk.Frame(self.frame)
        self.buttons_frame.pack(side=tk.LEFT)
        
        # Create decrement button
        self.decrement_button = ttk.Button(self.buttons_frame, text="-", width=2,
                                         command=self.decrement_round)
        self.decrement_button.pack(side=tk.LEFT)
        
        # Create a label to display the round number
        self.round_number = tk.StringVar(value="1")
        self.round_display = ttk.Label(self.buttons_frame, textvariable=self.round_number,
                                      width=3, anchor=tk.CENTER)
        self.round_display.pack(side=tk.LEFT, padx=3)
        
        # Create increment button
        self.increment_button = ttk.Button(self.buttons_frame, text="+", width=2,
                                         command=self.increment_round)
        self.increment_button.pack(side=tk.LEFT)
        
    def set_round(self, round_num):
        """Set the round number"""
        self.round_number.set(str(round_num))
        
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
