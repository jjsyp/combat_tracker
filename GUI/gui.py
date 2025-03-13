import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Dict, List
import copy
import json
import os
from character.character import Character
from PIL import Image, ImageTk

class CombatTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Combat Tracker")
        
        # Set application icon
        ico_path = os.path.join(os.path.dirname(__file__), 'app.ico')
        try:
            # Load icon for window decoration
            icon_image = Image.open(ico_path)
            icon_photo = ImageTk.PhotoImage(icon_image)
            # Handle icon setting based on platform
            if os.name == 'nt':  # Windows
                self.root.iconbitmap(ico_path)
            else:  # Linux/Unix
                self.root.iconphoto(True, icon_photo)
            # Keep a reference to prevent garbage collection
            self._icon_photo = icon_photo
        except Exception as e:
            print(f"Failed to load application icon: {e}")
            
        self.characters: List[Character] = []
        self.custom_fields: List[str] = []
        self.popup_entry = None
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create main frames
        self.character_list_frame = ttk.Frame(root)
        self.character_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.character_detail_frame = ttk.Frame(root)
        self.character_detail_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Initialize UI
        self.setup_character_list()
        self.setup_character_details()
        
        # Try to load last session
        self.load_last_session()
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_menu_bar(self):
        """Create the menu bar with File options"""
        from GUI.components.menu_bar import MenuBar
        self.menu_bar = MenuBar(self.root, self)
        
    def save_session(self):
        """Save the current session to the default file"""
        try:
            # Save character data
            save_path = os.path.join('saves', 'last_session.json')
            self.save_to_file(save_path)
            
            # Update combat state
            state_path = os.path.join('saves', 'combat_state.json')
            os.makedirs(os.path.dirname(state_path), exist_ok=True)
            with open(state_path, 'w') as f:
                json.dump({'in_combat': True}, f)
                
            messagebox.showinfo("Success", "Session saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save session: {str(e)}")
    
    def save_session_as(self):
        """Save the current session to a chosen file"""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                initialdir="saves"
            )
            if file_path:
                self.save_to_file(file_path)
                messagebox.showinfo("Success", "Session saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save session: {str(e)}")
    
    def save_to_file(self, file_path):
        """Save characters to a JSON file"""
        # Create saves directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Convert characters to dictionaries
        characters_data = [char.to_dict() for char in self.characters]
        
        # Save to file
        with open(file_path, 'w') as f:
            json.dump(characters_data, f, indent=2)
    
    def load_session(self):
        """Load a session from a chosen file"""
        try:
            file_path = filedialog.askopenfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                initialdir="saves"
            )
            if file_path:
                self.load_from_file(file_path)
                messagebox.showinfo("Success", "Session loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load session: {str(e)}")
    
    def load_last_session(self):
        """Try to load the last session if it exists and we're in combat"""
        state_path = os.path.join('saves', 'combat_state.json')
        last_session_path = os.path.join('saves', 'last_session.json')
        
        try:
            # Check if we should load the last session
            if os.path.exists(state_path):
                with open(state_path, 'r') as f:
                    state = json.load(f)
                if not state.get('in_combat', True):
                    return
            
            # Load last session if it exists
            if os.path.exists(last_session_path):
                self.load_from_file(last_session_path)
        except Exception:
            # Silently fail if last session can't be loaded
            pass
    
    def load_from_file(self, file_path):
        """Load characters from a JSON file"""
        with open(file_path, 'r') as f:
            characters_data = json.load(f)
        
        # Clear current characters
        self.characters.clear()
        
        # Create new characters from data
        for char_data in characters_data:
            self.characters.append(Character.from_dict(char_data))
        
        # Update the display
        self.update_character_list()
        
    def setup_character_list(self):
        """Initialize the character list view"""
        from GUI.components.character_list import CharacterList
        self.character_list = CharacterList(self.character_list_frame, self)
        
    def update_character_list(self):
        """Update the character list display"""
        self.character_list.update_character_list(self.characters)

    def edit_custom_fields(self, item):
        """Open a dialog to edit custom fields"""
        # Get the character
        items = self.character_list.character_tree.get_children()
        char_index = items.index(item)
        char = self.characters[char_index]
        
        # Create a dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Custom Fields")
        dialog.transient(self.root)
        
        # Center the dialog on the screen
        dialog.geometry("+%d+%d" % (self.root.winfo_x() + 50,
                                   self.root.winfo_y() + 50))
        
        # Wait for the window to be drawn
        dialog.update_idletasks()
        
        # Now we can safely set the grab
        dialog.grab_set()
        
        # Create a frame for the fields
        fields_frame = ttk.Frame(dialog)
        fields_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Dictionary to store entry widgets
        entries = {}
        
        # Add existing custom fields
        row = 0
        for key, value in char.custom_fields.items():
            ttk.Label(fields_frame, text="Name:").grid(row=row, column=0, padx=2)
            name_entry = ttk.Entry(fields_frame)
            name_entry.insert(0, key)
            name_entry.grid(row=row, column=1, padx=2)
            
            ttk.Label(fields_frame, text="Value:").grid(row=row, column=2, padx=2)
            value_entry = ttk.Entry(fields_frame)
            value_entry.insert(0, value)
            value_entry.grid(row=row, column=3, padx=2)
            
            entries[row] = (name_entry, value_entry)
            row += 1
        
        # Add a blank field for new entries
        ttk.Label(fields_frame, text="Name:").grid(row=row, column=0, padx=2)
        new_name = ttk.Entry(fields_frame)
        new_name.grid(row=row, column=1, padx=2)
        
        ttk.Label(fields_frame, text="Value:").grid(row=row, column=2, padx=2)
        new_value = ttk.Entry(fields_frame)
        new_value.grid(row=row, column=3, padx=2)
        
        entries[row] = (new_name, new_value)
        
        def save_fields():
            # Clear existing custom fields
            char.custom_fields.clear()
            
            # Save all non-empty fields
            for name_entry, value_entry in entries.values():
                name = name_entry.get().strip()
                if name:  # Only save if name is not empty
                    char.custom_fields[name] = value_entry.get()
            
            self.update_character_list()
            dialog.destroy()
        
        # Add Save button
        ttk.Button(dialog, text="Save", command=save_fields).pack(pady=5)

    def setup_character_details(self):
        """Initialize the character details panel"""
        from GUI.components.character_details import CharacterDetails
        self.character_details = CharacterDetails(self.character_detail_frame, self)

    def add_character(self):
        """Proxy method to maintain backward compatibility"""
        self.character_details.add_character()

    def clear_character_details(self):
        """Proxy method to maintain backward compatibility"""
        self.character_details.clear_character_details()

    def update_character_list(self):
        # Sort characters by initiative (highest to lowest), then bonus, then name
        sorted_chars = sorted(self.characters, 
                            key=lambda x: (-x.initiative, -x.initiative_bonus, x.name.lower()))
        
        # Update the internal list to maintain sort order
        self.characters = sorted_chars
        
        # Update the character list display
        self.character_list.update_character_list(self.characters)

    def copy_character(self):
        selected = self.character_list.character_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a character to copy")
            return
        
        # Get the index of the selected item
        items = self.character_list.character_tree.get_children()
        idx = items.index(selected[0])
        char = self.characters[idx]
        
        # Create a dialog for the new name
        dialog = tk.Toplevel(self.root)
        dialog.title("Copy Character")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Make dialog modal
        dialog.focus_set()
        
        # Create and pack the frame
        frame = ttk.Frame(dialog, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Add name label and entry
        ttk.Label(frame, text="Enter name for the new character:").pack(anchor=tk.W)
        name_var = tk.StringVar(value=char.name)
        name_entry = ttk.Entry(frame, textvariable=name_var, width=40)
        name_entry.pack(fill=tk.X, pady=(5, 10))
        
        # Select the text in the entry for easy editing
        name_entry.select_range(0, tk.END)
        name_entry.focus_set()
        
        def create_copy():
            new_name = name_var.get().strip()
            if not new_name:
                messagebox.showerror("Error", "Please enter a name")
                return
            
            # Check for duplicate names
            existing_names = [c.name for c in self.characters]
            if new_name in existing_names:
                error_dialog = tk.Toplevel(dialog)
                error_dialog.title("Error")
                error_dialog.transient(dialog)  # Set dialog as parent
                error_dialog.grab_set()  # Make error dialog modal
                
                # Position error dialog relative to parent
                error_dialog.geometry("+%d+%d" % (dialog.winfo_x() + 50,
                                                 dialog.winfo_y() + 50))
                
                # Create error message
                msg_frame = ttk.Frame(error_dialog, padding="20")
                msg_frame.pack(fill=tk.BOTH, expand=True)
                
                ttk.Label(msg_frame, 
                          text=f"A character named '{new_name}' already exists.\nPlease choose a different name.",
                          wraplength=300).pack(pady=(0, 10))
                
                # Add OK button
                ttk.Button(msg_frame, 
                          text="OK", 
                          command=error_dialog.destroy).pack()
                
                # Ensure error dialog is on top
                error_dialog.lift()
                error_dialog.focus_force()
                
                # Wait for error dialog to close
                dialog.wait_window(error_dialog)
                
                name_entry.select_range(0, tk.END)  # Re-select text for easy editing
                name_entry.focus_set()
                return
            
            new_char = copy.deepcopy(char)
            new_char.name = new_name
            self.characters.append(new_char)
            self.update_character_list()
            dialog.destroy()
        
        def on_enter(event):
            create_copy()
        
        # Bind Enter key to create copy
        name_entry.bind('<Return>', on_enter)
        
        # Add buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(button_frame, text="Create Copy", command=create_copy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT)
        
        # Position dialog relative to the copy button
        dialog.update_idletasks()  # Ensure dialog is fully created
        
        # Get button position and size
        btn_pos = self.character_list.get_copy_button_position()
        
        # Get dialog size
        dialog_width = dialog.winfo_width()
        dialog_height = dialog.winfo_height()
        
        # Center dialog over button
        dialog_x = btn_pos['x'] - (dialog_width - btn_pos['width']) // 2
        dialog_y = btn_pos['y'] - dialog_height - 10  # Position above button with small gap
        
        # Get screen dimensions and ensure dialog stays within bounds
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        
        dialog_x = max(0, min(dialog_x, screen_width - dialog_width))
        dialog_y = max(0, min(dialog_y, screen_height - dialog_height))
        
        dialog.geometry(f"+{dialog_x}+{dialog_y}")

    def delete_character(self):
        selected = self.character_list.character_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a character to delete")
            return
        
        # Get the index of the selected item
        items = self.character_list.character_tree.get_children()
        idx = items.index(selected[0])
        
        self.characters.pop(idx)
        self.update_character_list()

    def end_combat(self):
        """End the current combat, clearing all characters and preventing auto-load"""
        if messagebox.askyesno("End Combat", "Are you sure you want to end combat?\nThis will remove all characters and start fresh next time."):
            # Clear all characters
            self.characters.clear()
            self.update_character_list()
            
            # Save empty state file to prevent auto-load next time
            try:
                state_path = os.path.join('saves', 'combat_state.json')
                os.makedirs(os.path.dirname(state_path), exist_ok=True)
                with open(state_path, 'w') as f:
                    json.dump({'in_combat': False}, f)
                
                # Remove last session file if it exists
                last_session_path = os.path.join('saves', 'last_session.json')
                if os.path.exists(last_session_path):
                    os.remove(last_session_path)
                    
                messagebox.showinfo("Success", "Combat ended. Starting fresh next time!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save combat state: {str(e)}")

    def add_custom_field(self, field_name=None, value=None):
        """Proxy method to maintain backward compatibility"""
        return self.character_details.add_custom_field(field_name, value)

    def on_closing(self):
        """Handle window closing event - auto save if there are characters"""
        try:
            if self.characters:  # Only save if there are characters
                # Save character data
                save_path = os.path.join('saves', 'last_session.json')
                self.save_to_file(save_path)
                
                # Update combat state
                state_path = os.path.join('saves', 'combat_state.json')
                os.makedirs(os.path.dirname(state_path), exist_ok=True)
                with open(state_path, 'w') as f:
                    json.dump({'in_combat': True}, f)
        except Exception as e:
            print(f"Failed to auto-save session: {str(e)}")
        
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CombatTrackerGUI(root)
    root.mainloop()