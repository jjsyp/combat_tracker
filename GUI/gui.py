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

    def create_menu_bar(self):
        """Create the menu bar with File options"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self.save_session)
        file_menu.add_command(label="Save As...", command=self.save_session_as)
        file_menu.add_command(label="Load...", command=self.load_session)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
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
        # Character List Label
        ttk.Label(self.character_list_frame, text="Characters").pack()
        
        # Create Treeview
        self.character_tree = ttk.Treeview(self.character_list_frame)
        self.character_tree.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.character_list_frame, orient="vertical", command=self.character_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.character_tree.configure(yscrollcommand=scrollbar.set)
        
        # Configure columns
        self.character_tree['columns'] = ('name', 'initiative', 'health', 'ac', 'custom_fields')
        
        # Format columns
        self.character_tree.column('#0', width=0, stretch=tk.NO)  # Hidden ID column
        self.character_tree.column('name', anchor=tk.W, width=120)
        self.character_tree.column('initiative', anchor=tk.CENTER, width=60)
        self.character_tree.column('health', anchor=tk.CENTER, width=60)
        self.character_tree.column('ac', anchor=tk.CENTER, width=60)
        self.character_tree.column('custom_fields', anchor=tk.W, width=200)
        
        # Create headings
        self.character_tree.heading('#0', text='', anchor=tk.W)
        self.character_tree.heading('name', text='Name', anchor=tk.W)
        self.character_tree.heading('initiative', text='Initiative', anchor=tk.CENTER)
        self.character_tree.heading('health', text='Health', anchor=tk.CENTER)
        self.character_tree.heading('ac', text='AC', anchor=tk.CENTER)
        self.character_tree.heading('custom_fields', text='Custom Fields', anchor=tk.W)
        
        # Bind double-click event
        self.character_tree.bind('<Double-1>', self.on_double_click)
        
        # Buttons Frame
        btn_frame = ttk.Frame(self.character_list_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        self.copy_button = ttk.Button(btn_frame, text="Copy Character", command=self.copy_character)
        self.copy_button.pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Delete", command=self.delete_character).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="End Combat", command=self.end_combat).pack(side=tk.LEFT, padx=2)

    def get_cell_bbox(self, item, column):
        """Get the bounding box for a cell"""
        bbox = self.character_tree.bbox(item, column)
        if not bbox:
            return None
        return bbox

    def on_double_click(self, event):
        """Handle double-click on tree item"""
        region = self.character_tree.identify_region(event.x, event.y)
        if region != "cell":
            return
        
        # Get the item and column that was clicked
        item = self.character_tree.identify_row(event.y)
        column = self.character_tree.identify_column(event.x)
        
        if not item or not column:
            return
            
        # Get column name from column number
        column_name = self.character_tree['columns'][int(column[1]) - 1]
        
        # Don't edit custom fields directly
        if column_name == 'custom_fields':
            self.edit_custom_fields(item)
            return
            
        # Get the current value
        current_value = self.character_tree.item(item)['values'][int(column[1]) - 1]
        
        # Create and position the entry widget
        self.start_edit(item, column, column_name, str(current_value))

    def start_edit(self, item, column, column_name, current_value):
        """Start editing a cell"""
        # Cancel any existing edit
        self.cancel_edit()
        
        # Get cell bbox
        bbox = self.get_cell_bbox(item, column)
        if not bbox:
            return
        
        # Create entry widget
        self.popup_entry = ttk.Entry(self.character_tree)
        self.popup_entry.insert(0, current_value)
        self.popup_entry.select_range(0, tk.END)
        
        # Position the entry widget
        self.popup_entry.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])
        
        # Give focus to the entry
        self.popup_entry.focus_set()
        
        # Bind events
        self.popup_entry.bind('<Return>', lambda e: self.finish_edit(item, column_name))
        self.popup_entry.bind('<Escape>', lambda e: self.cancel_edit())
        self.popup_entry.bind('<FocusOut>', lambda e: self.cancel_edit())

    def finish_edit(self, item, column_name):
        """Save the edited value"""
        if not self.popup_entry:
            return
            
        # Get the new value
        new_value = self.popup_entry.get()
        
        # Get the character index
        items = self.character_tree.get_children()
        char_index = items.index(item)
        char = self.characters[char_index]
        
        try:
            # Update the character attribute based on column
            if column_name == 'name':
                char.name = new_value
            elif column_name == 'initiative':
                char.initiative = int(new_value)
            elif column_name == 'health':
                char.health = int(new_value)
            elif column_name == 'ac':
                char.ac = int(new_value)
                
            # Update the display
            self.update_character_list()
            
        except ValueError:
            messagebox.showerror("Error", f"Invalid value for {column_name}")
        
        self.cancel_edit()

    def cancel_edit(self):
        """Cancel the current edit"""
        if self.popup_entry:
            self.popup_entry.destroy()
            self.popup_entry = None

    def edit_custom_fields(self, item):
        """Open a dialog to edit custom fields"""
        # Get the character
        items = self.character_tree.get_children()
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
        # Name Entry
        ttk.Label(self.character_detail_frame, text="Name:").pack(anchor=tk.W)
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(self.character_detail_frame, textvariable=self.name_var)
        self.name_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Initiative Entry
        ttk.Label(self.character_detail_frame, text="Initiative:").pack(anchor=tk.W)
        self.initiative_var = tk.StringVar()
        self.initiative_entry = ttk.Entry(self.character_detail_frame, textvariable=self.initiative_var)
        self.initiative_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Health Frame
        health_frame = ttk.Frame(self.character_detail_frame)
        health_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(health_frame, text="Health:").pack(side=tk.LEFT)
        self.health_var = tk.StringVar()
        self.health_entry = ttk.Entry(health_frame, textvariable=self.health_var, width=8)
        self.health_entry.pack(side=tk.LEFT, padx=5)
        
        # AC Entry
        ttk.Label(self.character_detail_frame, text="Armor Class:").pack(anchor=tk.W)
        self.ac_var = tk.StringVar()
        self.ac_entry = ttk.Entry(self.character_detail_frame, textvariable=self.ac_var)
        self.ac_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Custom Fields Frame
        custom_frame = ttk.LabelFrame(self.character_detail_frame, text="Custom Fields")
        custom_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.custom_fields_frame = ttk.Frame(custom_frame)
        self.custom_fields_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add Custom Field Button
        ttk.Button(custom_frame, text="Add Custom Field", 
                  command=self.add_custom_field).pack(pady=5)
        
        # Add Character Button
        ttk.Button(self.character_detail_frame, text="Add Character", 
                  command=self.add_character).pack(fill=tk.X, pady=10)

    def add_character(self):
        try:
            # Create a new character with the current field values
            name = self.name_var.get()
            if not name.strip():
                messagebox.showerror("Error", "Please enter a name for the character")
                return
                
            char = Character(
                name=name,
                initiative=int(self.initiative_var.get() or 0),
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
            self.characters.append(char)
            self.update_character_list()
            
            # Clear the form for the next character
            self.clear_character_details()
            
            
        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid numbers for Initiative, Health, and AC")

    def clear_character_details(self):
        self.name_var.set("")
        self.initiative_var.set("")
        self.health_var.set("")
        self.ac_var.set("")
        
        for widget in self.custom_fields_frame.winfo_children():
            widget.destroy()

    def update_character_list(self):
        # Clear the tree
        for item in self.character_tree.get_children():
            self.character_tree.delete(item)
        
        # Add characters sorted by initiative
        for char in sorted(self.characters, key=lambda x: (-x.initiative, x.name)):
            # Format custom fields as a string
            custom_fields_str = ', '.join(f"{k}: {v}" for k, v in char.custom_fields.items())
            
            self.character_tree.insert(
                parent='',
                index='end',
                values=(
                    char.name,
                    char.initiative,
                    char.health,
                    char.ac,
                    custom_fields_str
                )
            )

    def copy_character(self):
        selected = self.character_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a character to copy")
            return
        
        # Get the index of the selected item
        items = self.character_tree.get_children()
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
        
        # Get button position relative to root window
        x = self.copy_button.winfo_rootx()
        y = self.copy_button.winfo_rooty()
        
        # Center dialog over button
        dialog_width = dialog.winfo_width()
        dialog_height = dialog.winfo_height()
        button_width = self.copy_button.winfo_width()
        button_height = self.copy_button.winfo_height()
        
        dialog_x = x - (dialog_width - button_width) // 2
        dialog_y = y - dialog_height - 10  # Position above button with small gap
        
        # Ensure dialog stays within screen bounds
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        
        dialog_x = max(0, min(dialog_x, screen_width - dialog_width))
        dialog_y = max(0, min(dialog_y, screen_height - dialog_height))
        
        dialog.geometry(f"+{dialog_x}+{dialog_y}")

    def delete_character(self):
        selected = self.character_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a character to delete")
            return
        
        # Get the index of the selected item
        items = self.character_tree.get_children()
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
        frame = ttk.Frame(self.custom_fields_frame)
        frame.pack(fill=tk.X, pady=2)
        
        name_var = tk.StringVar(value=field_name or "")
        value_var = tk.StringVar(value=value or "")
        
        name_entry = ttk.Entry(frame, textvariable=name_var, width=15)
        name_entry.pack(side=tk.LEFT, padx=2)
        
        value_entry = ttk.Entry(frame, textvariable=value_var)
        value_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        ttk.Button(frame, text="X", width=3,
                  command=lambda: frame.destroy()).pack(side=tk.RIGHT, padx=2)
        
        return frame, name_entry, value_entry

if __name__ == "__main__":
    root = tk.Tk()
    app = CombatTrackerGUI(root)
    root.mainloop()