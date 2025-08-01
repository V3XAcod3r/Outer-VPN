import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
import platform
import random
import colorsys

# =====================
# Global State & Config
# =====================

settings = {
    "stealth_mode": False,
    "rainbow_mode": True,
    "kill_switch": True,
    "ad_blocker": True,
    "ping_monitor": True,
    "split_tunneling": True,
    "anti_fingerprint": True,
    "mobile_mode": False,
    "dark_theme": True,
    "auto_disconnect_time": 0,
    "multi_hop": True,
    "speed_boost": True,
    "obfuscation": True
}

is_connected = False
connected_country = None
root = None
log_text = None
canvas = None
vpn_servers = {}
status_map = {}
rainbow_angle = 0

# =====================
# Server Definitions
# =====================

def load_vpn_servers():
    countries = [
        "USA", "Germany", "India", "UK", "Canada", "France", "Japan", "Brazil", "Australia", "Russia",
        "Spain", "Italy", "Mexico", "China", "Netherlands", "Poland", "Sweden", "Norway", "Finland",
        "Argentina", "South Korea", "Indonesia", "Vietnam", "Thailand", "Malaysia", "Philippines",
        "Turkey", "Ukraine", "Egypt", "South Africa", "Singapore", "Saudi Arabia", "UAE", "Chile",
        "Israel", "Ireland", "New Zealand", "Pakistan", "Bangladesh", "Colombia", "Kenya", "Morocco"
    ]
    # Positioning is fake for demo purposes
    return {country: (random.randint(50, 650), random.randint(50, 350)) for country in countries}

vpn_servers = load_vpn_servers()
status_map = {country: random.choice(['green', 'yellow', 'red']) for country in vpn_servers}

# =====================
# GUI and Logic
# =====================

def show_loading_screen():
    splash = tk.Tk()
    splash.attributes('-fullscreen', True)
    canvas = tk.Canvas(splash, bg="black")
    canvas.pack(fill=tk.BOTH, expand=True)

    radius = 100
    dots = []
    for i in range(12):
        angle = i * (360 / 12)
        x = 450 + radius * math.cos(math.radians(angle))
        y = 300 + radius * math.sin(math.radians(angle))
        dot = canvas.create_oval(x, y, x+10, y+10, fill="#8000ff", outline="")
        dots.append(dot)

    def animate():
        for i in range(30):
            for idx, dot in enumerate(dots):
                scale = 1.2 if i % 2 == 0 else 0.8
                canvas.scale(dot, 450, 300, scale, scale)
            splash.update()
            time.sleep(0.1)
        splash.destroy()
        build_main_gui()

    threading.Thread(target=animate).start()
    splash.mainloop()

def build_main_gui():
    global root, log_text, server_var, canvas

    root = tk.Tk()
    root.title("OuterVPN Full Visual Edition")
    root.geometry("1000x700")
    root.configure(bg="#1e1e1e")

    frame = tk.Frame(root, bg="#1e1e1e")
    frame.pack(pady=5)

    server_var = tk.StringVar(value=list(vpn_servers.keys())[0])
    combo = ttk.Combobox(frame, textvariable=server_var, values=list(vpn_servers.keys()), width=30)
    combo.grid(row=0, column=0, padx=5)

    tk.Button(frame, text="Connect", command=connect, bg="#2ecc71", fg="white", width=12).grid(row=0, column=1, padx=5)
    tk.Button(frame, text="Disconnect", command=disconnect, bg="#e74c3c", fg="white", width=12).grid(row=0, column=2, padx=5)
    tk.Button(frame, text="Settings", command=open_settings, bg="#3498db", fg="white", width=12).grid(row=0, column=3, padx=5)

    canvas = tk.Canvas(root, width=800, height=400, bg="black")
    canvas.pack(pady=10)

    log_text = scrolledtext.ScrolledText(root, font=("Consolas", 10), fg="#00FF00", bg="black", height=10)
    log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    log("Welcome to OuterVPN Visual Edition!")
    update_canvas()
    animate_rainbow()
    root.mainloop()

def connect():
    global is_connected, connected_country
    if is_connected:
        log("Already connected.")
        return
    country = server_var.get()
    connected_country = country
    is_connected = True
    log(f"Connecting to {country}...")

    # Simulated Features
    if settings["ping_monitor"]:
        log(f"Ping: {random.randint(20, 150)}ms")
    if settings["ad_blocker"]:
        log("Ad Blocker: Active")
    if settings["anti_fingerprint"]:
        log("Anti-Fingerprint: Enabled")
    if settings["multi_hop"]:
        log("Routing via Netherlands → India")
    if settings["speed_boost"]:
        log("Speed Boost Engaged")
    if settings["obfuscation"]:
        log("Obfuscation Active")
    if settings["split_tunneling"]:
        log("Split Tunneling: Chrome and Discord routed")
    if settings["auto_disconnect_time"] > 0:
        threading.Thread(target=auto_disconnect_timer, daemon=True).start()

    log(f"Connected to {country}")
    update_canvas()
    log("❗Note:")
    log("These proxies are public and unstable. Some may go offline.")

def disconnect():
    global is_connected, connected_country
    if not is_connected:
        log("Not connected.")
        return
    log(f"Disconnecting from {connected_country}")
    connected_country = None
    is_connected = False
    update_canvas()
    log("Disconnected.")

def auto_disconnect_timer():
    time.sleep(settings["auto_disconnect_time"])
    disconnect()

def update_canvas():
    canvas.delete("all")
    for country, (x, y) in vpn_servers.items():
        color = get_rainbow_color() if settings["rainbow_mode"] else status_map[country]
        canvas.create_oval(x, y, x+10, y+10, fill=color, outline="")
        if not settings["stealth_mode"]:
            canvas.create_text(x + 15, y + 5, text=country, anchor="w", fill="white")
        if connected_country == country:
            canvas.create_rectangle(x-2, y-2, x+12, y+12, outline="cyan")

def get_rainbow_color():
    global rainbow_angle
    rainbow_angle = (rainbow_angle + 0.02) % 1
    rgb = colorsys.hsv_to_rgb(rainbow_angle, 1, 1)
    return "#%02x%02x%02x" % (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))

def animate_rainbow():
    if settings["rainbow_mode"]:
        update_canvas()
    root.after(100, animate_rainbow)

def open_settings():
    win = tk.Toplevel(root)
    win.title("Settings")
    win.configure(bg="#2c3e50")

    for k in settings:
        if isinstance(settings[k], bool):
            var = tk.BooleanVar(value=settings[k])
            cb = tk.Checkbutton(win, text=k.replace('_', ' ').title(), variable=var,
                                command=lambda key=k, v=var: toggle_setting(key, v),
                                bg="#2c3e50", fg="white")
            cb.pack(anchor="w", padx=10)

    tk.Label(win, text="Auto-Disconnect Time (sec):", bg="#2c3e50", fg="white").pack()
    spin = tk.Spinbox(win, from_=0, to=600)
    spin.delete(0, tk.END)
    spin.insert(0, settings["auto_disconnect_time"])
    spin.pack()

    def apply_time():
        settings["auto_disconnect_time"] = int(spin.get())
        log("Auto-Disconnect Time updated.")

    tk.Button(win, text="Apply", command=apply_time, bg="#27ae60", fg="white").pack(pady=5)

def toggle_setting(key, var):
    settings[key] = var.get()
    log(f"{key.replace('_', ' ').title()} set to {settings[key]}")

def log(message):
    if not settings["stealth_mode"]:
        log_text.insert(tk.END, message + "\n")
        log_text.see(tk.END)

import math
show_loading_screen()