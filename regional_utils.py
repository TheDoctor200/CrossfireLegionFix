import subprocess
import winreg
import json
import os
import sys
import ctypes
from datetime import datetime

# --- ADMIN CHECK AND RELAUNCH ---
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == "__main__":
    if not is_admin():
        # Relaunch as admin
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join([f'"{arg}"' for arg in sys.argv]), None, 1
        )
        sys.exit(0)
# --- END ADMIN CHECK ---

class RegionalFormatChanger:
    def __init__(self):
        self.default_locale = None
        self.current_locale = None
        self.config_file = "region_config.json"
        
    def get_current_locale(self):
        """Get current Windows locale/regional format from Windows Settings (via Registry)"""
        try:
            # Primary method: Get from Windows Settings via Registry
            # This reads the same values that Windows Settings displays
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                              r"Control Panel\International") as key:
                # Get the locale name (e.g., "en-US")
                locale_name = winreg.QueryValueEx(key, "LocaleName")[0]
                
                # Get additional regional format info
                try:
                    # Get the format string (e.g., "English (United States)")
                    format_string = winreg.QueryValueEx(key, "sCountry")[0]
                except:
                    format_string = ""
                
                # Return comprehensive regional format info
                if locale_name:
                    return {
                        "locale": locale_name,
                        "country": format_string
                    }
                
        except Exception as e:
            print(f"Error reading from Registry: {e}")
        
        # Fallback method using PowerShell (less reliable but backup)
        try:
            result = subprocess.run([
                "powershell", "-Command", 
                "Get-WinSystemLocale | Select-Object -ExpandProperty Name"
            ], capture_output=True, text=True, shell=True)
            
            if result.returncode == 0:
                locale = result.stdout.strip()
                if locale:
                    return {"locale": locale, "country": ""}
        except Exception as e:
            print(f"Error using PowerShell fallback: {e}")
        
        return {"locale": "Unknown", "country": ""}
    
    def set_locale_to_en_us(self):
        """Open Windows Settings to Region page for user to set EN-US live"""
        try:
            # Open Windows Settings to Region page
            os.system('start ms-settings:regionlanguage')
            return True
        except Exception as e:
            print(f"Error opening Settings: {e}")
            return False

    def save_config(self):
        """Save configuration to file"""
        config = {
            "default_locale": self.default_locale,
            "last_saved": datetime.now().isoformat()
        }
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    return config.get("default_locale")
        except Exception as e:
            print(f"Error loading config: {e}")
        return None

    def launch_crossfire_legion(self):
        """Launch Crossfire: Legion via Steam"""
        try:
            # Get Steam install path from registry
            steam_path = None
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                  r"SOFTWARE\WOW6432Node\Valve\Steam") as key:
                    steam_path = winreg.QueryValueEx(key, "InstallPath")[0]
            except:
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                      r"SOFTWARE\Valve\Steam") as key:
                        steam_path = winreg.QueryValueEx(key, "InstallPath")[0]
                except:
                    pass
            
            if not steam_path:
                # Try current user registry
                try:
                    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                      r"SOFTWARE\Valve\Steam") as key:
                        steam_path = winreg.QueryValueEx(key, "SteamPath")[0]
                except:
                    pass
            
            if steam_path:
                # Try launching via Steam
                steam_exe = os.path.join(steam_path, "Steam.exe")
                if os.path.exists(steam_exe):
                    subprocess.Popen([steam_exe, "-applaunch", "1072190"], shell=True)
                    return True, "Launching via Steam..."
                else:
                    return False, "Steam executable not found"
            else:
                return False, "Steam installation not found in registry"
                
        except Exception as e:
            return False, f"Error launching via Steam: {e}"

    def launch_manual_path(self, game_path):
        """Launch Crossfire: Legion from manually specified path"""
        try:
            if not game_path or not os.path.exists(game_path):
                return False, "Invalid game path specified"
            
            # Check if it's the correct executable
            if not game_path.lower().endswith('crossfire_legion.exe'):
                return False, "Path must point to Crossfire_Legion.exe"
            
            # Launch the game
            subprocess.Popen([game_path], shell=True)
            return True, f"Game launched from: {os.path.dirname(game_path)}"
                
        except Exception as e:
            return False, f"Error launching game: {e}"
