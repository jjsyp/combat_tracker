import tkinter as tk
from tkinter import ttk, messagebox

class HealthEditDialog:
    def center_on_parent(self, parent):
        """Center the dialog on its parent window"""
        parent.update_idletasks()
        
        # Get parent geometry
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        # Calculate position
        dialog_width = self.dialog.winfo_width()
        dialog_height = self.dialog.winfo_height()
        
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        # Set position
        self.dialog.geometry(f"+{x}+{y}")
    def __init__(self, parent, character, on_edit_complete):
        """
        Initialize the health edit dialog
        
        Args:
            parent: Parent window
            character: Character whose health to edit
            on_edit_complete: Callback function to run after successful edit
        """
        # Store parameters first
        self.character = character
        self.on_edit_complete = on_edit_complete
        
        # Create and configure dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Edit Health - {character.name}")
        self.dialog.transient(parent)
        
        # Set dialog size
        self.dialog.geometry("250x150")
        self.dialog.resizable(False, False)
        
        # Configure grid
        self.dialog.grid_columnconfigure(0, weight=1)
        
        # Create widgets
        self.setup_widgets()
        
        # Wait for the window to be visible before grabbing
        self.dialog.update()
        
        # Center dialog on parent
        self.center_on_parent(parent)
        
        # Set grab after centering
        self.dialog.grab_set()
        
    def setup_widgets(self):
        """Setup the dialog widgets"""
        # Main frame to hold everything
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.grid(row=0, column=0, sticky='nsew')
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Current HP
        ttk.Label(main_frame, text="Current HP:").grid(row=0, column=0, sticky='w', padx=(0, 5), pady=(0, 5))
        self.current_hp_var = tk.StringVar(value=str(self.character.health))
        self.current_hp_entry = ttk.Entry(main_frame, textvariable=self.current_hp_var, width=8)
        self.current_hp_entry.grid(row=0, column=1, sticky='w')
        
        # Max HP
        ttk.Label(main_frame, text="Max HP:").grid(row=1, column=0, sticky='w', padx=(0, 5), pady=(0, 10))
        self.max_hp_var = tk.StringVar(value=str(self.character.maxhp))
        self.max_hp_entry = ttk.Entry(main_frame, textvariable=self.max_hp_var, width=8)
        self.max_hp_entry.grid(row=1, column=1, sticky='w')
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(5, 0))
        
        ttk.Button(button_frame, text="Save", command=self.save_changes).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Bind events
        self.dialog.bind('<Return>', lambda e: self.save_changes())
        self.dialog.bind('<Escape>', lambda e: self.dialog.destroy())
        
        # Focus current HP entry
        self.current_hp_entry.focus_set()
        self.current_hp_entry.select_range(0, tk.END)
        
    def save_changes(self):
        """Save the changes to the character"""
        try:
            current = int(self.current_hp_var.get())
            maximum = int(self.max_hp_var.get())
            
            # Validate values
            if current < 0 or maximum < 0:
                raise ValueError("Health values cannot be negative")
            if current > maximum:
                raise ValueError("Current HP cannot exceed Max HP")
                
            # Update character
            self.character.health = current
            self.character.maxhp = maximum
            
            # Call completion callback
            self.on_edit_complete()
            
            # Close dialog
            self.dialog.destroy()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e) if str(e) != "invalid literal for int() with base 10" 
                               else "Please enter valid numbers for health values")
