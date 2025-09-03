import flet as ft

def create_header():
    """Create the header with military styling"""
    return ft.Container(
        content=ft.Column([
            ft.Text(
                "⚡ REGIONAL FORMAT CONTROL ⚡",
                size=18,
                weight=ft.FontWeight.BOLD,
                color="#00ff41",
                text_align=ft.TextAlign.CENTER
            ),
            ft.Text(
                "CROSSFIRE LEGION TACTICAL SYSTEM",
                size=10,
                color="#888888",
                text_align=ft.TextAlign.CENTER
            )
        ], spacing=2),
        padding=ft.padding.all(15),
        border=ft.border.all(1, "#333333"),
        border_radius=ft.border_radius.only(top_left=8, top_right=8)
    )

def create_status_container(current_locale, default_locale):
    """Create the status display container"""
    current_status = ft.Text(
        f"Current: {current_locale}",
        size=12,
        color="#00ff41",
        weight=ft.FontWeight.BOLD
    )
    
    default_status = ft.Text(
        f"Default: {default_locale}",
        size=12,
        color="#ffaa00",
        weight=ft.FontWeight.BOLD
    )
    
    return ft.Container(
        content=ft.Column([
            ft.Text("SYSTEM STATUS", size=14, color="#ffffff", weight=ft.FontWeight.BOLD),
            ft.Divider(color="#333333", height=1),
            current_status,
            default_status,
        ], spacing=8),
        padding=ft.padding.all(15),
        border=ft.border.all(1, "#333333")
    )

def create_controls_container():
    """Create the controls container with buttons"""
    set_en_us_btn = ft.ElevatedButton(
        text="Set to EN-US",
        bgcolor="#2d5a3d",
        color="#ffffff",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=4),
            elevation=3,
        ),
        height=40,
        width=140
    )
    fast_en_us_btn = ft.ElevatedButton(
        text="Fast EN-US (Live)",
        bgcolor="#2d5a3d",
        color="#ffffff",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=4),
            elevation=3,
        ),
        height=40,
        width=180
    )
    
    refresh_btn = ft.ElevatedButton(
        text="🔄 Refresh",
        bgcolor="#2d4a5a",
        color="#ffffff",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=4),
            elevation=3,
        ),
        height=40,
        width=100
    )
    revert_default_btn = ft.ElevatedButton(
        text="Revert to Default",
        bgcolor="#5a3d2d",
        color="#ffffff",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=4),
            elevation=3,
        ),
        height=40,
        width=180
    )
    
    launch_game_btn = ft.ElevatedButton(
        text="Launch via Steam",
        bgcolor="#4a2d5a",
        color="#ffffff",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=4),
            elevation=3,
        ),
        height=40,
        width=180
    )
    
    offline_launch_btn = ft.ElevatedButton(
        text="Launch from Path",
        bgcolor="#5a2d4a",
        color="#ffffff",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=4),
            elevation=3,
        ),
        height=40,
        width=180
    )
    
    container = ft.Container(
        content=ft.Column([
            ft.Text("TACTICAL CONTROLS", size=14, color="#ffffff", weight=ft.FontWeight.BOLD),
            ft.Divider(color="#333333", height=1),
            ft.Row([
                set_en_us_btn,
                fast_en_us_btn,
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                refresh_btn,
                revert_default_btn,
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                launch_game_btn,
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                offline_launch_btn,
            ], alignment=ft.MainAxisAlignment.CENTER)
        ], spacing=10),
        padding=ft.padding.all(15),
        border=ft.border.all(1, "#333333")
    )
    
    # Return both the container and button references
    buttons = {
        'set_en_us_btn': set_en_us_btn,
        'fast_en_us_btn': fast_en_us_btn,
        'revert_default_btn': revert_default_btn,
        'refresh_btn': refresh_btn,
        'launch_game_btn': launch_game_btn,
        'offline_launch_btn': offline_launch_btn
    }
    
    return container, buttons

def create_path_input_section():
    """Create the path input section with text field and browse button"""
    label_text = ft.Text(
        "Game Path",
        size=12,
        color="#ffffff",
        weight=ft.FontWeight.BOLD
    )
    example_text = ft.Text(
        "Example: C:\\Steam\\steamapps\\common\\Crossfire Legion\\Crossfire_Legion.exe",
        size=11,
        color="#aaaaaa",
        selectable=True
    )
    game_path_input = ft.TextField(
        label=None,
        width=None,
        expand=True,
        height=40,
        border=ft.InputBorder.UNDERLINE,
        border_radius=4,
        color="#ffffff",
        bgcolor="transparent",
        text_align=ft.TextAlign.LEFT,
        hint_text="Enter full path to Crossfire_Legion.exe"
    )

    browse_btn = ft.ElevatedButton(
        text="📁 Browse",
        bgcolor="#2d5a4a",
        color="#ffffff",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=4),
            elevation=2,
        ),
        height=40,
        width=110
    )

    container = ft.Container(
        content=ft.Column([
            label_text,
            example_text,
            ft.Row([
                game_path_input,
                browse_btn
            ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.START, spacing=10)
        ], spacing=6),
        padding=ft.padding.all(15),
        border=ft.border.all(1, "#333333"),
        border_radius=ft.border_radius.only(bottom_left=8, bottom_right=8),
        expand=True
    )
    return container, browse_btn, game_path_input

