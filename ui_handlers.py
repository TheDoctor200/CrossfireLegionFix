import flet as ft
import os

def setup_ui_handlers(page, rfc, status_text, status_container, path_input_section, buttons):
    """Setup all UI event handlers and state management"""
    
    # Get references to UI elements from the buttons dictionary
    set_en_us_btn = buttons['set_en_us_btn']
    refresh_btn = buttons['refresh_btn']
    launch_game_btn = buttons['launch_game_btn']
    offline_launch_btn = buttons['offline_launch_btn']
    
    # Get references from the path input section container
    path_row = path_input_section.content  # Get the Row from the Container
    game_path_input = path_row.controls[0]  # Game path input field
    browse_btn = path_row.controls[1]       # Browse button
    
    # Store references on page for access in handlers
    page.game_path_input = game_path_input
    page.rfc = rfc
    page.status_text = status_text
    
    # Setup button click handlers
    set_en_us_btn.on_click = lambda e: on_set_en_us(e, page, rfc, status_text)
    refresh_btn.on_click = lambda e: on_refresh(e, page, rfc, status_text, status_container, buttons)
    launch_game_btn.on_click = lambda e: on_launch_game(e, page, rfc, status_text)
    offline_launch_btn.on_click = lambda e: on_launch_manual(e, page, rfc, status_text)
    browse_btn.on_click = lambda e: browse_for_game_file(e, page, game_path_input, status_text)

def on_set_en_us(e, page, rfc, status_text):
    """Handle setting locale to EN-US"""
    status_text.value = "➡️ Opening Windows Settings for Region..."
    status_text.color = "#ffa500"
    page.update()

    success = rfc.set_locale_to_en_us()
    if success:
        status_text.value = "ℹ️ Please set Region and Format to EN-US in Settings."
        status_text.color = "#2196F3"
    else:
        status_text.value = "❌ Failed to open Settings."
        status_text.color = "#f44336"

    page.update()
    page.run_task(delayed_update, page, status_text)

def on_refresh(e, page, rfc, status_text, status_container, buttons):
    """Handle manual refresh"""
    status_text.value = "🔄 Refreshing status..."
    status_text.color = "#2196F3"
    page.update()
    
    update_status(page, rfc, status_container, buttons)
    status_text.value = "✅ Status refreshed"
    status_text.color = "#4CAF50"
    page.update()

def on_launch_game(e, page, rfc, status_text):
    """Handle launching Crossfire: Legion via Steam"""
    status_text.value = "🚀 Launching Crossfire: Legion via Steam..."
    status_text.color = "#ffa500"
    page.update()
    
    success, message = rfc.launch_crossfire_legion()
    if success:
        status_text.value = f"✅ {message}"
        status_text.color = "#4CAF50"
    else:
        status_text.value = f"❌ {message}"
        status_text.color = "#f44336"
    
    page.update()
    page.run_task(delayed_update, page, status_text)

def on_launch_manual(e, page, rfc, status_text):
    """Handle launching Crossfire: Legion from manual path"""
    game_path = page.game_path_input.value
    if not game_path:
        status_text.value = "❌ Please enter a game path first"
        status_text.color = "#f44336"
        page.update()
        return
    
    status_text.value = "🎮 Launching Crossfire: Legion from manual path..."
    status_text.color = "#ffa500"
    page.update()
    
    success, message = rfc.launch_manual_path(game_path)
    if success:
        status_text.value = f"✅ {message}"
        status_text.color = "#4CAF50"
    else:
        status_text.value = f"❌ {message}"
        status_text.color = "#f44336"
    
    page.update()
    page.run_task(delayed_update, page, status_text)

def browse_for_game_file(e, page, game_path_input, status_text):
    """Open a file dialog to select a game executable."""
    try:
        # Create a file picker dialog
        file_picker = ft.FilePicker(
            on_result=lambda e: handle_file_picker_result(e, page, game_path_input)
        )
        page.overlay.append(file_picker)
        page.update()
        
        # Open the file picker
        file_picker.pick_files(
            allowed_extensions=["exe"],
            initial_directory=os.path.dirname(game_path_input.value) if game_path_input.value else "C:\\"
        )
        
    except Exception as e:
        status_text.value = f"❌ Browse error: {e}"
        status_text.color = "#f44336"
        page.update()

def handle_file_picker_result(e, page, game_path_input):
    """Handle the result from file picker"""
    if e.files:
        selected_file = e.files[0].path
        game_path_input.value = selected_file
        page.update()
    
    # Remove the file picker from overlay
    if page.overlay:
        page.overlay.pop()
        page.update()

async def delayed_update(page, status_text):
    """Delayed status update"""
    import asyncio
    await asyncio.sleep(1)
    status_text.value = "Ready for operations"
    status_text.color = "#ffffff"
    page.update()

def update_status(page, rfc, status_container, buttons):
    """Update the status display"""
    current_data = rfc.get_current_locale()
    current_locale = current_data.get("locale", "Unknown")
    rfc.current_locale = current_locale
    
    # Update status displays
    current_status = status_container.content.controls[2]  # Get current status text
    default_status = status_container.content.controls[3]  # Get default status text
    
    current_status.value = f"Current: {current_locale}"
    if current_data.get("country"):
        current_status.value += f" ({current_data['country']})"
    
    default_status.value = f"Default: {rfc.default_locale}"
    
    # Update button states using the buttons dictionary
    set_en_us_btn = buttons['set_en_us_btn']
    if current_locale.lower() == "en-us":
        set_en_us_btn.disabled = True
        set_en_us_btn.text = "✓ Already EN-US"
        set_en_us_btn.bgcolor = "#1a4d3a"
    else:
        set_en_us_btn.disabled = False
        set_en_us_btn.text = "Set to EN-US"
        set_en_us_btn.bgcolor = "#2d5a3d"
    
    page.update()
