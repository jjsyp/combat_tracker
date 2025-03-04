import tkinter as tk
from GUI.gui import CombatTrackerGUI

def main():
    root = tk.Tk()
    app = CombatTrackerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()