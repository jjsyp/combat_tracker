import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk

class AppConfig:
    def __init__(self, root):
        """
        Initialize application configuration
        
        Args:
            root: The root tkinter window
        """
        self.root = root
        self.setup_window()
        self.setup_icon()
        
    def setup_window(self):
        """Configure the main window"""
        self.root.title("Combat Tracker")
        
        # Create main frames
        self.character_list_frame = ttk.Frame(self.root)
        self.character_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.character_detail_frame = ttk.Frame(self.root)
        self.character_detail_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def setup_icon(self):
        """Set up the application icon based on platform"""
        ico_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app.ico')
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
            
    @property
    def list_frame(self):
        """Get the character list frame"""
        return self.character_list_frame
        
    @property
    def detail_frame(self):
        """Get the character detail frame"""
        return self.character_detail_frame
