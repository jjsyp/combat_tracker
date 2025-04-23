import tkinter as tk
from tkinter import ttk, messagebox

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
        self.current_character = None
        self.setup_quick_edit()
        
    def setup_quick_edit(self):
        """Initialize the quick edit panel"""
        # Name section
        ttk.Label(self.parent_frame, text="Name:").pack(anchor=tk.W)
        self.name_label = ttk.Label(self.parent_frame, text="", font=('TkDefaultFont', 12))
        self.name_label.pack(fill=tk.X, pady=(0, 10))
        
        # Health section
        self.health_frame = ttk.LabelFrame(self.parent_frame, text="Health")
        self.health_frame.pack(fill=tk.X, pady=5)
        
        # Current / Max HP display
        hp_display = ttk.Frame(self.health_frame)
        hp_display.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(hp_display, text="Current HP:").pack(side=tk.LEFT, padx=(0, 5))
        self.current_hp_label = ttk.Label(hp_display, text="-")
        self.current_hp_label.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Label(hp_display, text="Max HP:").pack(side=tk.LEFT, padx=(0, 5))
        self.max_hp_label = ttk.Label(hp_display, text="-")
        self.max_hp_label.pack(side=tk.LEFT)
        
        # Health modification section
        mod_frame = ttk.Frame(self.parent_frame)
        mod_frame.pack(fill=tk.X, pady=10)
        
        # Input field
        ttk.Label(mod_frame, text="Amount:").pack(anchor=tk.W)
        self.health_mod_var = tk.StringVar()
        self.health_mod_entry = ttk.Entry(mod_frame, textvariable=self.health_mod_var)
        self.health_mod_entry.pack(fill=tk.X, pady=(0, 5))
        
        # Buttons frame
        btn_frame = ttk.Frame(mod_frame)
        btn_frame.pack(fill=tk.X)
        
        # Heal and Damage buttons
        ttk.Button(btn_frame, text="Heal", command=self.heal).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Damage", command=self.damage).pack(side=tk.LEFT)
        
        # Add some padding at the bottom to maintain spacing
        ttk.Frame(self.parent_frame, height=30).pack(pady=5, fill=tk.X)

    def show_character(self, character):
        """Update the quick edit panel with the selected character"""
        self.current_character = character
        if character:
            self.name_label.config(text=character.name)
            self.current_hp_label.config(text=str(character.health))
            self.max_hp_label.config(text=str(character.maxhp))
        else:
            self.name_label.config(text="")
            self.current_hp_label.config(text="-")
            self.max_hp_label.config(text="-")
            self.health_mod_var.set("")
            
    def _validate_amount(self):
        """Validate and get the health modification amount"""
        try:
            amount = int(self.health_mod_var.get())
            if amount < 0:
                raise ValueError("Amount must be positive")
            return amount
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e) if str(e) != "invalid literal for int() with base 10: ''" else "Please enter a number")
            return None
            
    def _update_health(self, new_health):
        """Update character's health and display"""
        self.current_character.health = new_health
        self.current_hp_label.config(text=str(new_health))
        self.health_mod_var.set("")  # Clear the input field
        
        # Store the character's name before update
        char_name = self.current_character.name
        
        # Update the list
        self.parent.update_character_list()
        
        # Find and select the character by name in the updated list
        tree = self.parent.character_list.character_tree
        for item in tree.get_children():
            values = tree.item(item)['values']
            if values and values[0] == char_name:  # values[0] is the name column
                self.parent.character_list.suppress_selection_event = True
                tree.selection_set(item)
                self.parent.character_list.suppress_selection_event = False
                break
            
    def heal(self):
        """Heal the character by the specified amount"""
        if not self.current_character:
            return
            
        amount = self._validate_amount()
        if amount is None:
            return
            
        # Calculate new health, capped at max HP
        new_health = min(self.current_character.health + amount, self.current_character.maxhp)
        self._update_health(new_health)
        
    def damage(self):
        """Damage the character by the specified amount"""
        if not self.current_character:
            return
            
        amount = self._validate_amount()
        if amount is None:
            return
            
        # Calculate new health, minimum of 0
        new_health = max(self.current_character.health - amount, 0)
        self._update_health(new_health)
