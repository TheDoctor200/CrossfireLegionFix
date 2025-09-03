import flet as ft
import os
import asyncio

def setup_ui_handlers(page, rfc, status_text, status_container, path_input_section, buttons, browse_button=None, path_input=None):
    """Setup all UI event handlers and state management"""
    
    # Get references to UI elements from the buttons dictionary
    set_en_us_btn = buttons['set_en_us_btn']
    fast_en_us_btn = buttons['fast_en_us_btn']
    refresh_btn = buttons['refresh_btn']
    revert_default_btn = buttons['revert_default_btn']
    launch_game_btn = buttons['launch_game_btn']
    offline_launch_btn = buttons['offline_launch_btn']
    
    # If path controls are provided directly, use them; else fallback to extracting from container
    if path_input and browse_button:
        game_path_input = path_input
        browse_btn = browse_button
    else:
        # Fallback for legacy: extract from container
        path_row = path_input_section.content  # Get the Column from the Container
        row = path_row.controls[2]  # The Row is the third control in the Column
        game_path_input = row.controls[0]
        browse_btn = row.controls[1]

    # Store references on page for access in handlers
    page.game_path_input = game_path_input
    page.rfc = rfc
    page.status_text = status_text

    # Load saved game path if available
    try:
        saved_path = rfc.load_game_path()
        if saved_path:
            game_path_input.value = saved_path
    except Exception:
        pass

    # Auto-save when user edits the path field
    def on_game_path_changed(e):
        try:
            rfc.save_game_path(game_path_input.value or "")
            status_text.value = "✅ Path saved"
            status_text.color = "#4CAF50"
            page.update()
        except Exception as ex:
            status_text.value = f"⚠️ Could not save path: {ex}"
            status_text.color = "#ffa500"
            page.update()
    game_path_input.on_change = on_game_path_changed
    
    # Setup button click handlers
    set_en_us_btn.on_click = lambda e: on_set_en_us(e, page, rfc, status_text)
    fast_en_us_btn.on_click = lambda e: on_fast_set_en_us(e, page, rfc, status_text, status_container, buttons)
    refresh_btn.on_click = lambda e: on_refresh(e, page, rfc, status_text, status_container, buttons)
    revert_default_btn.on_click = lambda e: on_revert_default(e, page, rfc, status_text, status_container, buttons)
    launch_game_btn.on_click = lambda e: on_launch_game(e, page, rfc, status_text)
    offline_launch_btn.on_click = lambda e: on_launch_manual(e, page, rfc, status_text)
    browse_btn.on_click = lambda e: browse_for_game_file(e, page, game_path_input, status_text, rfc)

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

def on_fast_set_en_us(e, page, rfc, status_text, status_container, buttons):
    """Quickly apply EN-US regional format via registry and broadcast."""
    buttons['fast_en_us_btn'].disabled = True
    buttons['revert_default_btn'].disabled = True
    status_text.value = "⚡ Applying EN-US regional format..."
    status_text.color = "#ffa500"
    page.update()

    success, message = rfc.apply_locale_quick("en-US")
    if success:
        status_text.value = f"✅ {message}"
        status_text.color = "#4CAF50"
    else:
        status_text.value = f"❌ {message}"
        status_text.color = "#f44336"

    update_status(page, rfc, status_container, buttons)
    page.update()
    page.run_task(button_cooldown, page, buttons, 15, rfc, status_container)

def on_revert_default(e, page, rfc, status_text, status_container, buttons):
    """Revert regional format to saved default from config."""
    buttons['fast_en_us_btn'].disabled = True
    buttons['revert_default_btn'].disabled = True
    status_text.value = "↩️ Reverting to default regional format..."
    status_text.color = "#ffa500"
    page.update()

    success, message = rfc.revert_to_default_quick()
    if success:
        status_text.value = f"✅ {message}"
        status_text.color = "#4CAF50"
    else:
        status_text.value = f"❌ {message}"
        status_text.color = "#f44336"

    update_status(page, rfc, status_container, buttons)
    page.update()
    page.run_task(button_cooldown, page, buttons, 15, rfc, status_container)

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

