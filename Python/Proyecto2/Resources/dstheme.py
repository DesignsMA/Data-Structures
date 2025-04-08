# Import required libraries  
import ttkbootstrap as ttk  
from ttkbootstrap.constants import *  
from ttkbootstrap.style import ThemeDefinition  
import json  # Load theme from a JSON file  
import os

def apply_custom_theme():
    dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(dir,"dstheme.json"), "r") as f:  
        custom_theme_data = json.load(f)  # Load JSON as a dictionary  

    # Required theme properties  
    required_keys = ["name", "colors", "fonts", "layout"]  
    filtered_theme_data = {key: custom_theme_data[key] for key in required_keys if key in custom_theme_data}  

    # Ensure essential color properties exist  
    required_colors = ["border", "inputfg", "inputbg", "active"]  
    for color in required_colors:  
        if color not in filtered_theme_data["colors"]:  
            filtered_theme_data["colors"][color] = "#000000"  # Default black if missing  
    # Convert dictionary to ThemeDefinition object  
    custom_theme = ThemeDefinition(**filtered_theme_data)  
    
    return custom_theme