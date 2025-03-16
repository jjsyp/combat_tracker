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
        
        # Set minimum window size
        self.root.minsize(800, 400)
        
        # Create main container frame with grid
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        self.main_container.grid_columnconfigure(0, weight=1, minsize=400)  # Left frame gets more space
        self.main_container.grid_columnconfigure(1, weight=0)  # Right frame doesn't expand
        self.main_container.grid_rowconfigure(0, weight=1)
        
        # Create main frames
        self.character_list_frame = ttk.Frame(self.main_container)
        self.character_list_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        
        # Create a wrapper frame to control the maximum width of the right frame
        right_wrapper = ttk.Frame(self.main_container)
        right_wrapper.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        right_wrapper.grid_columnconfigure(0, weight=1)
        right_wrapper.grid_rowconfigure(0, weight=1)
        
        # Create the actual right frame with fixed width
        self.character_detail_frame = ttk.Frame(right_wrapper, width=300)
        self.character_detail_frame.grid(row=0, column=0, sticky='nsew')
        self.character_detail_frame.grid_propagate(False)  # Keep fixed width
        
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
