import tkinter as tk
from tkinter import ttk

class QuickEdit:
    def __init__(self, parent_frame, parent):
        """
        Initialize the quick edit component
        
        Args:
            parent_frame: Frame to place the quick edit panel in
            parent: Parent window (main GUI) that contains character management methods
        """
        self.parent_frame = parent_frame
        self.parent = parent
        self.setup_quick_edit()
        
    def setup_quick_edit(self):
        """Initialize the quick edit panel"""
        # Name section
        ttk.Label(self.parent_frame, text="Name:").pack(anchor=tk.W)
        self.name_label = ttk.Label(self.parent_frame, text="", font=('TkDefaultFont', 12))
        self.name_label.pack(fill=tk.X, pady=(0, 10))
        
        # Add placeholder sections to maintain size
        for section in ["Health", "Initiative", "Armor Class", "Custom Fields"]:
            frame = ttk.LabelFrame(self.parent_frame, text=section)
            frame.pack(fill=tk.X, pady=5)
            # Add some padding inside to maintain height
            ttk.Frame(frame, height=30).pack(pady=5)

    def show_character(self, character):
        """Update the quick edit panel with the selected character"""
        if character:
            self.name_label.config(text=character.name)
        else:
            self.name_label.config(text="")
