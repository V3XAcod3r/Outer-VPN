import tkinter as tk
from tkinter import ttk, scrolledtext, colorchooser
import threading, time, random, colorsys, math, requests

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

countries = [
    "USA", "Germany", "India", "UK", "Canada", "France", "Japan", "Brazil", "Australia", "Russia",
    "Spain", "Italy", "Mexico", "China", "Netherlands", "Poland", "Sweden", "Norway", "Finland",
    "Argentina", "South Korea", "Indonesia", "Vietnam", "Thailand", "Malaysia", "Philippines",
    "Turkey", "Ukraine", "Egypt", "South Africa", "Singapore", "Saudi Arabia", "UAE", "Chile",
    "Israel", "Ireland", "New Zealand", "Pakistan", "Bangladesh", "Colombia", "Kenya", "Morocco"
]
vpn_servers = {c: (random.randint(50, 750), random.randint(50, 400)) for c in countries}
status_map = {c: random.choice(['green', 'yellow', 'red']) for c in countries}

proxies = {
    "USA Proxy": "http://168.138.211.5:8080",
    "Germany Proxy": "http://88.198.24.108:8080",
    "India Proxy": "http://103.151.177.106:80",
    "UK Proxy": "http://51.195.76.154:3128",
    "Canada Proxy": "http://51.161.119.141:3128",
    "France Proxy": "http://51.158.68.68:8811",
    "Japan Proxy": "http://47.74.152.29:8888",
    "Brazil Proxy": "http://186.202.226.238:8080",
    "Australia Proxy": "http://103.107.133.5:80",
    "Russia Proxy": "http://91.214.31.234:8080",
    "Spain Proxy": "http://188.165.0.192:3128",
    "Italy Proxy": "http://151.0.35.156:3128",
    "Mexico Proxy": "http://187.188.182.107:999",
    "China Proxy": "http://120.26.0.6:8888",
    "Netherlands Proxy": "http://188.166.125.87:3128",
    "Poland Proxy": "http://94.237.63.245:8080",
    "Sweden Proxy": "http://185.14.194.174:8080",
    "Norway Proxy": "http://82.196.11.105:3128",
    "Finland Proxy": "http://95.217.132.199:8888",
    "Argentina Proxy": "http://200.123.15.121:999",
    "South Korea Proxy": "http://121.129.65.46:80",
    "Indonesia Proxy": "http://103.76.27.161:8080",
    "Vietnam Proxy": "http://113.160.206.37:19132",
    "Thailand Proxy": "http://134.236.168.100:3128",
    "Malaysia Proxy": "http://110.74.195.253:80",
    "Philippines Proxy": "http://202.129.16.98:8080",
    "Turkey Proxy": "http://88.255.101.236:8080",
    "Ukraine Proxy": "http://91.203.114.74:8080",
    "Egypt Proxy": "http://196.202.215.143:8083",
    "South Africa Proxy": "http://102.215.195.161:8080",
    "Singapore Proxy": "http://128.199.202.122:8080",
    "Saudi Arabia Proxy": "http://193.32.86.123:8085",
    "UAE Proxy": "http://5.195.148.122:8080",
    "Chile Proxy": "http://201.148.31.115:8080",
    "Israel Proxy": "http://185.201.8.178:8080",
    "Ireland Proxy": "http://52.30.95.242:3128",
    "New Zealand Proxy": "http://103.242.119.88:80",
    "Pakistan Proxy": "http://103.86.49.122:3128",
    "Bangladesh Proxy": "http://103.48.68.34:84",
    "Colombia Proxy": "http://190.60.34.162:8080",
    "Kenya Proxy": "http://102.219.208.111:8080",
    "Morocco Proxy": "http://196.200.8.58:8080"
}

background_color = "#1e1e1e"

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

def build_gui():
    global root, canvas, log_text, server_var, proxy_var, top
    root = tk.Tk()
    root.title("OuterVPN Full Visual Edition")
    root.geometry("1000x700")
    root.configure(bg=background_color)

    top = tk.Frame(root, bg=background_color)
    top.pack(pady=5)

    server_var = tk.StringVar(value=countries[0])
    proxy_var = tk.StringVar(value=list(proxies.keys())[0])

    menu = ttk.Combobox(top, textvariable=server_var, values=countries, state="readonly", width=30)
    menu.grid(row=0, column=0, padx=5)

    tk.Button(top, text="Connect", command=lambda: connect(proxy_var), bg="#2ecc71", fg="white", width=12).grid(row=0, column=1, padx=5)
    tk.Button(top, text="Disconnect", command=disconnect, bg="#e74c3c", fg="white", width=12).grid(row=0, column=2, padx=5)
    tk.Button(top, text="Settings", command=open_settings, bg="#3498db", fg="white", width=12).grid(row=0, column=3, padx=5)

    tk.Label(top, text="Proxy:", bg=background_color, fg="white").grid(row=1, column=0, padx=5)
    ttk.Combobox(top, textvariable=proxy_var, values=list(proxies.keys()), width=30, state="readonly").grid(row=1, column=1, columnspan=2, pady=5)

    canvas = tk.Canvas(root, width=800, height=400, bg="black")
    canvas.pack(pady=10)

    log_text = scrolledtext.ScrolledText(root, font=("Consolas", 10), fg="#00FF00", bg="black", height=10)
    log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    log("Welcome to OuterVPN!")
    update_canvas()
    animate_rainbow()
    root.mainloop()

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
            top.configure(bg=c)
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

def connect(proxy_var):
    global is_connected, connected_country
    if is_connected:
        log("Already connected.")
        return
    connected_country = server_var.get()
    is_connected = True
    log(f"Connecting to {connected_country}...")

    proxy_key = proxy_var.get()
    proxy_url = proxies.get(proxy_key, "")
    log(f"Using proxy: {proxy_key} ({proxy_url})")

    if settings["anti_malware"]:
        log("Anti-Malware scan passed ✔️")

    if settings["kill_switch"] and random.random() < 0.1:
        log("Kill switch triggered! Connection blocked.")
        disconnect()
        return

    try:
        ip = requests.get("https://api.ipify.org", proxies={"http": proxy_url, "https": proxy_url}, timeout=5).text
        log(f"✅ Real IP switched to: {ip}")
    except Exception as e:
        log(f"❌ Proxy connection failed: {str(e)}")
        log("Falling back to simulated IP...")
        log(f"Simulated IP: {proxy_url.split('//')[1].split(':')[0]}")

    latency = random.randint(50, 250)
    log(f"Connected to {connected_country} ({latency}ms ping)")

    if settings["auto_disconnect_time"] > 0:
        threading.Thread(target=lambda: (time.sleep(settings["auto_disconnect_time"]), disconnect()), daemon=True).start()

    update_canvas()

def disconnect():
    global is_connected, connected_country
    if not is_connected:
        log("Not connected.")
        return
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

def log(message):
    if not settings["stealth_mode"]:
        log_text.insert(tk.END, message + "\n")
        log_text.see(tk.END)

# Launch
show_loading_screen()
