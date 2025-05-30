import tkinter as tk
from tkinter import ttk, messagebox

class CharacterList:
    def __init__(self, parent_frame, parent):
        """
        Initialize the character list component
        
        Args:
            parent_frame: Frame to place the character list in
            parent: Parent window (main GUI) that contains character management methods
        """
        self.parent_frame = parent_frame
        self.parent = parent
        self.popup_entry = None
        self.round_counter = getattr(parent, 'round_counter', None)
        self.suppress_selection_event = False
        
        # Set up trace on current character if available
        if self.round_counter and hasattr(self.round_counter, 'current_character'):
            self.round_counter.current_character.trace_add('write', self._on_current_character_change)
            
        self.setup_character_list()
        
    def setup_character_list(self):
        """Initialize the character list view"""
        # Character List Label
        ttk.Label(self.parent_frame, text="Characters").pack()
        
        # Create bold style for current character
        self.style = ttk.Style()
        self.style.configure('Bold.Treeview.Item', font=('TkDefaultFont', 12, 'bold'))
        
        # Create Treeview
        self.character_tree = ttk.Treeview(self.parent_frame)

        
        # Add vertical scrollbar
        y_scrollbar = ttk.Scrollbar(self.parent_frame, orient="vertical", command=self.character_tree.yview)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add horizontal scrollbar
        x_scrollbar = ttk.Scrollbar(self.parent_frame, orient="horizontal", command=self.character_tree.xview)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Configure tree scrolling
        self.character_tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        
        # Configure tree to expand with window
        self.character_tree.pack(fill=tk.BOTH, expand=True)
        
        # Configure columns
        self.character_tree['columns'] = ('name', 'initiative', 'bonus', 'health', 'ac', 'custom_fields')
        
        # Format columns with minimum widths and stretch enabled
        self.character_tree.column('#0', width=0, stretch=tk.NO)  # Hidden ID column
        self.character_tree.column('name', anchor=tk.W, width=120, minwidth=100, stretch=tk.NO)
        self.character_tree.column('initiative', anchor=tk.CENTER, width=75, minwidth=75, stretch=tk.NO)
        self.character_tree.column('bonus', anchor=tk.CENTER, width=50, minwidth=50, stretch=tk.NO)
        self.character_tree.column('health', anchor=tk.CENTER, width=100, minwidth=100, stretch=tk.NO)
        self.character_tree.column('ac', anchor=tk.CENTER, width=40, minwidth=40, stretch=tk.NO)
        self.character_tree.column('custom_fields', anchor=tk.W, width=200, minwidth=150, stretch=tk.YES)
        
        # Create headings
        self.character_tree.heading('#0', text='', anchor=tk.W)
        self.character_tree.heading('name', text='Name', anchor=tk.W)
        self.character_tree.heading('initiative', text='Initiative', anchor=tk.CENTER)
        self.character_tree.heading('bonus', text='Bonus', anchor=tk.CENTER)
        self.character_tree.heading('health', text='Health', anchor=tk.CENTER)
        self.character_tree.heading('ac', text='AC', anchor=tk.CENTER)
        self.character_tree.heading('custom_fields', text='Custom Fields', anchor=tk.W)
        
        # Bind double-click event
        self.character_tree.bind('<Double-1>', self.on_double_click)
        # Bind selection event
        self.character_tree.bind('<<TreeviewSelect>>', self.on_select)
        # Bind click event for empty area detection
        self.character_tree.bind('<Button-1>', self.on_click)
        
        # Buttons Frame
        btn_frame = ttk.Frame(self.parent_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        self.copy_button = ttk.Button(btn_frame, text="Copy Character", command=self.parent.copy_character)
        self.copy_button.pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Delete", command=self.parent.delete_character).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="End Combat", command=self.parent.end_combat).pack(side=tk.LEFT, padx=2)
        
    def get_copy_button_position(self):
        """Get the position and size of the copy button"""
        return {
            'x': self.copy_button.winfo_rootx(),
            'y': self.copy_button.winfo_rooty(),
            'width': self.copy_button.winfo_width(),
            'height': self.copy_button.winfo_height()
        }

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
        
        # Handle special fields
        if column_name == 'custom_fields':
            self.parent.edit_custom_fields(item)
            return
        
        # Get the character
        items = self.character_tree.get_children()
        char_index = items.index(item)
        char = self.parent.characters[char_index]
        
        # Get the current value
        current_value = self.character_tree.item(item)['values'][int(column[1]) - 1]
        
        # If editing health, extract just the current health value
        if column_name == 'health':
            current_value = current_value.split(' | ')[0]
        
        # Create and position the entry widget
        if column_name == 'health':
            # Pass both current health and max hp for health editing
            max_hp = char.maxhp
            self.start_edit(item, column, column_name, str(current_value), max_hp=max_hp)
        else:
            self.start_edit(item, column, column_name, str(current_value))

    def start_edit(self, item, column, column_name, current_value, max_hp=None):
        """Start editing a cell"""
        # Cancel any existing edit
        self.cancel_edit()
        
        # Get cell bbox
        bbox = self.get_cell_bbox(item, column)
        if not bbox:
            return
            
        # Store current edit info
        self.current_edit = {'item': item, 'column_name': column_name}
        
        if column_name == 'health' and max_hp is not None:
            # Create frame to hold both entry and max hp label
            self.popup_frame = ttk.Frame(self.character_tree)
            
            # Create entry for current health
            self.popup_entry = ttk.Entry(self.popup_frame, width=5)
            self.popup_entry.pack(side=tk.LEFT)
            self.popup_entry.insert(0, current_value)
            self.popup_entry.select_range(0, tk.END)
            
            # Add separator and max hp
            ttk.Label(self.popup_frame, text=" | ").pack(side=tk.LEFT)
            ttk.Label(self.popup_frame, text=str(max_hp)).pack(side=tk.LEFT)
            
            # Position the frame
            self.popup_frame.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])
        else:
            # Create regular entry widget for all non-special fields
            self.popup_entry = ttk.Entry(self.character_tree)
            self.popup_entry.insert(0, current_value)
            self.popup_entry.select_range(0, tk.END)
            
            # Position the entry widget
            self.popup_entry.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])
        
        # Give focus to the entry
        self.popup_entry.focus_set()
        
        # Bind events
        self.popup_entry.bind('<Return>', lambda e: self.finish_edit())
        self.popup_entry.bind('<Escape>', lambda e: self.cancel_edit())
        self.popup_entry.bind('<FocusOut>', lambda e: self.finish_edit())


    def finish_edit(self):
        """Save the edited value"""
        if not hasattr(self, 'current_edit'):
            return
            
        # Get the edit info
        item = self.current_edit['item']
        column_name = self.current_edit['column_name']
        
        # Get the character index
        items = self.character_tree.get_children()
        char_index = items.index(item)
        char = self.parent.characters[char_index]
        
        try:
            # Get value from popup_entry
            new_value = self.popup_entry.get().strip()
            
            # Update the character attribute based on column
            if column_name == 'name':
                char.name = new_value
            elif column_name == 'initiative':
                char.initiative = int(new_value)
                # Select this character after sorting
                self.last_edited_name = char.name
            elif column_name == 'bonus':
                char.initiative_bonus = int(new_value)
                # Select this character after sorting
                self.last_edited_name = char.name
            elif column_name == 'health':
                try:
                    new_health = int(new_value)
                    if new_health < 0:
                        raise ValueError("Health cannot be negative")
                    # Cap health at max HP instead of showing warning
                    char.health = min(new_health, char.maxhp)
                except ValueError as e:
                    messagebox.showerror("Invalid Input", str(e))
                    self.popup_entry.focus_set()
                    return
            elif column_name == 'ac':
                char.ac = int(new_value)
            
            # Update the display
            self.parent.update_character_list()
            
            # If we just edited initiative, reselect the character
            if column_name == 'initiative' and hasattr(self, 'last_edited_name'):
                for item in self.character_tree.get_children():
                    values = self.character_tree.item(item)['values']
                    if values[0] == self.last_edited_name:  # Check name
                        self.character_tree.selection_set(item)
                        self.character_tree.see(item)  # Ensure visible
                        break
                delattr(self, 'last_edited_name')
            
        except ValueError as e:
            messagebox.showerror("Error", str(e) if str(e) else f"Invalid value for {column_name}")
        finally:
            self.cancel_edit()

    def cancel_edit(self):
        """Cancel the current edit"""
        if self.popup_entry:
            self.popup_entry.destroy()
            self.popup_entry = None
        if hasattr(self, 'popup_frame'):
            self.popup_frame.destroy()
            del self.popup_frame


    def update_character_list(self, characters):
        """Update the character list display"""
        # Clear existing items
        for item in self.character_tree.get_children():
            self.character_tree.delete(item)
            
        # Sort characters by initiative
        sorted_chars = sorted(characters, key=lambda x: (-x.initiative, -x.initiative_bonus))
        
        # Get current character name
        current_name = None
        if self.round_counter and hasattr(self.round_counter, 'current_character'):
            current_name = self.round_counter.current_character.get()
        
        # Add characters to tree
        for char in sorted_chars:
            # Format custom fields for display
            custom_fields_str = ', '.join(f"{k}: {v}" for k, v in char.custom_fields.items())
            
            # Insert the character
            item = self.character_tree.insert('', 'end', values=(
                char.name,
                char.initiative,
                char.initiative_bonus,
                f"{char.health} | {char.maxhp}",
                char.ac,
                custom_fields_str
            ))
            
            # Apply bold style if this is the current character
            if current_name and char.name == current_name:
                self.character_tree.tag_configure('bold', font=('TkDefaultFont', 11, 'bold'))
                self.character_tree.item(item, tags=('bold',))

    def _on_current_character_change(self, *args):
        """Called when the current character changes"""
        if hasattr(self.parent, 'characters'):
            self.update_character_list(self.parent.characters)
    
    def get_selected_character(self):
        """Get the currently selected character"""
        selected = self.character_tree.selection()
        if not selected:
            return None
        items = self.character_tree.get_children()
        char_index = items.index(selected[0])
        return self.parent.characters[char_index]
        
    def on_select(self, event):
        """Handle selection of a character"""
        if self.suppress_selection_event:
            return
        character = self.get_selected_character()
        if hasattr(self.parent, 'on_character_selected'):
            self.parent.on_character_selected(character)
            
    def on_click(self, event):
        """Handle clicks on the tree view"""
        region = self.character_tree.identify('region', event.x, event.y)
        # If clicked in an empty area (not on a row)
        if region == 'nothing':
            # Clear selection and notify parent
            self.character_tree.selection_remove(self.character_tree.selection())
            if hasattr(self.parent, 'on_character_selected'):
                self.parent.on_character_selected(None)
