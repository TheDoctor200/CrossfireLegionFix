import flet as ft
from regional_utils import RegionalFormatChanger
from ui_components import create_header, create_status_container, create_controls_container, create_path_input_section
from ui_handlers import setup_ui_handlers, update_status

def main(page: ft.Page):
    # FAST STARTuP
    page.title = "Regional Format Control - Crossfire Legion"
    page.padding = 15
    page.spacing = 15
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#1a1a1a"
    page.color_scheme_seed = "#00ff41"
    
    # INSTANT DESKTOP WINDOW PROPERTIES - instant loading
    try:
        # Modern Flet window properties (instant loading)
        page.window.width = 550
        page.window.height = 650
        page.window.resizable = False
        page.window.maximizable = False
        page.window.center()
        page.window.min_width = 550
        page.window.min_height = 650
        page.window.always_on_top = False
        page.window.skip_task_bar = False
        page.window.frameless = False
        page.window.full_screen = False
        page.window.visible = True
    except Exception:
        # Fallback for older Flet versions (instant loading)
        try:
            page.window_width = 550
            page.window_height = 650
            page.window_resizable = False
            page.window_maximizable = False
        except Exception:
            pass
    
    # Initialize the regional format changer
    rfc = RegionalFormatChanger()
    
    # Initialize locale data
    current_locale_data = rfc.get_current_locale()
    current_locale = current_locale_data.get("locale", "Unknown")
    rfc.current_locale = current_locale
    
    # Load or set default locale
    saved_default = rfc.load_config()
    if saved_default:
        rfc.default_locale = saved_default
    else:
        rfc.default_locale = current_locale
        rfc.save_config()
    
    # Create UI components
    header = create_header()
    status_container = create_status_container(current_locale, rfc.default_locale)
    controls_container, buttons = create_controls_container()
    path_input_section = create_path_input_section()
    
    # Status text for operations feedback
    status_text = ft.Text(
        "Ready for operations",
        size=11,
        color="#ffffff",
        text_align=ft.TextAlign.CENTER,
        italic=True
    )
    
    # Main layout
    main_container = ft.Container(
        content=ft.Column([
            header,
            status_container,
            controls_container,
            path_input_section
        ], spacing=0),
        expand=True
    )
    
    # Add to page
    page.add(main_container)
    
    # Setup UI handlers and state management
    setup_ui_handlers(page, rfc, status_text, status_container, path_input_section, buttons)
    
    # Initial status update
    update_status(page, rfc, status_container, buttons)

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.FLET_APP)
