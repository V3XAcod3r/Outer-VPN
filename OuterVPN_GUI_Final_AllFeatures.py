
import subprocess
import requests
import tkinter as tk
from tkinter import ttk, scrolledtext, colorchooser, filedialog
import threading, time, random, colorsys, math, os, datetime

# === SETTINGS ===
settings = {
    "rainbow_mode": True,
    "stealth_mode": False,
    "kill_switch": True,
    "auto_disconnect_time": 0,
    "anti_malware": True
}
is_connected = False
connected_country = None
rainbow_angle = 0
background_color = "#1e1e1e"
vpn_config_path = "/etc/openvpn/client.conf"
log_file = os.path.expanduser("~/outervpn_log.txt")

# === PROXIES ===
proxies = {
    "USA": "http://198.199.86.11:3128",
    "Germany": "http://138.201.223.250:31288",
    "France": "http://51.158.154.173:3128",
    "UK": "http://51.38.71.101:8080",
    "India": "http://103.169.186.57:3128",
    "Canada": "http://134.209.29.120:3128"
}
countries = list(proxies.keys())
vpn_servers = {c: (random.randint(50, 750), random.randint(50, 400)) for c in countries}
status_map = {c: random.choice(['green', 'yellow', 'red']) for c in countries}

# === LOGGING ===
def log(message):
    if not settings["stealth_mode"]:
        log_text.insert(tk.END, message + "\n")
        log_text.see(tk.END)
    with open(log_file, "a") as f:
        f.write(f"[{datetime.datetime.now()}] {message}\n")

# === NETWORK FUNCTIONS ===
def set_system_proxy(ip, port, service="Wi-Fi"):
    try:
        subprocess.run(["networksetup", "-setwebproxy", service, ip, port], check=True)
        subprocess.run(["networksetup", "-setsecurewebproxy", service, ip, port], check=True)
        subprocess.run(["networksetup", "-setwebproxystate", service, "on"], check=True)
        subprocess.run(["networksetup", "-setsecurewebproxystate", service, "on"], check=True)
        log(f"✅ Proxy set: {ip}:{port}")
    except Exception as e:
        log(f"❌ Failed to set proxy: {e}")

def unset_system_proxy(service="Wi-Fi"):
    try:
        subprocess.run(["networksetup", "-setwebproxystate", service, "off"], check=True)
        subprocess.run(["networksetup", "-setsecurewebproxystate", service, "off"], check=True)
        log("🔌 Proxy disabled")
    except Exception as e:
        log(f"❌ Failed to disable proxy: {e}")

def get_current_ip_info():
    try:
        r = requests.get("https://api.myip.com", timeout=10)
        data = r.json()
        log(f"🌍 IP: {data['ip']}\nCountry: {data['country']}")
    except:
        log("❌ Failed to fetch IP info")

def connect_vpn():
    def run_vpn():
        try:
            subprocess.run(["sudo", "openvpn", "--config", vpn_config_path])
            log("🔒 VPN connected.")
        except Exception as e:
            log(f"❌ VPN error: {e}")
    threading.Thread(target=run_vpn, daemon=True).start()

def stop_vpn():
    try:
        subprocess.run(["sudo", "killall", "openvpn"])
        log("🔓 VPN disconnected.")
    except Exception as e:
        log(f"❌ Stop VPN error: {e}")

def change_dns():
    try:
        subprocess.run(["networksetup", "-setdnsservers", "Wi-Fi", "1.1.1.1", "8.8.8.8"], check=True)
        log("🌐 DNS set to Cloudflare/Google")
    except Exception as e:
        log(f"❌ DNS error: {e}")

def select_vpn_config():
    global vpn_config_path
    file_path = filedialog.askopenfilename(filetypes=[("OVPN Files", "*.ovpn")])
    if file_path:
        vpn_config_path = file_path
        log(f"📁 VPN config selected: {vpn_config_path}")

# === GUI BUILD ===
def build_gui():
    global root, canvas, log_text, server_var
    root = tk.Tk()
    root.title("OuterVPN GUI")
    root.geometry("1000x720")
    root.configure(bg=background_color)

    top = tk.Frame(root, bg=background_color)
    top.pack(pady=10)

    server_var = tk.StringVar(value=countries[0])
    ttk.Combobox(top, textvariable=server_var, values=countries, width=30, state="readonly").grid(row=0, column=0, padx=5)

    tk.Button(top, text="Connect Proxy", command=connect_proxy, bg="#2ecc71", fg="white").grid(row=0, column=1, padx=5)
    tk.Button(top, text="Disconnect", command=disconnect_proxy, bg="#e74c3c", fg="white").grid(row=0, column=2, padx=5)
    tk.Button(top, text="Pick VPN Config", command=select_vpn_config, bg="#9b59b6", fg="white").grid(row=0, column=3, padx=5)
    tk.Button(top, text="Start VPN", command=connect_vpn, bg="#2980b9", fg="white").grid(row=0, column=4, padx=5)
    tk.Button(top, text="Stop VPN", command=stop_vpn, bg="#34495e", fg="white").grid(row=0, column=5, padx=5)
    tk.Button(top, text="Set DNS", command=change_dns, bg="#f39c12", fg="white").grid(row=0, column=6, padx=5)
    tk.Button(top, text="My IP", command=get_current_ip_info, bg="#27ae60", fg="white").grid(row=0, column=7, padx=5)
    tk.Button(top, text="Settings", command=open_settings, bg="#8e44ad", fg="white").grid(row=0, column=8, padx=5)

    canvas_container = tk.Frame(root)
    canvas_container.pack()
    global canvas
    canvas = tk.Canvas(canvas_container, width=900, height=400, bg="black")
    canvas.pack()

    global log_text
    log_text = scrolledtext.ScrolledText(root, font=("Consolas", 10), fg="#00FF00", bg="black", height=10)
    log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    log("✅ OuterVPN GUI Loaded.")
    update_canvas()
    animate_rainbow()
    root.mainloop()

