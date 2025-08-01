import tkinter as tk
from tkinter import ttk, scrolledtext, colorchooser
import threading
import time
import random
import json
import os

try:
    from playsound import playsound
except ImportError:
    playsound = None

config_file = "vpn_config.json"

settings = {
    "font_size": 10,
    "log_fg": "#00FF00",
    "random_connect": False,
    "auto_disconnect_time": 0,
    "rainbow_mode": False,
    "sound_effects": False,
    "stealth_mode": False,
    "dark_theme": True,
    "ping_monitor": False,
    "dns_leak_protection": True,
    "kill_switch": True,
    "split_tunneling": False,
    "speed_boost": False,
    "ads_blocker": True,
    "malware_protection": True,
    "custom_protocol": "UDP",
    "multi_hop": False,
    "anti_fingerprint": True,
    "obfuscation": False,
    "mobile_mode": False,
    "animated_transitions": True,
    "hover_tooltips": True
}

def load_config():
    if os.path.exists(config_file):
        with open(config_file, ' 'r') as f:
            data = json.load(f)
            settings.update(data.get("settings", {}))
            return data
    return {"is_premium": True}

def save_config():
    with open(config_file, 'w') as f:
        json.dump({"is_premium": is_premium, "settings": settings}, f)

is_connected = False
connected_country = None
config = load_config()
is_premium = config.get("is_premium", False)

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if not settings["hover_tooltips"]:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, background="#333", fg="white", relief="solid", borderwidth=1)
        label.pack()

    def hide_tip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

def log(message):
    if not settings["stealth_mode"]:
        log_text.insert(tk.END, message + "\n")
        log_text.see(tk.END)

def simulate_connect(country):
    global is_connected, connected_country
    if is_connected:
        log("Already connected.")
        return
    is_connected = True
    connected_country = country

    if settings["animated_transitions"]:
        for dot in "...":
            log(dot)
            time.sleep(0.3)

    log(f"Connecting to {country} using {settings['custom_protocol']} protocol...")

    if settings["ping_monitor"]:
        log(f"Ping: {random.randint(20, 150)}ms")
    if settings["dns_leak_protection"]:
        log("DNS Leak Protection is active.")
    if settings["kill_switch"]:
        log("Kill Switch armed.")
    if settings["split_tunneling"]:
        log("Split Tunneling enabled for: Chrome, Discord")
    if settings["speed_boost"]:
        log("Speed Boost engaged.")
    if settings["ads_blocker"]:
        log("Ad Blocker enabled.")
    if settings["malware_protection"]:
        log("Performing malware scan... Clean.")
    if settings["multi_hop"]:
        log("Routing via Netherlands -> India (Multi-Hop)")
    if settings["anti_fingerprint"]:
        log("Anti-Fingerprint mode active.")
    if settings["obfuscation"]:
        log("Obfuscating traffic...")
    if settings["mobile_mode"]:
        log("Mobile-optimized mode enabled.")
    if settings["sound_effects"] and playsound:
        try:
            playsound("connect.wav", block=False)
        except Exception as e:
            log(f"Sound error (connect): {e}")

    log(f"Connected to {country}")
    simulate_location_change(country)
    update_canvas()

    if settings["auto_disconnect_time"] > 0:
        threading.Thread(target=auto_disconnect_timer, daemon=True).start()

def simulate_disconnect():
    global is_connected, connected_country
    if not is_connected:
        log("Not connected.")
        return

    if settings["kill_switch"]:
        log("Kill switch triggered. Forcing disconnect.")
    log(f"Disconnecting from {connected_country}...")
    time.sleep(1)
    is_connected = False
    log(f"Disconnected from {connected_country}")
    connected_country = None
    update_canvas()
    if settings["sound_effects"] and playsound:
        try:
            playsound("disconnect.wav", block=False)
        except Exception as e:
            log(f"Sound error (disconnect): {e}")

def auto_disconnect_timer():
    time.sleep(settings["auto_disconnect_time"])
    simulate_disconnect()

def toggle_setting(key):
    settings[key] = not settings[key]
    log(f"Toggled {key}: {settings[key]}")

def choose_color():
    color = colorchooser.askcolor(title="Choose Log Text Color")[1]
    if color:
        settings["log_fg"] = color
        log_text.config(fg=color)

def open_settings():
    win = tk.Toplevel(root)
    win.title("Settings")
    win.configure(bg="#2c3e50")

    tk.Label(win, text="Font Size:", fg="white", bg="#2c3e50").pack()
    font_size = tk.Spinbox(win, from_=6, to=24)
    font_size.insert(0, settings["font_size"])
    font_size.pack()
    ToolTip(font_size, "Change the font size of the log text area")

    tk.Label(win, text="Auto-Disconnect (sec):", fg="white", bg="#2c3e50").pack()
    auto_disc = tk.Spinbox(win, from_=0, to=3600)
    auto_disc.insert(0, settings["auto_disconnect_time"])
    auto_disc.pack()
    ToolTip(auto_disc, "Time in seconds before auto-disconnect occurs (0 = disabled)")

    tk.Button(win, text="Choose Log Color", command=choose_color, bg="gray", fg="white").pack(pady=5)

    tooltip_descriptions = {
        "random_connect": "Automatically connect to a random server",
        "rainbow_mode": "Use random colors for map dots",
        "sound_effects": "Play connect/disconnect sound effects",
        "stealth_mode": "Hide logs and map labels",
        "dark_theme": "Use dark theme background",
        "ping_monitor": "Show fake ping time when connecting",
        "dns_leak_protection": "Enable DNS leak prevention logs",
        "kill_switch": "Force disconnect on trigger",
        "split_tunneling": "Log apps using VPN tunnel",
        "speed_boost": "Enable speed boost simulation",
        "ads_blocker": "Log ad blocker activation",
        "malware_protection": "Log malware scan simulation",
        "multi_hop": "Log traffic routing through multiple servers",
        "anti_fingerprint": "Log anti-tracking message",
        "obfuscation": "Simulate obfuscating VPN traffic",
        "mobile_mode": "Log mobile optimization message",
        "animated_transitions": "Add animation dots on connect",
        "hover_tooltips": "Show tooltips on hover"
    }

    for key in settings:
        if isinstance(settings[key], bool):
            var = tk.BooleanVar(value=settings[key])
            cb = tk.Checkbutton(
                win,
                text=key.replace('_', ' ').title(),
                variable=var,
                command=lambda k=key: toggle_setting(k),
                bg="#2c3e50",
                fg="white"
            )
            cb.pack(anchor='w', padx=10)
            ToolTip(cb, tooltip_descriptions.get(key, key))

    def apply():
        settings["font_size"] = int(font_size.get())
        settings["auto_disconnect_time"] = int(auto_disc.get())
        log_text.config(font=("Consolas", settings["font_size"]))
        save_config()
        win.destroy()

    tk.Button(win, text="Apply", command=apply, bg="#27ae60", fg="white").pack(pady=10)