def browse_for_game_file(e, page, game_path_input, status_text, rfc):
    """Open a file dialog to select a game executable."""
    try:
        # Reuse a persistent file picker attached to page
        if not hasattr(page, "file_picker") or page.file_picker is None:
            try:
                page.file_picker = ft.FilePicker(
                    on_result=lambda res: handle_file_picker_result(res, page, game_path_input, rfc)
                )
                page.overlay.append(page.file_picker)
                page.update()
            except Exception:
                page.file_picker = None

        # Open the file picker (ANY type for wider compatibility)
        try:
            if page.file_picker:
                page.file_picker.pick_files(
                    allow_multiple=False,
                    # Use filter by extension if ANY is not supported in this version
                    allowed_extensions=["exe"],
                    initial_directory=(os.path.dirname(game_path_input.value) if game_path_input.value else "C:\\")
                )
            else:
                # Fallback: use dialog via pick_files on a temporary picker
                temp_picker = ft.FilePicker(
                    on_result=lambda res: handle_file_picker_result(res, page, game_path_input, rfc)
                )
                page.overlay.append(temp_picker)
                page.update()
                temp_picker.pick_files(allow_multiple=False, allowed_extensions=["exe"], initial_directory="C:\\")
        except Exception as ex:
            status_text.value = f"❌ Browse not supported: {ex}"
            status_text.color = "#f44336"
            page.update()
            # Fallback using tkinter
            try:
                import tkinter as tk
                from tkinter import filedialog
                root = tk.Tk()
                root.withdraw()
                file_path = filedialog.askopenfilename(title="Select Crossfire_Legion.exe", initialdir="C:/", filetypes=[("Executable", "*.exe"), ("All files", "*.*")])
                root.update()
                root.destroy()
                if file_path:
                    game_path_input.value = file_path
                    try:
                        rfc.save_game_path(file_path)
                        status_text.value = "✅ Path saved"
                        status_text.color = "#4CAF50"
                    except Exception:
                        status_text.value = "⚠️ Could not save path"
                        status_text.color = "#ffa500"
                    page.update()
            except Exception:
                pass
        
    except Exception as e:
        status_text.value = f"❌ Browse error: {e}"
        status_text.color = "#f44336"
        page.update()

def handle_file_picker_result(e, page, game_path_input, rfc):
    """Handle the result from file picker"""
    if e.files:
        selected_file = e.files[0].path
        if not selected_file.lower().endswith(".exe"):
            page.status_text.value = "❌ Please select a .exe file"
            page.status_text.color = "#f44336"
        else:
            game_path_input.value = selected_file
            try:
                rfc.save_game_path(selected_file)
                page.status_text.value = "✅ Path saved"
                page.status_text.color = "#4CAF50"
            except Exception:
                page.status_text.value = "⚠️ Could not save path, will still use it now"
                page.status_text.color = "#ffa500"
        page.update()
    
    # Remove the file picker from overlay
    # Keep picker in overlay for reuse; do not pop

async def delayed_update(page, status_text):
    """Delayed status update"""
    import asyncio
    await asyncio.sleep(3)
    status_text.value = "Ready for operations"
    status_text.color = "#ffffff"
    page.update()

async def button_cooldown(page, buttons, duration, rfc, status_container):
    """Disables buttons for a duration, then re-enables them by refreshing status."""
    fast_btn = buttons['fast_en_us_btn']
    revert_btn = buttons['revert_default_btn']
    
    original_fast_text = fast_btn.text
    original_revert_text = revert_btn.text

    fast_btn.disabled = True
    revert_btn.disabled = True

    for i in range(duration, 0, -1):
        cooldown_text = f"Cooldown ({i}s)"
        fast_btn.text = cooldown_text
        revert_btn.text = cooldown_text
        page.update()
        await asyncio.sleep(1)
    
    fast_btn.text = original_fast_text
    revert_btn.text = original_revert_text
    update_status(page, rfc, status_container, buttons)
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
    fast_en_us_btn = buttons.get('fast_en_us_btn')
    revert_default_btn = buttons.get('revert_default_btn')

    is_en_us = current_locale.lower() == "en-us"
    
    # Do not change button state if it's in cooldown
    if fast_en_us_btn and fast_en_us_btn.text.startswith("Cooldown"):
        page.update()
        return

    if is_en_us:
        set_en_us_btn.disabled = True
        set_en_us_btn.text = "✓ Already EN-US"
        set_en_us_btn.bgcolor = "#1a4d3a"
        if fast_en_us_btn:
            fast_en_us_btn.disabled = True
            fast_en_us_btn.text = "✓ Already EN-US"
            fast_en_us_btn.bgcolor = "#1a4d3a"
    else:
        set_en_us_btn.disabled = False
        set_en_us_btn.text = "Set to EN-US"
        set_en_us_btn.bgcolor = "#2d5a3d"
        if fast_en_us_btn:
            fast_en_us_btn.disabled = False
            fast_en_us_btn.text = "Fast EN-US (Live)"
            fast_en_us_btn.bgcolor = "#2d5a3d"

    # Revert button state
    if revert_default_btn:
        if rfc.default_locale and current_locale.lower() == str(rfc.default_locale).lower():
            revert_default_btn.disabled = True
            revert_default_btn.text = "✓ Already Default"
            revert_default_btn.bgcolor = "#4d3a1a"
        else:
            revert_default_btn.disabled = False
            revert_default_btn.text = "Revert to Default"
            revert_default_btn.bgcolor = "#5a3d2d"
    
    page.update()
