import os
import json
from typing import List
from tkinter import messagebox, filedialog
from character.character import Character

class SessionManager:
    def __init__(self, parent):
        """
        Initialize the session manager
        
        Args:
            parent: Parent window (main GUI) that contains character management methods
        """
        self.parent = parent
        
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
    
    def save_to_file(self, file_path: str):
        """
        Save characters to a JSON file
        
        Args:
            file_path: Path to save the file to
        """
        # Create saves directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Convert characters to dictionaries
        characters_data = [char.to_dict() for char in self.parent.characters]
        
        # Get current turn index (if combat started)
        current_turn_index = None
        combat_started = False
        if hasattr(self.parent, 'round_counter'):
            rc = self.parent.round_counter
            combat_started = getattr(rc, 'combat_started', False)
            if combat_started:
                # Find current character index
                current_name = rc.current_character.get()
                for idx, char in enumerate(self.parent.characters):
                    if getattr(char, 'name', None) == current_name:
                        current_turn_index = idx
                        break
        # Create save data with characters and round number
        save_data = {
            'characters': characters_data,
            'round': self.parent.round_counter.get_round(),
            'combat_started': combat_started,
            'current_turn_index': current_turn_index
        }
        
        # Save to file
        with open(file_path, 'w') as f:
            json.dump(save_data, f, indent=2)
    
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
    
    def load_from_file(self, file_path: str):
        """
        Load characters from a JSON file
        
        Args:
            file_path: Path to load the file from
        """
        with open(file_path, 'r') as f:
            save_data = json.load(f)
            
        # Handle legacy save files that only contain character data
        if isinstance(save_data, list):
            characters_data = save_data
            round_number = 1  # Default to round 1 for legacy saves
            combat_started = False
            current_turn_index = None
        else:
            characters_data = save_data.get('characters', [])
            round_number = save_data.get('round', 1)
            combat_started = save_data.get('combat_started', False)
            current_turn_index = save_data.get('current_turn_index', None)
        
        # Clear current characters
        self.parent.characters.clear()
        
        # Create new characters from data
        for char_data in characters_data:
            self.parent.characters.append(Character.from_dict(char_data))
        
        # Update round counter
        self.parent.round_counter.set_round(round_number)
        
        # Restore combat state and current turn
        if combat_started:
            self.parent.round_counter.combat_started = True
            self.parent.round_counter.start_combat_button.pack_forget()
            # Set current turn if valid
            if current_turn_index is not None and 0 <= current_turn_index < len(self.parent.characters):
                char = self.parent.characters[current_turn_index]
                self.parent.round_counter.set_current_character(getattr(char, 'name', str(char)))
        else:
            self.parent.round_counter.combat_started = False
            self.parent.round_counter.set_current_character("-")
            self.parent.round_counter.start_combat_button.pack(fill=tk.X, pady=(0, 10))
        
        # Update the display
        self.parent.update_character_list()

    def end_combat(self):
        """End the current combat, clearing all characters and preventing auto-load"""
        try:
            # Update combat state
            state_path = os.path.join('saves', 'combat_state.json')
            os.makedirs(os.path.dirname(state_path), exist_ok=True)
            with open(state_path, 'w') as f:
                json.dump({'in_combat': False}, f)
            
            # Clear characters and reset round
            self.parent.characters.clear()
            self.parent.round_counter.set_round(1)
            self.parent.update_character_list()
            
            # Remove last session file if it exists
            last_session_path = os.path.join('saves', 'last_session.json')
            if os.path.exists(last_session_path):
                os.remove(last_session_path)
                
            messagebox.showinfo("Success", "Combat ended. Starting fresh next time!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save combat state: {str(e)}")

    def auto_save_on_close(self):
        """Auto-save the session when closing the application"""
        try:
            if self.parent.characters:  # Only save if there are characters
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
