"""
Main file for the project. This file is intended to be the main entry point for the project.
"""
import sys
from pathlib import Path
import tkinter as tk

if __name__ == "__main__":
    # Add the current directory to the system path
    sys.path.append(str(Path(__file__).parent))
    
    # Run the initialization GUI
    from gui_initialize import *
    from utils.commands_gui_initialize import *
    window.mainloop()
    print("Initialization GUI closed.")
    
    # Run the main GUI
    from gui_main_frame import *
    from utils.commands_gui_main_frame import *
    window.mainloop()