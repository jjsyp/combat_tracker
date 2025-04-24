import tkinter as tk
from tkinter import messagebox, filedialog
import os
import json

class MenuBar:
    def __init__(self, root, parent):
        """
        Initialize the menu bar
        
        Args:
            root: The root window
            parent: The parent window (main GUI) that contains save/load methods
        """
        self.root = root
        self.parent = parent
        self.create_menu_bar()
        
    def create_menu_bar(self):
        """Create the menu bar with File options and Templates button"""
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
        
        # Templates button
        menubar.add_command(label="Templates", command=self.show_templates)

    def save_session(self):
        """Save the current session to the default file"""
        try:
            # Save character data
            save_path = os.path.join('saves', 'last_session.json')
            self.parent.save_to_file(save_path)
            
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
                self.parent.save_to_file(file_path)
                messagebox.showinfo("Success", "Session saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save session: {str(e)}")
    
    def load_session(self):
        """Load a session from a chosen file"""
        try:
            file_path = filedialog.askopenfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                initialdir="saves"
            )
            if file_path:
                self.parent.load_from_file(file_path)
                messagebox.showinfo("Success", "Session loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load session: {str(e)}")
            
    def show_templates(self):
        """Show the templates management screen"""
        from GUI.components.templates_screen import TemplatesScreen
        TemplatesScreen(self.root, self.parent)
