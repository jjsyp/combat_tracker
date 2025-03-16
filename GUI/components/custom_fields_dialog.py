import tkinter as tk
from tkinter import ttk, messagebox

class CustomFieldsDialog:
    def __init__(self, parent, character, character_list, main_gui):
        """
        Initialize the custom fields dialog
        
        Args:
            parent: Parent window
            character: Character whose custom fields to edit
            character_list: Reference to the character list component for updates
            main_gui: Reference to the main GUI for character list access
        """
        self.parent = parent
        self.character = character
        self.character_list = character_list
        self.main_gui = main_gui
        self.entries = {}
        
        # Create dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Custom Fields")
        self.dialog.transient(parent)
        
        # Create a frame for the fields
        self.fields_frame = ttk.Frame(self.dialog)
        self.fields_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add existing custom fields
        self.setup_fields()
        
        # Add buttons
        self.setup_buttons()
        
        # Position the dialog
        self.position_dialog()
        
        # Wait for the window to be drawn
        self.dialog.update_idletasks()
        
        # Now we can safely set the grab
        self.dialog.grab_set()
        
    def setup_fields(self):
        """Set up the custom fields display"""
        row = 0
        for key, value in self.character.custom_fields.items():
            ttk.Label(self.fields_frame, text="Name:").grid(row=row, column=0, padx=2)
            name_entry = ttk.Entry(self.fields_frame)
            name_entry.insert(0, key)
            name_entry.grid(row=row, column=1, padx=2)
            
            ttk.Label(self.fields_frame, text="Value:").grid(row=row, column=2, padx=2)
            value_entry = ttk.Entry(self.fields_frame)
            value_entry.insert(0, value)
            value_entry.grid(row=row, column=3, padx=2)
            
            # Store entries for later access
            self.entries[row] = (name_entry, value_entry)
            row += 1
            
    def setup_buttons(self):
        """Set up the dialog buttons"""
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="Add Field", 
                  command=self.add_field).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save", 
                  command=self.save_fields).pack(side=tk.RIGHT, padx=5)
                  
    def position_dialog(self):
        """Position the dialog relative to the parent window"""
        # Get parent window position and size
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        # Get dialog size
        dialog_width = self.dialog.winfo_reqwidth()
        dialog_height = self.dialog.winfo_reqheight()
        
        # Calculate position (centered over parent)
        dialog_x = parent_x + (parent_width - dialog_width) // 2
        dialog_y = parent_y + (parent_height - dialog_height) // 2
        
        # Get screen dimensions and ensure dialog stays within bounds
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()
        
        dialog_x = max(0, min(dialog_x, screen_width - dialog_width))
        dialog_y = max(0, min(dialog_y, screen_height - dialog_height))
        
        self.dialog.geometry(f"+{dialog_x}+{dialog_y}")
        
    def add_field(self):
        """Add a new empty field to the dialog"""
        row = len(self.entries)
        
        ttk.Label(self.fields_frame, text="Name:").grid(row=row, column=0, padx=2)
        name_entry = ttk.Entry(self.fields_frame)
        name_entry.grid(row=row, column=1, padx=2)
        
        ttk.Label(self.fields_frame, text="Value:").grid(row=row, column=2, padx=2)
        value_entry = ttk.Entry(self.fields_frame)
        value_entry.grid(row=row, column=3, padx=2)
        
        self.entries[row] = (name_entry, value_entry)
        
    def save_fields(self):
        """Save the custom fields back to the character"""
        # Clear existing custom fields
        self.character.custom_fields.clear()
        
        # Add all non-empty fields
        for name_entry, value_entry in self.entries.values():
            field_name = name_entry.get().strip()
            if field_name:  # Only add if field name is not empty
                self.character.custom_fields[field_name] = value_entry.get()
        
        # Update the display with main GUI's character list
        self.character_list.update_character_list(self.main_gui.characters)
        
        # Close the dialog
        self.dialog.destroy()
