#!/usr/bin/env python3
"""
Maya GUI - Futuristic Edition
Full animated sci-fi experience with pulsing rings, waveform visualizer, and animated background
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
from datetime import datetime
from Brain.smart_brain import _smart_brain
from TextToSpeech.Fast_DF_TTS import speak
from internet_check import is_Online
import sys
import math
import random

class AnimatedCanvas(tk.Canvas):
    """Custom canvas for futuristic animations"""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.animations = []
        self.is_animating = False
        self.config(bg="#0a0e1e", highlightthickness=0)

    def draw_circuit_pattern(self):
        """Draw animated circuit board background"""
        w = self.winfo_width()
        h = self.winfo_height()

        if w < 2 or h < 2:
            return

        # Draw grid pattern
        spacing = 40
        for x in range(0, w, spacing):
            self.create_line(x, 0, x, h, fill="#001a4d", width=1, dash=(2, 2))
        for y in range(0, h, spacing):
            self.create_line(0, y, w, y, fill="#001a4d", width=1, dash=(2, 2))

        # Draw random circuit nodes
        for _ in range(8):
            x = random.randint(0, w)
            y = random.randint(0, h)
            self.create_oval(x-3, y-3, x+3, y+3, fill="#00d9ff", outline="#0088ff")

    def draw_pulsing_rings(self, cx, cy, radius, intensity=1.0):
        """Draw animated pulsing rings"""
        colors = ["#00d9ff", "#0088ff", "#001a4d"]
        for i, color in enumerate(colors):
            ring_radius = radius * (1 + i * 0.3)
            alpha = int(255 * (1 - intensity) * (1 - i * 0.3))
            self.create_oval(
                cx - ring_radius, cy - ring_radius,
                cx + ring_radius, cy + ring_radius,
                outline=color, width=2
            )

    def draw_waveform(self, x, y, width, height, values):
        """Draw animated waveform bars"""
        if not values:
            return

        bar_width = width // len(values)
        for i, val in enumerate(values):
            bar_height = height * min(val, 1.0)
            x_pos = x + i * bar_width
            self.create_rectangle(
                x_pos, y + height - bar_height,
                x_pos + bar_width - 2, y + height,
                fill="#00ff00", outline="#00d9ff"
            )

    def draw_glowing_core(self, cx, cy, size, glow_intensity):
        """Draw animated glowing core"""
        # Outer glow
        glow_colors = ["#001a4d", "#0044aa", "#00d9ff"]
        for i, color in enumerate(glow_colors):
            glow_size = size * (1 + i * 0.3 + glow_intensity * 0.2)
            self.create_oval(
                cx - glow_size, cy - glow_size,
                cx + glow_size, cy + glow_size,
                fill=color, outline=color
            )

        # Inner core
        self.create_oval(
            cx - size, cy - size,
            cx + size, cy + size,
            fill="#00d9ff", outline="#0088ff", width=3
        )

class MayaFuturistic:
    def __init__(self, root):
        self.root = root
        self.root.title("Maya - Intelligent Voice AI Assistant")
        self.root.geometry("1200x800")
        self.root.configure(bg="#0a0e27")

        # Variables
        self.is_listening = False
        self.is_processing = False
        self.is_online = False
        self.command_thread = None
        self.last_command = None
        self.waveform_values = [0] * 20
        self.pulse_phase = 0
        self.glow_intensity = 0

        self.setup_styles()
        self.create_widgets()
        self.update_online_status()
        self.animate()

    def setup_styles(self):
        """Configure robust dark mode color scheme"""
        style = ttk.Style()
        style.theme_use('clam')

        # Premium dark mode - carefully chosen for aesthetics and readability
        self.bg_dark = "#0a0e1e"           # Deep midnight blue (not pure black)
        self.bg_card = "#0f1428"           # Card background (slightly lighter)
        self.bg_header = "#050810"         # Header darker background
        self.primary_color = "#00d9ff"     # Bright cyan (not harsh)
        self.accent_color = "#00ffaa"      # Soft green accent
        self.success_color = "#00ff99"     # Success green
        self.warning_color = "#ffaa00"     # Warm orange
        self.text_color = "#f0f0f0"        # Off-white (easier on eyes than pure white)
        self.text_secondary = "#888888"    # Secondary text
        self.border_color = "#1a2540"      # Subtle borders

        style.configure("Dark.TFrame", background=self.bg_dark, relief=tk.FLAT)
        style.configure("Dark.TLabel", background=self.bg_dark, foreground=self.text_color)

    def create_widgets(self):
        """Create main GUI components"""
        main_frame = ttk.Frame(self.root, style="Dark.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        # Header
        self.create_header(main_frame)

        # Main content area with animation canvas
        content_frame = tk.Frame(main_frame, bg=self.bg_dark)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        # Left side - Animation canvas
        canvas_frame = tk.Frame(content_frame, bg=self.bg_dark)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))

        self.canvas = AnimatedCanvas(canvas_frame, width=400, height=300, bg="#0a0e27")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Right side - Status and conversation
        right_frame = tk.Frame(content_frame, bg=self.bg_dark)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Status section
        self.create_status_section(right_frame)

        # Conversation section
        self.create_conversation_section(right_frame)

        # Controls section
        self.create_controls_section(main_frame)

        # Footer
        self.create_footer(main_frame)

    def create_header(self, parent):
        """Create application header"""
        header_frame = tk.Frame(parent, bg=self.bg_header, height=85)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)

        title_frame = tk.Frame(header_frame, bg=self.bg_header)
        title_frame.pack(side=tk.LEFT, padx=30, pady=20)

        logo_label = tk.Label(title_frame, text="✨", font=("Arial", 36), bg=self.bg_header)
        logo_label.pack(side=tk.LEFT, padx=(0, 15))

        title_label = tk.Label(
            title_frame,
            text="Maya",
            font=("Arial", 34, "bold"),
            bg=self.bg_header,
            fg=self.primary_color
        )
        title_label.pack(side=tk.LEFT)

        subtitle_label = tk.Label(
            title_frame,
            text="Intelligent AI Assistant for bamah",
            font=("Arial", 11),
            bg=self.bg_header,
            fg=self.text_secondary
        )
        subtitle_label.pack(anchor=tk.W, padx=(20, 0))

        status_frame = tk.Frame(header_frame, bg=self.bg_header)
        status_frame.pack(side=tk.RIGHT, padx=30, pady=20)

        self.status_indicator = tk.Label(
            status_frame,
            text="●",
            font=("Arial", 16),
            bg=self.bg_header,
            fg=self.warning_color
        )
        self.status_indicator.pack(side=tk.LEFT, padx=(0, 8))

        self.status_text = tk.Label(
            status_frame,
            text="Initializing...",
            font=("Arial", 10),
            bg=self.bg_header,
            fg=self.text_secondary
        )
        self.status_text.pack(side=tk.LEFT)

    def create_status_section(self, parent):
        """Create status display"""
        status_frame = tk.Frame(parent, bg=self.bg_card, relief=tk.FLAT)
        status_frame.pack(fill=tk.X, padx=10, pady=(0, 15))

        status_inner = tk.Frame(status_frame, bg=self.bg_card)
        status_inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

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
            font=("Arial", 18, "bold"),
            bg=self.bg_card,
            fg=self.success_color
        )
        self.status_display.pack(anchor=tk.W, pady=(5, 0))

    def create_conversation_section(self, parent):
        """Create conversation display"""
        conv_frame = tk.Frame(parent, bg=self.bg_card)
        conv_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        title = tk.Label(
            conv_frame,
            text="Conversation",
            font=("Arial", 12, "bold"),
            bg=self.bg_card,
            fg=self.primary_color
        )
        title.pack(anchor=tk.W, padx=15, pady=(15, 10))

        text_frame = tk.Frame(conv_frame, bg=self.bg_card)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        self.text_display = scrolledtext.ScrolledText(
            text_frame,
            height=8,
            width=40,
            bg="#070b18",
            fg=self.text_color,
            font=("Menlo", 10),
            wrap=tk.WORD,
            relief=tk.FLAT,
            borderwidth=0,
            padx=12,
            pady=10,
            insertbackground=self.primary_color
        )
        self.text_display.pack(fill=tk.BOTH, expand=True)
        self.text_display.config(state=tk.DISABLED)

        self.text_display.tag_config("user", foreground=self.primary_color, font=("Menlo", 10, "bold"))
        self.text_display.tag_config("jarvis", foreground=self.success_color, font=("Menlo", 10))
        self.text_display.tag_config("time", foreground=self.text_secondary, font=("Menlo", 9))

    def create_controls_section(self, parent):
        """Create control buttons"""
        controls_frame = tk.Frame(parent, bg=self.bg_card, height=80)
        controls_frame.pack(fill=tk.X, padx=20, pady=15)
        controls_frame.pack_propagate(False)

        button_frame = tk.Frame(controls_frame, bg=self.bg_card)
        button_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

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

    def create_footer(self, parent):
        """Create footer"""
        footer_frame = tk.Frame(parent, bg=self.bg_header, height=45)
        footer_frame.pack(fill=tk.X, padx=0, pady=0)
        footer_frame.pack_propagate(False)

        footer_text = tk.Label(
            footer_frame,
            text="Maya v1.0 | Intelligent AI Assistant with Beautiful Dark Mode",
            font=("Arial", 9),
            bg=self.bg_header,
            fg=self.text_secondary
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
            self.text_display.insert(tk.END, f"Maya: {text}\n", "jarvis")

        self.text_display.see(tk.END)
        self.text_display.config(state=tk.DISABLED)

    def clear_display(self):
        """Clear conversation"""
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)
        self.text_display.config(state=tk.DISABLED)

    def update_status(self, message, color):
        """Update status display"""
        emoji_map = {
            "listening": "🎤",
            "processing": "🧠",
            "speaking": "🔊",
            "ready": "✓"
        }

        emoji = emoji_map.get(message.lower().split()[0], "●")
        self.status_display.config(text=f"{emoji} {message}", fg=color)

    def update_online_status(self):
        """Check network status"""
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
        self.root.after(30000, self.update_online_status)

    def start_listening(self):
        """Start listening"""
        if self.is_processing or self.is_listening:
            return

        self.is_listening = True
        self.update_status("Listening...", self.primary_color)
        self.listen_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.command_thread = threading.Thread(target=self.simulate_listening, daemon=True)
        self.command_thread.start()

    def simulate_listening(self):
        """Simulate voice input with animations"""
        import random

        for i in range(30):
            if not self.is_listening:
                break

            # Update waveform
            self.waveform_values = [random.random() * random.random() for _ in range(20)]
            time.sleep(0.1)

        if self.is_listening:
            self.is_listening = False
            # Varied test commands that showcase Maya capabilities
            test_commands = [
                "hello",
                "what can you do",
                "help",
                "what system am i on",
                "what time is it",
                "tell me a joke",
                "tell me a fact",
                "what's my network info",
                "tell me something interesting",
                "hi there"
            ]
            available_commands = [cmd for cmd in test_commands if cmd != self.last_command]
            if not available_commands:
                available_commands = test_commands
            command = random.choice(available_commands)
            self.last_command = command
            self.process_voice_command(command)

    def process_voice_command(self, command):
        """Process command with smart brain"""
        self.update_status("Processing...", self.accent_color)
        self.is_processing = True

        self.add_message("user", command)

        try:
            response = _smart_brain.process_command(command)
            time.sleep(0.5)

            self.update_status("Speaking...", self.success_color)
            self.add_message("jarvis", response)
            speak(response)
            time.sleep(1)

        except Exception as e:
            self.add_message("jarvis", f"Error: {str(e)}")

        finally:
            self.update_status("Ready to listen", self.success_color)
            self.is_processing = False
            self.listen_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.waveform_values = [0] * 20

    def stop_listening(self):
        """Stop listening"""
        self.is_listening = False
        self.stop_button.config(state=tk.DISABLED)
        self.listen_button.config(state=tk.NORMAL)
        self.update_status("Ready to listen", self.success_color)
        self.waveform_values = [0] * 20

    def animate(self):
        """Main animation loop"""
        try:
            self.canvas.delete("all")

            # Draw background
            self.canvas.draw_circuit_pattern()

            w = self.canvas.winfo_width()
            h = self.canvas.winfo_height()

            if w > 50 and h > 50:
                cx, cy = w // 2, h // 2

                if self.is_listening:
                    # Pulsing rings when listening
                    self.pulse_phase = (self.pulse_phase + 0.1) % (2 * math.pi)
                    intensity = (math.sin(self.pulse_phase) + 1) / 2
                    self.canvas.draw_glowing_core(cx, cy, 40, intensity)
                    self.canvas.draw_pulsing_rings(cx, cy, 80, intensity)

                    # Waveform
                    self.canvas.draw_waveform(cx - 100, cy + 100, 200, 50, self.waveform_values)

                elif self.is_processing:
                    # Spinning glow when processing
                    self.glow_intensity = (self.glow_intensity + 0.05) % 1.0
                    self.canvas.draw_glowing_core(cx, cy, 40, self.glow_intensity)

                else:
                    # Calm glow when ready
                    self.canvas.draw_glowing_core(cx, cy, 30, 0.3)

        except tk.TclError:
            pass

        self.root.after(50, self.animate)

def main():
    """Main entry point"""
    root = tk.Tk()
    app = MayaFuturistic(root)
    app.add_message("jarvis", "Maya initialized. Click '🎤 Listen' to begin. Try saying 'hello', 'what can you do', or 'add task'.")

    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[Maya] Shutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"[Maya Error] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
