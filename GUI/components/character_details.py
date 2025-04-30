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
        self.template_mode = False
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
        
        # Health/Max HP Frame
        health_frame = ttk.Frame(self.parent_frame)
        health_frame.pack(fill=tk.X, pady=(0, 10))
        
        # In template mode, show Max HP. In normal mode, show Health
        self.health_label = ttk.Label(health_frame, text="Health:")
        self.max_hp_label = ttk.Label(health_frame, text="Max HP:")
        
        # Only one will be visible based on mode
        self.health_var = tk.StringVar()
        self.health_entry = ttk.Entry(health_frame, textvariable=self.health_var, width=8)
        self.health_entry.bind('<Return>', lambda e: self.add_character())
        
        # Configure initial state
        if hasattr(self, 'template_mode') and self.template_mode:
            self.max_hp_label.pack(side=tk.LEFT)
            self.health_entry.pack(side=tk.LEFT, padx=5)
        else:
            self.health_label.pack(side=tk.LEFT)
            self.health_entry.pack(side=tk.LEFT, padx=5)
        
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
                
            health_value = int(self.health_var.get() or 0)
            char = Character(
                name=name,
                initiative=int(self.initiative_var.get() or 0),
                initiative_bonus=int(self.bonus_var.get() or 0),
                health=health_value,
                maxhp=health_value,  # In template mode, health value is max HP
                ac=int(self.ac_var.get() or 0)
            )
            
            # Add custom fields
            for frame in self.custom_fields_frame.winfo_children():
                entries = [w for w in frame.winfo_children() if isinstance(w, ttk.Entry)]
                if len(entries) == 2:
                    field_name = entries[0].get().strip()
                    if field_name:  # Only add if field name is not empty
                        char.custom_fields[field_name] = entries[1].get()
            
            # Add character through parent's add_character method
            self.parent.add_character(char)
            
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
        
    def set_template_mode(self, enabled):
        """Enable or disable template mode"""
        self.template_mode = enabled
        if enabled:
            # Switch to Max HP label
            self.health_label.pack_forget()
            self.max_hp_label.pack(side=tk.LEFT)
            
            # Hide initiative fields
            for widget in self.parent_frame.winfo_children():
                if isinstance(widget, ttk.Label) and widget.cget("text") in ["Initiative:", "Initiative Bonus:"]:
                    widget.pack_forget()
                    
            self.initiative_entry.pack_forget()
            self.bonus_entry.pack_forget()
        else:
            # Switch back to Health label
            self.max_hp_label.pack_forget()
            self.health_label.pack(side=tk.LEFT)
            
            # Show initiative fields
            for i, (label_text, entry) in enumerate([
                ("Initiative:", self.initiative_entry),
                ("Initiative Bonus:", self.bonus_entry)
            ]):
                # Find or create label
                label = None
                for widget in self.parent_frame.winfo_children():
                    if isinstance(widget, ttk.Label) and widget.cget("text") == label_text:
                        label = widget
                        break
                if not label:
                    label = ttk.Label(self.parent_frame, text=label_text)
                
                # Pack label and entry in order
                label.pack(anchor=tk.W)
                entry.pack(fill=tk.X, pady=(0, 10))
        
    def show_template(self, template):
        """Show template data in the form"""
        self.name_var.set(template.name)
        self.initiative_var.set(str(template.initiative))
        self.bonus_var.set(str(template.initiative_bonus))
        self.health_var.set(str(template.maxhp))
        self.ac_var.set(str(template.ac))
        
        # Clear existing custom fields
        for widget in self.custom_fields_frame.winfo_children():
            widget.destroy()
            
        # Add template's custom fields
        for field_name, value in template.custom_fields.items():
            self.add_custom_field(field_name, value)

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
        name_entry.bind('<Return>', lambda e: self.add_character())
        
        # Value entry
        ttk.Label(frame, text="Value:").pack(side=tk.LEFT, padx=2)
        value_entry = ttk.Entry(frame, width=4)
        if value:
            value_entry.insert(0, value)
        value_entry.pack(side=tk.LEFT, padx=2)
        value_entry.bind('<Return>', lambda e: self.add_character())
        
        # Delete button
        ttk.Button(frame, text="X", width=2,
                  command=lambda: frame.destroy()).pack(side=tk.RIGHT, padx=2)