# === SETTINGS WINDOW ===
def open_settings():
    win = tk.Toplevel(root)
    win.title("Settings")
    win.configure(bg="#2b2b2b")

    def toggle(key):
        settings[key] = not settings[key]
        log(f"{key.replace('_', ' ').title()} set to {settings[key]}")

    def update_disconnect_time(val):
        settings["auto_disconnect_time"] = int(val)
        log(f"Auto Disconnect Time set to {val} sec")

    def change_bg():
        global background_color
        c = colorchooser.askcolor(title="Choose background color")[1]
        if c:
            background_color = c
            root.configure(bg=c)
            log(f"Background color changed to {c}")

    for i, (label, key) in enumerate([
        ("Rainbow Mode", "rainbow_mode"),
        ("Stealth Mode", "stealth_mode"),
        ("Kill Switch", "kill_switch"),
        ("Anti-Malware", "anti_malware")
    ]):
        btn = tk.Checkbutton(win, text=label, variable=tk.BooleanVar(value=settings[key]),
                             command=lambda k=key: toggle(k), bg="#2b2b2b", fg="white", selectcolor="#3b3b3b")
        btn.grid(row=i, column=0, sticky="w", padx=10, pady=5)

    tk.Label(win, text="Auto Disconnect Time (sec)", bg="#2b2b2b", fg="white").grid(row=5, column=0, sticky="w", padx=10)
    scale = tk.Scale(win, from_=0, to=60, orient="horizontal", bg="#2b2b2b", fg="white",
                     highlightbackground="#2b2b2b", command=update_disconnect_time)
    scale.set(settings["auto_disconnect_time"])
    scale.grid(row=6, column=0, padx=10, pady=10)

    tk.Button(win, text="Change Background", command=change_bg, bg="#8e44ad", fg="white").grid(row=7, column=0, padx=10, pady=10)

# === RENDERING ===
def connect_proxy():
    global is_connected, connected_country
    if is_connected:
        log("Already connected.")
        return
    connected_country = server_var.get()
    is_connected = True
    ip, port = proxies[connected_country].replace("http://", "").split(":")
    set_system_proxy(ip, port)
    log(f"Connected to proxy in {connected_country}")
    update_canvas()

def disconnect_proxy():
    global is_connected, connected_country
    if not is_connected:
        log("Not connected.")
        return
    unset_system_proxy()
    log(f"Disconnected from {connected_country}")
    is_connected = False
    connected_country = None
    update_canvas()

def update_canvas():
    canvas.delete("all")
    for c, (x, y) in vpn_servers.items():
        color = get_rainbow_color() if settings["rainbow_mode"] else status_map[c]
        canvas.create_oval(x, y, x + 10, y + 10, fill=color, outline="")
        if not settings["stealth_mode"]:
            canvas.create_text(x + 15, y + 5, text=c, anchor="w", fill="white")
        if connected_country == c:
            canvas.create_rectangle(x - 2, y - 2, x + 12, y + 12, outline="cyan")

def get_rainbow_color():
    global rainbow_angle
    rainbow_angle = (rainbow_angle + 0.01) % 1
    r, g, b = colorsys.hsv_to_rgb(rainbow_angle, 1, 1)
    return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"

def animate_rainbow():
    if settings["rainbow_mode"]:
        update_canvas()
    root.after(100, animate_rainbow)

# === LOADING SCREEN ===
def show_loading_screen():
    splash = tk.Tk()
    splash.attributes("-fullscreen", True)
    canvas = tk.Canvas(splash, bg="black")
    canvas.pack(fill="both", expand=True)
    w = splash.winfo_screenwidth()
    h = splash.winfo_screenheight()
    cx, cy = w // 2, h // 2
    canvas.create_text(cx, cy, text="Outer VPN", fill="#b266ff", font=("Helvetica", 40, "bold"))

    squares = []
    for i in range(12):
        size = 50 + i * 40
        sq = canvas.create_rectangle(cx - size, cy - size, cx + size, cy + size, outline="#8000ff", width=2)
        squares.append(sq)

    def animate(step=0):
        if step > 60:
            splash.destroy()
            build_gui()
            return
        scale = 1 + 0.03 * math.sin(step * 0.2)
        for i, sq in enumerate(squares):
            size = (50 + i * 40) * scale
            canvas.coords(sq, cx - size, cy - size, cx + size, cy + size)
        splash.after(50, lambda: animate(step + 1))

    animate()
    splash.mainloop()

show_loading_screen()
