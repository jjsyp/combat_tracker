import tkinter as tk
from tkinter import ttk

class RoundCounter:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Create a label for "Round:"
        self.round_label = ttk.Label(self.frame, text="Round:")
        self.round_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Create a label to display the round number
        self.round_number = tk.StringVar(value="1")
        self.round_display = ttk.Label(self.frame, textvariable=self.round_number)
        self.round_display.pack(side=tk.LEFT)