def update_canvas():
    canvas.delete("all")
    for country, (x, y) in vpn_servers.items():
        color = f"#{random.randint(0,0xFFFFFF):06x}" if settings["rainbow_mode"] else "cyan" if connected_country == country else "lime"
        canvas.create_oval(x, y, x + 10, y + 10, fill=color)
        if not settings["stealth_mode"]:
            canvas.create_text(x + 15, y + 5, text=country, anchor="w", fill="white")

def show_random_connect():
    if is_connected:
        log("Already connected.")
        return
    country = random.choice(list(vpn_servers.keys()))
    log(f"Randomly selected {country} to connect.")
    simulate_connect(country)

def simulate_location_change(country):
    # Simulate location change message
    log(f"System location spoofed to {country} (simulated on macOS)")
    # Actual implementation would require elevated permissions + tools like `networksetup` or third-party VPNs

vpn_servers = {
    "USA": (80, 130), "Canada": (80, 60), "Brazil": (120, 260), "UK": (260, 80), "Germany": (290, 100),
    "Russia": (380, 70), "India": (420, 160), "China": (460, 120), "Japan": (520, 110), "Australia": (560, 260),
    "South Africa": (320, 280), "Egypt": (300, 170), "France": (270, 110), "Italy": (280, 130), "Spain": (250, 130),
    "Mexico": (60, 180), "Argentina": (130, 320), "South Korea": (500, 100), "Indonesia": (500, 200),
    "Turkey": (330, 140), "Sweden": (275, 70), "Norway": (260, 50), "Finland": (300, 50), "Poland": (310, 90),
    "Ukraine": (350, 100), "Saudi Arabia": (370, 170), "Thailand": (480, 170), "Vietnam": (490, 160),
    "Philippines": (510, 170)
}

# --- Loading Screen ---
def show_loading_screen():
    splash = tk.Tk()
    splash.attributes('-fullscreen', True)
    splash.configure(bg="black")
    label = tk.Label(splash, text="Loading S3CUR3 VPN...", font=("Helvetica", 36), fg="lime", bg="black")
    label.pack(expand=True)
    splash.after(3000, lambda: [splash.destroy(), start_main_gui()])
    splash.mainloop()

# --- Main GUI ---
def start_main_gui():
    global root, canvas, log_text

    root = tk.Tk()
    root.title("S3CUR3 VPN - VR & Laptop Compatible")
    root.geometry("900x600")
    root.configure(bg="#1e1e1e")

    top_frame = tk.Frame(root, bg="#1e1e1e")
    top_frame.pack(pady=5)

    server_var = tk.StringVar(value="USA")
    server_menu = ttk.Combobox(top_frame, textvariable=server_var, values=list(vpn_servers.keys()), state="readonly", width=20)
    server_menu.grid(row=0, column=0, padx=5)

    tk.Button(top_frame, text="Connect",
              command=lambda: threading.Thread(target=(show_random_connect if settings["random_connect"] else lambda: simulate_connect(server_var.get())), daemon=True).start(),
              bg="#2ecc71", fg="white", width=12).grid(row=0, column=1, padx=5)

    tk.Button(top_frame, text="Disconnect", command=lambda: threading.Thread(target=simulate_disconnect, daemon=True).start(),
              bg="#e74c3c", fg="white", width=12).grid(row=0, column=2, padx=5)

    tk.Button(top_frame, text="Settings", command=open_settings, bg="#3498db", fg="white", width=12).grid(row=0, column=3, padx=5)

    if is_premium:
        tk.Button(top_frame, text="Random Connect", command=lambda: threading.Thread(target=show_random_connect, daemon=True).start(),
                  bg="#8e44ad", fg="white", width=14).grid(row=0, column=4, padx=5)

    canvas = tk.Canvas(root, width=700, height=400, bg="#222")
    canvas.pack(pady=10)

    log_text = scrolledtext.ScrolledText(root, font=("Consolas", settings["font_size"]),
                                         fg=settings["log_fg"], bg="black", height=6)
    log_text.pack(fill=tk.BOTH, padx=10, pady=(0, 10), expand=False)

    log("Welcome to S3CUR3 VPN")
    if is_premium:
        log("Premium features enabled.")

    update_canvas()
    root.mainloop()

# --- Launch Program ---
show_loading_screen()

