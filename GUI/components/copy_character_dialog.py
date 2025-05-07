import tkinter as tk
from tkinter import ttk, messagebox

class CopyCharacterDialog:
    def __init__(self, parent, character, characters, on_copy_complete):
        """
        Initialize the copy character dialog
        
        Args:
            parent: Parent window
            character: Character to copy
            characters: List of existing characters
            on_copy_complete: Callback function to run after successful copy
        """
        self.parent = parent
        self.character = character
        self.characters = characters
        self.on_copy_complete = on_copy_complete
        
        # Create dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Copy Character")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Make dialog modal
        self.dialog.focus_set()
        
        # Create and pack the frame
        self.frame = ttk.Frame(self.dialog, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Add name label and entry
        ttk.Label(self.frame, text="Enter name for the new character:").pack(anchor=tk.W)
        self.name_var = tk.StringVar(value=character.name)
        self.name_entry = ttk.Entry(self.frame, textvariable=self.name_var, width=40)
        self.name_entry.pack(fill=tk.X, pady=(5, 10))
        
        # Add copy button
        ttk.Button(self.frame, text="Copy", command=self.create_copy).pack(pady=5)
        
        # Select the text in the entry for easy editing
        self.name_entry.select_range(0, tk.END)
        self.name_entry.focus_set()
        
        # Position dialog
        self.position_dialog()
        
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
        
    def create_copy(self):
        """Create a copy of the character with the new name"""
        new_name = self.name_var.get().strip()
        if not new_name:
            messagebox.showerror("Error", "Please enter a name")
            return
        
        # Check for duplicate names
        existing_names = [c.name for c in self.characters]
        if new_name in existing_names:
            self.show_duplicate_error(new_name)
            return
            
        # Create the copy
        new_char = self.character.copy()
        new_char.name = new_name
        
        # Call the completion callback
        self.on_copy_complete(new_char)
        
        # Close the dialog
        self.dialog.destroy()
        
    def show_duplicate_error(self, name):
        """Show error dialog for duplicate name"""
        error_dialog = tk.Toplevel(self.dialog)
        error_dialog.title("Error")
        error_dialog.transient(self.dialog)  # Set dialog as parent
        error_dialog.grab_set()  # Make error dialog modal
        
        # Position error dialog relative to parent
        error_dialog.geometry("+%d+%d" % (self.dialog.winfo_x() + 50,
                                         self.dialog.winfo_y() + 50))
        
        # Create error message
        msg_frame = ttk.Frame(error_dialog, padding="20")
        msg_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(msg_frame, 
                  text=f"A character named '{name}' already exists.\nPlease choose a different name.",
                  wraplength=300).pack(pady=(0, 10))
        
        # Add OK button
        ttk.Button(msg_frame, text="OK", 
                  command=error_dialog.destroy).pack(pady=(0, 10))
