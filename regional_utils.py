import subprocess
import winreg
import json
import os
import sys
import ctypes
import time
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
        self.game_config_file = os.path.join(self._get_app_dir(), "game_config.json")
        # Common locale display names for convenience
        self.locale_display_names = {
            "en-US": "United States",
        }
        # Minimal safe registry overrides for fast apply
        self.locale_registry_overrides = {
            "en-US": {
                "Locale": "00000409",  # LCID
                "LocaleName": "en-US",
                "iCountry": "1",
                "sCountry": "United States",
                "sCurrency": "$",
                "sShortDate": "M/d/yyyy",
                "sLongDate": "dddd, MMMM d, yyyy",
                "sTimeFormat": "h:mm:ss tt",
                "sShortTime": "h:mm tt",
                "sMonDecimalSep": ".",
                "sMonThousandSep": ",",
                "sDecimal": ".",
                "sThousand": ",",
                "iMeasure": "1",
                "iFirstDayOfWeek": "6",
                "iCalendarType": "1",
                "iDate": "0",
                "iTime": "0",
            }
            ,
            "de-DE": {
                "Locale": "00000407",  # LCID for German (Germany)
                "LocaleName": "de-DE",
                "iCountry": "49",
                "sCountry": "Germany",
                "sCurrency": "€",
                "sShortDate": "dd.MM.yyyy",
                "sLongDate": "dddd, d. MMMM yyyy",
                "sTimeFormat": "HH:mm:ss",
                "sShortTime": "HH:mm",
                "sMonDecimalSep": ",",
                "sMonThousandSep": ".",
                "sDecimal": ",",
                "sThousand": ".",
                "iMeasure": "0",
                "iFirstDayOfWeek": "0",
                "iCalendarType": "1",
                "iDate": "1",
                "iTime": "1",
            }
        }
        
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

    # --- FAST LIVE APPLY: change current user's regional format ---
    def _broadcast_setting_change(self):
        """Broadcast WM_SETTINGCHANGE to apply changes without reboot/logoff."""
        try:
            HWND_BROADCAST = 0xFFFF
            WM_SETTINGCHANGE = 0x001A
            SMTO_ABORTIFHUNG = 0x0002

            user32 = ctypes.windll.user32
            SendMessageTimeoutW = user32.SendMessageTimeoutW
            # LRESULT SendMessageTimeoutW(HWND hWnd, UINT Msg, WPARAM wParam, LPWSTR lParam, UINT fuFlags, UINT uTimeout, PDWORD_PTR lpdwResult)
            SendMessageTimeoutW.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_ulong)]
            SendMessageTimeoutW.restype = ctypes.c_void_p

            result = ctypes.c_ulong(0)
            SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, ctypes.c_wchar_p("intl"), SMTO_ABORTIFHUNG, 5000, ctypes.byref(result))
        except Exception as e:
            # Non-fatal; settings will still apply for most apps next launch
            print(f"Broadcast error: {e}")

    def apply_locale_quick(self, locale_name: str):
        """Quickly set current user's regional format to the given locale (e.g., 'en-US').

        Returns: (success: bool, message: str)
        """
        try:
            # Update HKCU regional format
            overrides = self.locale_registry_overrides.get(locale_name, {"LocaleName": locale_name})
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\International", 0, winreg.KEY_SET_VALUE) as key:
                for value_name, value_data in overrides.items():
                    winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, value_data)

            # Flush to registry (best-effort)
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\International", 0, winreg.KEY_READ) as key:
                    winreg.FlushKey(key)
            except Exception:
                pass

            # Broadcast change so many apps pick it up immediately
            self._broadcast_setting_change()

            # Short delay to let Windows apply changes
            time.sleep(0.3)

            # Verify with simple retry
            for _ in range(5):
                try:
                    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\International") as key:
                        applied = winreg.QueryValueEx(key, "LocaleName")[0]
                        if str(applied).lower() == locale_name.lower():
                            break
                except Exception:
                    pass
                time.sleep(0.4)

            # Also try using PowerShell to set culture and language list for broader coverage
            try:
                # Ensure language basic capability is present (best-effort)
                culture = locale_name
                basic_cap = f"Language.Basic~~~{culture}~0.0.1.0"
                ps_cmd = (
                    "$culture=\"" + culture + "\"; "
                    "$basic=\"Language.Basic~~~$culture~0.0.1.0\"; "
                    "$cap=Get-WindowsCapability -Online | Where-Object { $_.Name -eq $basic }; "
                    "if(-not $cap -or $cap.State -ne 'Installed'){ Add-WindowsCapability -Online -Name $basic | Out-Null }; "
                    f"Set-Culture -CultureInfo '{culture}'; "
                    "$list = New-Object System.Collections.Generic.List[System.String]; "
                    f"$list.Add('{culture}'); "
                    "Set-WinUserLanguageList -LanguageList $list -Force | Out-Null"
                )
                subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-Command", ps_cmd],
                               capture_output=True, text=True, shell=True, timeout=60)
            except Exception:
                # Best-effort; ignore failures here
                pass

            # Final delay to stabilize
            time.sleep(0.5)

            # Update in-memory current locale
            self.current_locale = locale_name
            return True, f"Regional format set to {locale_name}"
        except PermissionError:
            return False, "Permission denied. Please run as Administrator."
        except Exception as e:
            return False, f"Failed to set locale: {e}"

    def revert_to_default_quick(self):
        """Revert regional format to saved default locale from config."""
        try:
            target_locale = self.default_locale or self.load_config()
            if not target_locale:
                return False, "No default locale saved in configuration."
            return self.apply_locale_quick(target_locale)
        except Exception as e:
            return False, f"Failed to revert: {e}"

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

    # --- GAME PATH CONFIG ---
    def _get_app_dir(self):
        """Resolve a writable directory near the app for configs."""
        try:
            if getattr(sys, 'frozen', False):
                return os.path.dirname(sys.executable)
            return os.path.dirname(os.path.abspath(__file__))
        except Exception:
            return os.getcwd()

    def save_game_path(self, game_path: str):
        """Persist game path to separate config file."""
        try:
            data = {"game_path": game_path, "last_saved": datetime.now().isoformat()}
            with open(self.game_config_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving game path: {e}")

    def load_game_path(self):
        """Load game path from separate config file."""
        try:
            if os.path.exists(self.game_config_file):
                with open(self.game_config_file, 'r') as f:
                    data = json.load(f)
                    return data.get("game_path")
        except Exception as e:
            print(f"Error loading game path: {e}")
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
            
            # Launch the game with proper working directory to avoid black screen
            exe_dir = os.path.dirname(game_path)
            try:
                DETACHED_PROCESS = 0x00000008
                subprocess.Popen([game_path], cwd=exe_dir, shell=False, creationflags=DETACHED_PROCESS)
            except Exception:
                # Fallback via PowerShell Start-Process with WorkingDirectory
                ps_cmd = f"Start-Process -FilePath \"{game_path}\" -WorkingDirectory \"{exe_dir}\""
                subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-Command", ps_cmd],
                               capture_output=True, text=True, shell=True, timeout=15)
            return True, f"Game launched from: {os.path.dirname(game_path)}"
                
        except Exception as e:
            return False, f"Error launching game: {e}"
