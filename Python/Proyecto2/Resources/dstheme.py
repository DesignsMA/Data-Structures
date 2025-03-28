from ttkbootstrap.style import Style
USER_THEMES = {
    "dstheme": {
        "type": "dark",
        "colors": {
            "primary": "#00ff99",
            "secondary": "#0b9ff0",
            "success": "#0fff6f",
            "info": "#3498db",
            "warning": "#f39c12",
            "danger": "#ff5353",
            "light": "#ADB5BD",
            "dark": "#303030",
            "bg": "#161616",
            "fg": "#ffffff",
            "selectbg": "#626262",
            "selectfg": "#ffffff",
            "border": "#0dff55",
            "inputfg": "#ffffff",
            "inputbg": "#313131",
            "active": "#95ffca"
        }
    }
}

Style().configure(
    ".",
    font=("Montserrat", 12)  # Fuente para todos los widgets
)
