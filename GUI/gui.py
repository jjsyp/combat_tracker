import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Dict, List
import copy
import json
import os
from character.character import Character
from PIL import Image, ImageTk
from GUI.components.quick_edit import QuickEdit

class CombatTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.characters: List[Character] = []
        self.custom_fields: List[str] = []
        self.popup_entry = None
        self.current_round = 1
        
        # Initialize app configuration
        from GUI.components.app_config import AppConfig
        self.app_config = AppConfig(root)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Store frame references
        self.character_list_frame = self.app_config.list_frame
        self.character_detail_frame = self.app_config.detail_frame
        
        # Initialize UI
        self.setup_round_counter()
        self.setup_character_list()
        self.setup_character_details()
        
        # Initialize session manager
        from GUI.components.session_manager import SessionManager
        self.session_manager = SessionManager(self)
        
        # Try to load last session
        self.load_last_session()
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_menu_bar(self):
        """Create the menu bar with File options"""
        from GUI.components.menu_bar import MenuBar
        self.menu_bar = MenuBar(self.root, self)
        
    def save_session(self):
        """Proxy method to maintain backward compatibility"""
        self.session_manager.save_session()
    
    def save_session_as(self):
        """Proxy method to maintain backward compatibility"""
        self.session_manager.save_session_as()
    
    def save_to_file(self, file_path):
        """Proxy method to maintain backward compatibility"""
        self.session_manager.save_to_file(file_path)
    
    def load_session(self):
        """Proxy method to maintain backward compatibility"""
        self.session_manager.load_session()
    
    def load_last_session(self):
        """Proxy method to maintain backward compatibility"""
        self.session_manager.load_last_session()
    
    def load_from_file(self, file_path):
        """Proxy method to maintain backward compatibility"""
        self.session_manager.load_from_file(file_path)
        
    def setup_round_counter(self):
        """Initialize the round counter"""
        from GUI.components.round_counter import RoundCounter
        self.round_counter = RoundCounter(self.character_list_frame, gui_ref=self)

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
        
        # Create and show the dialog
        from GUI.components.custom_fields_dialog import CustomFieldsDialog
        CustomFieldsDialog(self.root, char, self.character_list, self)

    def setup_character_details(self):
        """Initialize the character details panel"""
        # Create a frame for character details
        self.details_frame = ttk.Frame(self.character_detail_frame)
        self.details_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create a frame for quick edit
        self.quick_edit_frame = ttk.Frame(self.character_detail_frame)
        
        # Initialize both panels
        from GUI.components.character_details import CharacterDetails
        self.character_details = CharacterDetails(self.details_frame, self)
        self.quick_edit = QuickEdit(self.quick_edit_frame, self)
        
        # Start with character details visible
        self.show_character_details()

    def add_character(self, char=None):
        """Add a character to the combat tracker
        
        Args:
            char: Optional Character instance. If not provided, creates a new character
                 using the character details panel.
        """
        if char is None:
            # Proxy to character details panel for backward compatibility
            self.character_details.add_character()
        else:
            # Add provided character to the list
            self.characters.append(char)
            self.update_character_list()

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
        
        def on_copy_complete(new_char):
            self.characters.append(new_char)
            self.update_character_list()
        
        # Create and show the dialog
        from GUI.components.copy_character_dialog import CopyCharacterDialog
        CopyCharacterDialog(self.root, char, self.characters, on_copy_complete)

    def delete_character(self):
        selected = self.character_list.character_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a character to delete")
            return
        
        # Get the index of the selected item
        items = self.character_list.character_tree.get_children()
        idx = items.index(selected[0])
        
        deleted_char = self.characters.pop(idx)
        # If the deleted character was the current turn, advance turn or clear
        if hasattr(self.round_counter, "current_character"):
            current_name = self.round_counter.current_character.get()
            if current_name == getattr(deleted_char, 'name', str(deleted_char)):
                if self.characters:
                    # If we're deleting the last character in turn order, increment round
                    if idx == len(self.characters):
                        self.round_counter.increment_round()
                    self.round_counter.set_current_character(getattr(self.characters[0], 'name', str(self.characters[0])))
                else:
                    self.round_counter.set_current_character("-")
        self.update_character_list()

    def end_combat(self):
        """End the current combat, clearing all characters and preventing auto-load"""
        if messagebox.askyesno("End Combat", "Are you sure you want to end combat?\nThis will remove all characters and start fresh next time."):
            self.session_manager.end_combat()

    def add_custom_field(self, field_name=None, value=None):
        """Proxy method to maintain backward compatibility"""
        return self.character_details.add_custom_field(field_name, value)

    def show_character_details(self):
        """Show the character details panel"""
        self.quick_edit_frame.pack_forget()
        self.details_frame.pack(fill=tk.BOTH, expand=True)
        
    def show_quick_edit(self):
        """Show the quick edit panel"""
        self.details_frame.pack_forget()
        self.quick_edit_frame.pack(fill=tk.BOTH, expand=True)
        
    def on_character_selected(self, character):
        """Handle character selection"""
        if character:
            self.show_quick_edit()
            self.quick_edit.show_character(character)
        else:
            self.show_character_details()
            
    def on_closing(self):
        """Handle window closing event"""
        self.session_manager.auto_save_on_close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CombatTrackerGUI(root)
    root.mainloop()