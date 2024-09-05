"""
Main file for the project. This file is intended to be the main entry point for the project.
"""
import sys
from pathlib import Path
import tkinter as tk

if __name__ == "__main__":
    # Run the initialization GUI
    from gui_initialize import *
    sys.path.append(str(Path(__file__).parent))
    window.mainloop()
    
    # Run the main GUI
    sys.path.append(str(Path(__file__).parent))
    from gui_main import window
    window.mainloop()