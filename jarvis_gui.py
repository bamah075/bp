#!/usr/bin/env python3
"""
JARVIS GUI - Professional Voice AI Assistant Interface
Modern graphical interface with voice activation, status display, and real-time feedback
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
from datetime import datetime
from Brain.brain import process_command
from TextToSpeech.Fast_DF_TTS import speak
from internet_check import is_Online
import sys

class JARVISGui:
    def __init__(self, root):
        self.root = root
        self.root.title("J.A.R.V.I.S - Voice AI Assistant")
        self.root.geometry("900x700")
        self.root.configure(bg="#0a0e27")

        # Variables
        self.is_listening = False
        self.is_processing = False
        self.is_online = False
        self.command_thread = None

        self.setup_styles()
        self.create_widgets()
        self.update_online_status()

    def setup_styles(self):
        """Configure color scheme and styles"""
        style = ttk.Style()
        style.theme_use('clam')

        # Dark theme colors
        self.bg_dark = "#0a0e27"
        self.bg_card = "#1a1f3a"
        self.primary_color = "#00d9ff"
        self.accent_color = "#ff006e"
        self.success_color = "#06ffa5"
        self.warning_color = "#ffa500"
        self.text_color = "#ffffff"

        style.configure("Dark.TFrame", background=self.bg_dark)
        style.configure("Card.TFrame", background=self.bg_card)
        style.configure("Dark.TLabel", background=self.bg_dark, foreground=self.text_color)
        style.configure("Primary.TButton", background=self.primary_color, foreground="#000000")

    def create_widgets(self):
        """Create main GUI components"""
        # Main container
        main_frame = ttk.Frame(self.root, style="Dark.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        # Header
        self.create_header(main_frame)

        # Status section
        self.create_status_section(main_frame)

        # Display section
        self.create_display_section(main_frame)

        # Controls section
        self.create_controls_section(main_frame)

        # Footer
        self.create_footer(main_frame)

    def create_header(self, parent):
        """Create application header with title and status"""
        header_frame = tk.Frame(parent, bg="#0f1333", height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)

        # Logo and title
        title_frame = tk.Frame(header_frame, bg="#0f1333")
        title_frame.pack(side=tk.LEFT, padx=30, pady=20)

        logo_label = tk.Label(title_frame, text="🤖", font=("Arial", 40), bg="#0f1333")
        logo_label.pack(side=tk.LEFT, padx=(0, 15))

        title_label = tk.Label(
            title_frame,
            text="J.A.R.V.I.S",
            font=("Arial", 28, "bold"),
            bg="#0f1333",
            fg=self.primary_color
        )
        title_label.pack(side=tk.LEFT)

        subtitle_label = tk.Label(
            title_frame,
            text="Voice AI Assistant",
            font=("Arial", 10),
            bg="#0f1333",
            fg="#888888"
        )
        subtitle_label.pack(anchor=tk.W, padx=(55, 0))

        # Network status indicator
        status_frame = tk.Frame(header_frame, bg="#0f1333")
        status_frame.pack(side=tk.RIGHT, padx=30, pady=20)

        self.status_indicator = tk.Label(
            status_frame,
            text="●",
            font=("Arial", 16),
            bg="#0f1333",
            fg=self.warning_color
        )
        self.status_indicator.pack(side=tk.LEFT, padx=(0, 8))

        self.status_text = tk.Label(
            status_frame,
            text="Checking Connection...",
            font=("Arial", 10),
            bg="#0f1333",
            fg="#888888"
        )
        self.status_text.pack(side=tk.LEFT)

    def create_status_section(self, parent):
        """Create microphone and listening status display"""
        status_frame = ttk.Frame(parent, style="Card.TFrame", height=100)
        status_frame.pack(fill=tk.X, padx=20, pady=15)
        status_frame.pack_propagate(False)

        # Listening status
        status_inner = tk.Frame(status_frame, bg=self.bg_card)
        status_inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        status_label = tk.Label(
            status_inner,
            text="Status:",
            font=("Arial", 11, "bold"),
            bg=self.bg_card,
            fg=self.text_color
        )
        status_label.pack(anchor=tk.W)

        self.status_display = tk.Label(
            status_inner,
            text="🎤 Ready to listen",
            font=("Arial", 20, "bold"),
            bg=self.bg_card,
            fg=self.success_color
        )
        self.status_display.pack(anchor=tk.W, pady=(5, 0))

        # Microphone level
        level_label = tk.Label(
            status_inner,
            text="Microphone Level:",
            font=("Arial", 10),
            bg=self.bg_card,
            fg="#888888"
        )
        level_label.pack(anchor=tk.W, pady=(10, 5))

        self.level_canvas = tk.Canvas(
            status_inner,
            width=400,
            height=20,
            bg="#111111",
            highlightthickness=1,
            highlightbackground="#333333"
        )
        self.level_canvas.pack(anchor=tk.W)

        # Initial empty bar
        self.level_canvas.create_rectangle(0, 0, 0, 20, fill=self.primary_color, tags="level")

    def create_display_section(self, parent):
        """Create conversation display area"""
        display_frame = ttk.Frame(parent, style="Card.TFrame")
        display_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Title
        title = tk.Label(
            display_frame,
            text="Conversation History",
            font=("Arial", 12, "bold"),
            bg=self.bg_card,
            fg=self.primary_color
        )
        title.pack(anchor=tk.W, padx=15, pady=(15, 10))

        # Text display with scrollbar
        text_frame = tk.Frame(display_frame, bg=self.bg_card)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        self.text_display = scrolledtext.ScrolledText(
            text_frame,
            height=12,
            width=80,
            bg="#111111",
            fg=self.text_color,
            insertbackground=self.primary_color,
            font=("Courier", 10),
            wrap=tk.WORD,
            relief=tk.FLAT,
            borderwidth=0
        )
        self.text_display.pack(fill=tk.BOTH, expand=True)
        self.text_display.config(state=tk.DISABLED)

        # Configure tags for styling
        self.text_display.tag_config("user", foreground=self.primary_color, font=("Courier", 10, "bold"))
        self.text_display.tag_config("jarvis", foreground=self.success_color, font=("Courier", 10))
        self.text_display.tag_config("time", foreground="#666666", font=("Courier", 9))

    def create_controls_section(self, parent):
        """Create control buttons"""
        controls_frame = ttk.Frame(parent, style="Card.TFrame", height=80)
        controls_frame.pack(fill=tk.X, padx=20, pady=15)
        controls_frame.pack_propagate(False)

        button_frame = tk.Frame(controls_frame, bg=self.bg_card)
        button_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        # Listen button
        self.listen_button = tk.Button(
            button_frame,
            text="🎤 Listen",
            font=("Arial", 12, "bold"),
            bg=self.primary_color,
            fg="#000000",
            padx=30,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.start_listening
        )
        self.listen_button.pack(side=tk.LEFT, padx=5)

        # Stop button
        self.stop_button = tk.Button(
            button_frame,
            text="⏹ Stop",
            font=("Arial", 12, "bold"),
            bg="#555555",
            fg=self.text_color,
            padx=30,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.stop_listening,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Clear button
        clear_button = tk.Button(
            button_frame,
            text="🗑 Clear",
            font=("Arial", 12, "bold"),
            bg="#666666",
            fg=self.text_color,
            padx=30,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.clear_display
        )
        clear_button.pack(side=tk.LEFT, padx=5)

        # Settings button
        settings_button = tk.Button(
            button_frame,
            text="⚙ Settings",
            font=("Arial", 12, "bold"),
            bg="#666666",
            fg=self.text_color,
            padx=30,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.show_settings
        )
        settings_button.pack(side=tk.LEFT, padx=5)

    def create_footer(self, parent):
        """Create footer with version and info"""
        footer_frame = tk.Frame(parent, bg="#0f1333", height=40)
        footer_frame.pack(fill=tk.X, padx=0, pady=0)
        footer_frame.pack_propagate(False)

        footer_text = tk.Label(
            footer_frame,
            text="JARVIS v1.0 | Ready for voice commands | Python 3.9+",
            font=("Arial", 9),
            bg="#0f1333",
            fg="#666666"
        )
        footer_text.pack(side=tk.LEFT, padx=20, pady=10)

    def add_message(self, sender, text):
        """Add message to display"""
        self.text_display.config(state=tk.NORMAL)

        timestamp = datetime.now().strftime("%H:%M:%S")

        if sender == "user":
            self.text_display.insert(tk.END, f"[{timestamp}] ", "time")
            self.text_display.insert(tk.END, f"You: {text}\n", "user")
        else:
            self.text_display.insert(tk.END, f"[{timestamp}] ", "time")
            self.text_display.insert(tk.END, f"JARVIS: {text}\n", "jarvis")

        self.text_display.see(tk.END)
        self.text_display.config(state=tk.DISABLED)
        self.root.update()

    def clear_display(self):
        """Clear conversation display"""
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)
        self.text_display.config(state=tk.DISABLED)

    def update_level_bar(self, level):
        """Update microphone level visualization"""
        # level should be 0-100
        width = int((level / 100) * 400)
        self.level_canvas.coords("level", 0, 0, width, 20)
        self.root.update_idletasks()

    def update_status(self, message, color, is_listening=False):
        """Update status display"""
        emoji_map = {
            "listening": "🎤",
            "processing": "🧠",
            "speaking": "🔊",
            "ready": "✓"
        }

        emoji = emoji_map.get(message.lower().split()[0], "●")
        self.status_display.config(text=f"{emoji} {message}", fg=color)
        self.is_listening = is_listening
        self.root.update_idletasks()

    def update_online_status(self):
        """Check and update network status"""
        def check_status():
            try:
                online = is_Online()
                if online:
                    self.status_indicator.config(fg=self.success_color)
                    self.status_text.config(text="Online", fg=self.success_color)
                    self.is_online = True
                else:
                    self.status_indicator.config(fg=self.warning_color)
                    self.status_text.config(text="Offline", fg=self.warning_color)
                    self.is_online = False
            except:
                self.status_indicator.config(fg=self.warning_color)
                self.status_text.config(text="Offline", fg=self.warning_color)
                self.is_online = False

        thread = threading.Thread(target=check_status, daemon=True)
        thread.start()

        # Check again every 30 seconds
        self.root.after(30000, self.update_online_status)

    def start_listening(self):
        """Start listening for voice commands"""
        if self.is_processing:
            return

        self.update_status("Listening...", self.primary_color, is_listening=True)
        self.listen_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        # Simulate listening with animated level
        self.command_thread = threading.Thread(target=self.simulate_listening, daemon=True)
        self.command_thread.start()

    def simulate_listening(self):
        """Simulate voice input with level animation"""
        import random

        # In a real implementation, this would capture actual audio
        # For demo: simulate with random levels
        for i in range(30):
            if not self.is_listening:
                break

            level = random.randint(10, 60)
            self.update_level_bar(level)
            time.sleep(0.1)

        # Only process if still listening (not stopped by user)
        if self.is_listening:
            self.is_listening = False  # Stop listening before processing
            # Process simulated command
            self.process_voice_command("hello")

    def process_voice_command(self, command):
        """Process voice command and get response"""
        self.update_status("Processing...", self.accent_color)
        self.is_processing = True

        self.add_message("user", command)

        try:
            response = process_command(command)

            # Simulate processing time
            time.sleep(0.5)

            self.update_status("Speaking...", self.success_color)
            self.add_message("jarvis", response)

            # Speak the response
            speak(response)

            time.sleep(1)

        except Exception as e:
            error_msg = f"Error processing command: {str(e)}"
            self.add_message("jarvis", error_msg)

        finally:
            self.update_status("Ready to listen", self.success_color)
            self.is_processing = False
            self.listen_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.update_level_bar(0)

    def stop_listening(self):
        """Stop listening"""
        self.is_listening = False
        self.stop_button.config(state=tk.DISABLED)
        self.listen_button.config(state=tk.NORMAL)
        self.update_status("Ready to listen", self.success_color)
        self.update_level_bar(0)

    def show_settings(self):
        """Show settings window"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("JARVIS Settings")
        settings_window.geometry("400x300")
        settings_window.configure(bg=self.bg_dark)

        # Settings content
        settings_frame = tk.Frame(settings_window, bg=self.bg_dark)
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        title = tk.Label(
            settings_frame,
            text="Settings",
            font=("Arial", 16, "bold"),
            bg=self.bg_dark,
            fg=self.primary_color
        )
        title.pack(anchor=tk.W)

        # Settings options
        settings_options = [
            ("Voice Volume", "100%"),
            ("Microphone Input", "Default"),
            ("Response Speed", "Normal"),
            ("Theme", "Dark Mode"),
        ]

        for option, value in settings_options:
            frame = tk.Frame(settings_frame, bg=self.bg_dark)
            frame.pack(fill=tk.X, pady=10)

            label = tk.Label(
                frame,
                text=option + ":",
                font=("Arial", 10),
                bg=self.bg_dark,
                fg=self.text_color
            )
            label.pack(side=tk.LEFT)

            value_label = tk.Label(
                frame,
                text=value,
                font=("Arial", 10),
                bg=self.bg_dark,
                fg=self.primary_color
            )
            value_label.pack(side=tk.RIGHT)

        close_btn = tk.Button(
            settings_frame,
            text="Close",
            font=("Arial", 10),
            bg=self.primary_color,
            fg="#000000",
            padx=20,
            pady=8,
            relief=tk.FLAT,
            command=settings_window.destroy
        )
        close_btn.pack(pady=20)

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = JARVISGui(root)

    # Add welcome message
    app.add_message("jarvis", "Hello! I'm JARVIS, your personal AI assistant. Click 'Listen' to get started.")

    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[JARVIS] Shutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"[JARVIS Error] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
