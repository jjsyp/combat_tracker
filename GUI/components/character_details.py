import tkinter as tk
from tkinter import ttk, messagebox
from character.character import Character

class CharacterDetails:
    def __init__(self, parent_frame, parent):
        """
        Initialize the character details component
        
        Args:
            parent_frame: Frame to place the character details in
            parent: Parent window (main GUI) that contains character management methods
        """
        self.parent_frame = parent_frame
        self.parent = parent
        self.setup_character_details()
        
    def setup_character_details(self):
        """Initialize the character details panel"""
        # Name Entry
        ttk.Label(self.parent_frame, text="Name:").pack(anchor=tk.W)
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(self.parent_frame, textvariable=self.name_var)
        self.name_entry.pack(fill=tk.X, pady=(0, 10))
        self.name_entry.bind('<Return>', lambda e: self.add_character())
        
        # Initiative Entry
        ttk.Label(self.parent_frame, text="Initiative:").pack(anchor=tk.W)
        self.initiative_var = tk.StringVar()
        self.initiative_entry = ttk.Entry(self.parent_frame, textvariable=self.initiative_var)
        self.initiative_entry.pack(fill=tk.X, pady=(0, 10))
        self.initiative_entry.bind('<Return>', lambda e: self.add_character())
        
        # Initiative Bonus
        ttk.Label(self.parent_frame, text="Initiative Bonus:").pack(anchor=tk.W)
        self.bonus_var = tk.StringVar(value='0')
        self.bonus_entry = ttk.Entry(self.parent_frame, textvariable=self.bonus_var)
        self.bonus_entry.pack(fill=tk.X, pady=(0, 10))
        self.bonus_entry.bind('<Return>', lambda e: self.add_character())
        
        # Health Frame
        health_frame = ttk.Frame(self.parent_frame)
        health_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(health_frame, text="Health:").pack(side=tk.LEFT)
        self.health_var = tk.StringVar()
        self.health_entry = ttk.Entry(health_frame, textvariable=self.health_var, width=8)
        self.health_entry.pack(side=tk.LEFT, padx=5)
        self.health_entry.bind('<Return>', lambda e: self.add_character())
        
        # AC Entry
        ttk.Label(self.parent_frame, text="Armor Class:").pack(anchor=tk.W)
        self.ac_var = tk.StringVar()
        self.ac_entry = ttk.Entry(self.parent_frame, textvariable=self.ac_var)
        self.ac_entry.pack(fill=tk.X, pady=(0, 10))
        self.ac_entry.bind('<Return>', lambda e: self.add_character())
        
        # Custom Fields Frame
        custom_frame = ttk.LabelFrame(self.parent_frame, text="Custom Fields")
        custom_frame.pack(fill=tk.X, pady=5)  # Changed to fill=tk.X so it doesn't try to expand vertically
        
        # Frame to hold custom fields that will grow vertically
        self.custom_fields_frame = ttk.Frame(custom_frame, height=20)
        self.custom_fields_frame.pack(fill=tk.X, padx=5, pady=5)  # Changed to fill=tk.X to match parent
        
        # Button Frame to keep buttons together
        button_frame = ttk.Frame(custom_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        # Add Custom Field Button
        ttk.Button(button_frame, text="Add Custom Field", 
                  command=self.add_custom_field).pack()
        
        # Add Character Button
        ttk.Button(self.parent_frame, text="Add Character", 
                  command=self.add_character).pack(fill=tk.X, pady=10)

    def add_character(self, event=None):
        """Add a new character with the current field values"""
        try:
            # Create a new character with the current field values
            name = self.name_var.get()
            if not name.strip():
                messagebox.showerror("Error", "Please enter a name for the character")
                return
                
            char = Character(
                name=name,
                initiative=int(self.initiative_var.get() or 0),
                initiative_bonus=int(self.bonus_var.get() or 0),
                health=int(self.health_var.get() or 0),
                ac=int(self.ac_var.get() or 0)
            )
            
            # Add custom fields
            for frame in self.custom_fields_frame.winfo_children():
                entries = [w for w in frame.winfo_children() if isinstance(w, ttk.Entry)]
                if len(entries) == 2:
                    field_name = entries[0].get().strip()
                    if field_name:  # Only add if field name is not empty
                        char.custom_fields[field_name] = entries[1].get()
            
            # Add to character list and update display
            self.parent.characters.append(char)
            self.parent.update_character_list()
            
            # Clear the form for the next character
            self.clear_character_details()
            
        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid numbers for Initiative, Health, and AC")

    def clear_character_details(self):
        """Clear all fields in the character details panel"""
        self.name_var.set("")
        self.initiative_var.set("")
        self.bonus_var.set("0")
        self.health_var.set("")
        self.ac_var.set("")
        
        for widget in self.custom_fields_frame.winfo_children():
            widget.destroy()
            
        # Reset custom fields frame size
        self.custom_fields_frame.configure(height=20)

    def add_custom_field(self, field_name=None, value=None):
        """Add a new custom field to the form"""
        frame = ttk.Frame(self.custom_fields_frame)
        frame.pack(fill=tk.X, pady=2)
        
        # Name entry
        ttk.Label(frame, text="Name:").pack(side=tk.LEFT, padx=2)
        name_entry = ttk.Entry(frame, width=10)
        if field_name:
            name_entry.insert(0, field_name)
        name_entry.pack(side=tk.LEFT, padx=2)
        
        # Value entry
        ttk.Label(frame, text="Value:").pack(side=tk.LEFT, padx=2)
        value_entry = ttk.Entry(frame, width=4)
        if value:
            value_entry.insert(0, value)
        value_entry.pack(side=tk.LEFT, padx=2)
        
        # Delete button
        ttk.Button(frame, text="X", width=2,
                  command=lambda: frame.destroy()).pack(side=tk.RIGHT, padx=2)
