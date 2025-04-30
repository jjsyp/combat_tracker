import tkinter as tk
from tkinter import ttk
from character.character import Character
import os
import json

class TemplateList:
    def __init__(self, parent_frame, gui_ref):
        """
        Initialize the template list component
        
        Args:
            parent_frame: The frame to place this component in
            gui_ref: Reference to the main GUI for callbacks
        """
        self.parent_frame = parent_frame
        self.gui_ref = gui_ref
        self.templates = []
        
        # Get the absolute path to the templates directory
        self.template_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "templates"
        )
        os.makedirs(self.template_dir, exist_ok=True)
        
        # Create template list view
        self.create_template_list()
        
        # Load existing templates
        self.load_templates()
        
    def create_template_list(self):
        """Create the template list treeview with checkboxes"""
        # Create frame for template list
        self.frame = ttk.Frame(self.parent_frame)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview
        columns = ("Selected", "Name", "HP", "AC")
        self.template_tree = ttk.Treeview(self.frame, columns=columns, show="headings")
        
        # Set column headings
        self.template_tree.heading("Selected", text="")  # Checkbox column
        self.template_tree.heading("Name", text="Name")
        self.template_tree.heading("HP", text="HP")
        self.template_tree.heading("AC", text="AC")
        
        # Set column widths
        self.template_tree.column("Selected", width=50, stretch=False)  # Increased width for checkbox
        self.template_tree.column("Name", width=150)
        self.template_tree.column("HP", width=70)
        self.template_tree.column("AC", width=70)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.template_tree.yview)
        self.template_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        self.template_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind events
        self.template_tree.bind("<ButtonRelease-1>", self.on_click)
        
        # Create larger checkbox symbols
        self.checkbox_unchecked = "☐"  # Larger empty checkbox
        self.checkbox_checked = "☑"  # Larger checked checkbox
        
    def load_templates(self):
        """Load templates from the templates directory"""
        
        self.templates = []
        try:
            for filename in os.listdir(self.template_dir):
                if filename.endswith(".json"):
                    with open(os.path.join(self.template_dir, filename), 'r') as f:
                        template_data = json.load(f)
                        template = Character.from_dict(template_data)
                        self.templates.append(template)
            
            self.update_template_list()
        except Exception as e:
            print(f"Error loading templates: {str(e)}")
            
    def update_template_list(self):
        """Update the template list display"""
        # Clear existing items
        for item in self.template_tree.get_children():
            self.template_tree.delete(item)
            
        # Add templates to tree
        for template in self.templates:
            values = (
                self.checkbox_unchecked,  # Unchecked checkbox
                template.name,
                f"{template.health}/{template.maxhp}",
                template.ac
            )
            self.template_tree.insert("", tk.END, values=values)
            
    def on_click(self, event):
        """Handle mouse click in the template tree"""
        # Get the clicked region and item
        region = self.template_tree.identify_region(event.x, event.y)
        item = self.template_tree.identify_row(event.y)
        if not item:
            return
            
        # Handle checkbox click
        if region == "cell":
            column = self.template_tree.identify_column(event.x)
            if str(column) == "#1":  # Selected column
                current_value = self.template_tree.set(item, "Selected")
                new_value = self.checkbox_checked if current_value == self.checkbox_unchecked else self.checkbox_unchecked
                self.template_tree.set(item, "Selected", new_value)
                return
        
        # Handle template selection (if not clicking checkbox)
        if region != "nothing":
            # Get the template index
            items = self.template_tree.get_children()
            idx = items.index(item)
            template = self.templates[idx]
            
            # Update character details panel with template data
            if hasattr(self.gui_ref, 'character_details'):
                self.gui_ref.character_details.show_template(template)
                    
    def save_template(self, character):
        """Save a character as a template"""
        # Save template to file
        template_path = os.path.join(self.template_dir, f"{character.name}.json")
        with open(template_path, 'w') as f:
            json.dump(character.__dict__, f, indent=4)
            
        # Add to templates list and update display
        self.templates.append(character)
        self.update_template_list()
        
    def get_selected_templates(self):
        """Get list of selected templates"""
        selected = []
        for item in self.template_tree.get_children():
            if self.template_tree.set(item, "Selected") == "☑":
                idx = list(self.template_tree.get_children()).index(item)
                selected.append(self.templates[idx])
        return selected
        
    def delete_template(self, template):
        """Delete a template from disk and memory"""
        # Remove from disk
        template_path = os.path.join(self.template_dir, f"{template.name}.json")
        try:
            os.remove(template_path)
        except OSError:
            pass  # File might not exist
            
        # Remove from memory
        try:
            self.templates.remove(template)
        except ValueError:
            pass  # Template might not be in list
