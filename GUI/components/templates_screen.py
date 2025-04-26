import tkinter as tk
from tkinter import ttk
from GUI.components.template_list import TemplateList
from GUI.components.character_details import CharacterDetails

class TemplatesScreen:
    def __init__(self, root, parent):
        """
        Initialize the templates screen
        
        Args:
            root: The root window
            parent: The parent window (main GUI)
        """
        self.root = root
        self.parent = parent
        
        # Create main window
        self.window = tk.Toplevel(root)
        self.window.title("Character Templates")
        self.window.geometry("1000x600")
        
        # Create main container
        self.main_container = ttk.Frame(self.window)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create left and right frames
        self.left_frame = ttk.Frame(self.main_container)
        self.right_frame = ttk.Frame(self.main_container)
        
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Initialize components
        self.setup_template_list()
        self.setup_character_details()
        
        # Add buttons at the bottom
        self.setup_buttons()
        
    def setup_template_list(self):
        """Setup the templates list panel"""
        # Create a label frame for the template list
        list_frame = ttk.LabelFrame(self.left_frame, text="Templates")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create the template list component
        self.template_list = TemplateList(list_frame, self)
        
    def setup_character_details(self):
        """Setup the character details panel"""
        # Create a label frame for character details
        details_frame = ttk.LabelFrame(self.right_frame, text="New Character")
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create the character details component with a custom parent that handles template creation
        class TemplateParent:
            def __init__(self, template_screen):
                self.template_screen = template_screen
                
            def add_character(self, char):
                # Save the character as a template
                self.template_screen.template_list.save_template(char)
                
        self.template_parent = TemplateParent(self)
        self.character_details = CharacterDetails(details_frame, self.template_parent)
        
        # Enable template mode
        self.character_details.set_template_mode(True)
        
    def setup_buttons(self):
        """Setup the action buttons"""
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Left side buttons
        left_buttons = ttk.Frame(button_frame)
        left_buttons.pack(side=tk.LEFT, fill=tk.X)
        
        # Add to Combat button
        ttk.Button(
            left_buttons, 
            text="Add Selected to Combat",
            command=self.add_selected_to_combat
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        # Delete Selected button
        ttk.Button(
            left_buttons,
            text="Delete Selected",
            command=self.delete_selected_templates
        ).pack(side=tk.LEFT)
        
        # Close button (right side)
        ttk.Button(
            button_frame,
            text="Close",
            command=self.window.destroy
        ).pack(side=tk.RIGHT)
        
    def add_selected_to_combat(self):
        """Add selected templates to the combat tracker"""
        selected_templates = self.template_list.get_selected_templates()
        if not selected_templates:
            return
            
        # Add each selected template as a new character
        for template in selected_templates:
            # Create a copy of the template
            char = template.copy()
            # Add to the main combat tracker
            self.parent.characters.append(char)
            
        # Update the main combat tracker display
        self.parent.update_character_list()
        
    def delete_selected_templates(self):
        """Delete selected templates"""
        selected_templates = self.template_list.get_selected_templates()
        if not selected_templates:
            return
            
        # Delete each selected template
        for template in selected_templates:
            self.template_list.delete_template(template)
        
        # Update the template list display
        self.template_list.update_template_list()
