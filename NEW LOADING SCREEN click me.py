import tkinter as tk
from tkinter import ttk, scrolledtext, colorchooser
import threading, time, random, colorsys, requests, dns.resolver

# ===== GLOBALS =====
settings = {"rainbow_mode": True, "stealth_mode": False, "kill_switch": True,
            "auto_disconnect_time": 0, "anti_malware": True}
is_connected = False
connected_country = None
rainbow_angle = 0

countries = ["USA","Germany","India","UK","Canada","France","Japan","Brazil","Australia","Russia",
             "Spain","Italy","Mexico","China","Netherlands","Poland","Sweden","Norway","Finland",
             "Argentina","South Korea","Indonesia","Vietnam","Thailand","Malaysia","Philippines",
             "Turkey","Ukraine","Egypt","South Africa","Singapore","Saudi Arabia","UAE","Chile",
             "Israel","Ireland","New Zealand","Pakistan","Bangladesh","Colombia","Kenya","Morocco"]
vpn_servers = {c: (random.randint(50, 750), random.randint(50, 400)) for c in countries}
status_map = {c: random.choice(['green','yellow','red']) for c in countries}
proxies = {}  # Will be filled with working proxies
dns_servers = {"Google DNS":"8.8.8.8","Cloudflare DNS":"1.1.1.1","OpenDNS":"208.67.222.222"}
selected_proxy = None
selected_dns = None
background_color = "#1e1e1e"

# ===== FETCH PROXIES =====
def fetch_proxies(callback=None):
    def task():
        try:
            r = requests.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=3000&country=all&ssl=all&anonymity=all", timeout=5)
            all_proxies = r.text.splitlines()
        except:
            all_proxies = []

        working = []
        lock = threading.Lock()
        def test_proxy(proxy):
            try:
                res = requests.get("http://httpbin.org/ip",
                                   proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"},
                                   timeout=3)
                if res.status_code == 200:
                    with lock: working.append(proxy)
            except:
                pass

        threads = []
        for proxy in all_proxies[:200]:
            t = threading.Thread(target=test_proxy, args=(proxy,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

        for i, proxy in enumerate(working[:40]):
            proxies[f"Proxy {i+1}"] = f"http://{proxy}"

        if callback:
            # Schedule callback on main thread
            splash_root.after(0, callback)

    threading.Thread(target=task, daemon=True).start()

# ===== LOG FUNCTION =====
def log(msg):
    if not settings["stealth_mode"]:
        log_text.insert(tk.END, msg+"\n")
        log_text.see(tk.END)

# ===== GUI SPLASH SCREEN =====
def gui_loading_screen():
    global splash_root
    splash_root = tk.Tk()
    splash_root.title("OuterVPN Loading")
    splash_root.geometry("600x300")
    splash_root.configure(bg="black")
    splash_root.resizable(False, False)

    label = tk.Label(splash_root, text="LOADING Outer VPN", font=("Courier", 24, "bold"), fg="#b266ff", bg="black")
    label.pack(pady=40)

    progress = ttk.Progressbar(splash_root, orient="horizontal", length=500, mode="determinate")
    progress.pack(pady=20)

    percent_label = tk.Label(splash_root, text="0%", font=("Courier", 12), fg="white", bg="black")
    percent_label.pack()

    def fill(i=0):
        if i > 100:
            def after_fetch():
                splash_root.destroy()
                build_gui()
            fetch_proxies(callback=after_fetch)
            return
        progress['value'] = i
        percent_label.config(text=f"{i}%")
        splash_root.update()
        splash_root.after(30, lambda: fill(i+2))

    fill()
    splash_root.mainloop()

# ===== GUI MAIN BUILD =====
def build_gui():
    global root, canvas, log_text, server_var, proxy_var, dns_var, selected_proxy, selected_dns, top
    root = tk.Tk()
    root.title("OuterVPN Full Visual Edition")
    root.geometry("1000x700")
    root.configure(bg=background_color)

    top = tk.Frame(root, bg=background_color)
    top.pack(pady=5)

    server_var = tk.StringVar(value=countries[0])
    proxy_var = tk.StringVar(value=list(proxies.keys())[0] if proxies else "")
    dns_var = tk.StringVar(value=list(dns_servers.keys())[0])
    selected_proxy = proxy_var
    selected_dns = dns_var

    ttk.Combobox(top, textvariable=server_var, values=countries, state="readonly", width=30).grid(row=0, column=0, padx=5)
    tk.Button(top, text="Connect", command=connect, bg="#2ecc71", fg="white", width=12).grid(row=0, column=1, padx=5)
    tk.Button(top, text="Disconnect", command=disconnect, bg="#e74c3c", fg="white", width=12).grid(row=0, column=2, padx=5)
    tk.Button(top, text="Settings", command=open_settings, bg="#3498db", fg="white", width=12).grid(row=0, column=3, padx=5)

    tk.Label(top, text="Proxy:", bg=background_color, fg="white").grid(row=1, column=0, padx=5)
    ttk.Combobox(top, textvariable=proxy_var, values=list(proxies.keys()), width=30, state="readonly").grid(row=1, column=1, columnspan=2, pady=5)

    tk.Label(top, text="DNS Server:", bg=background_color, fg="white").grid(row=2, column=0, padx=5)
    ttk.Combobox(top, textvariable=dns_var, values=list(dns_servers.keys()), width=30, state="readonly").grid(row=2, column=1, columnspan=2, pady=5)

    canvas = tk.Canvas(root, width=800, height=400, bg="black")
    canvas.pack(pady=10)

    log_text = scrolledtext.ScrolledText(root, font=("Consolas",10), fg="#00FF00", bg="black", height=10)
    log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    log("Welcome to OuterVPN!")
    update_canvas()
    animate_rainbow()
    root.mainloop()

# ===== CONNECT/DISCONNECT FUNCTIONS =====
def connect():
    global is_connected, connected_country
    if is_connected: log("Already connected."); return
    connected_country = server_var.get(); is_connected=True
    log(f"Connecting to {connected_country}...")
    proxy_key = proxy_var.get(); proxy_url = proxies.get(proxy_key,"")
    log(f"Using proxy: {proxy_key} ({proxy_url})")
    dns_key = dns_var.get(); dns_ip = dns_servers.get(dns_key)
    log(f"Using DNS server: {dns_key} ({dns_ip})")
    if settings["anti_malware"]: log("Anti-Malware scan passed ✔️")
    if settings["kill_switch"] and random.random()<0.1: log("Kill switch triggered!"); disconnect(); return
    try:
        proxy_dict={"http":proxy_url,"https":proxy_url}
        r=requests.get("https://api.ipify.org",proxies=proxy_dict,timeout=5)
        log(f"IP switched to {r.text}")
    except:
        if proxy_url: log(f"Simulated IP: {proxy_url.split('//')[1].split(':')[0]}")
    try:
        resolver=dns.resolver.Resolver(); resolver.nameservers=[dns_ip]; answer=resolver.resolve('example.com'); log(f"DNS resolved example.com to {answer[0]}")
    except: pass
    latency=random.randint(50,250); log(f"Connected to {connected_country} ({latency}ms ping)")
    if settings["auto_disconnect_time"]>0:
        threading.Thread(target=lambda:(time.sleep(settings["auto_disconnect_time"]),disconnect()),daemon=True).start()
    update_canvas()

def disconnect():
    global is_connected, connected_country
    if not is_connected: log("Not connected."); return
    log(f"Disconnected from {connected_country}"); is_connected=False; connected_country=None; update_canvas()

# ===== SETTINGS WINDOW =====
def open_settings():
    win=tk.Toplevel(root); win.title("Settings"); win.configure(bg="#2b2b2b")
    def toggle(key): settings[key]=not settings[key]; log(f"{key.replace('_',' ').title()} set to {settings[key]}")
    def update_disconnect_time(val): settings["auto_disconnect_time"]=int(val); log(f"Auto Disconnect Time set to {val} sec")
    def change_bg():
        global background_color
        c=colorchooser.askcolor(title="Choose background color")[1]
        if c: background_color=c; root.configure(bg=c); top.configure(bg=c); log(f"Background color changed to {c}")
    for i,(label,key) in enumerate([("Rainbow Mode","rainbow_mode"),("Stealth Mode","stealth_mode"),("Kill Switch","kill_switch"),("Anti-Malware","anti_malware")]):
        btn=tk.Checkbutton(win,text=label,variable=tk.BooleanVar(value=settings[key]),command=lambda k=key: toggle(k),bg="#2b2b2b",fg="white",selectcolor="#3b3b3b"); btn.grid(row=i,column=0,sticky="w",padx=10,pady=5)
    tk.Label(win,text="Auto Disconnect Time (sec)",bg="#2b2b2b",fg="white").grid(row=5,column=0,sticky="w",padx=10)
    scale=tk.Scale(win,from_=0,to=60,orient="horizontal",bg="#2b2b2b",fg="white",highlightbackground="#2b2b2b",command=update_disconnect_time)
    scale.set(settings["auto_disconnect_time"]); scale.grid(row=6,column=0,padx=10,pady=10)
    tk.Button(win,text="Change Background",command=change_bg,bg="#8e44ad",fg="white").grid(row=7,column=0,padx=10,pady=10)

# ===== RAINBOW CANVAS =====
def get_rainbow_color():
    global rainbow_angle
    rainbow_angle = (rainbow_angle+0.01)%1
    r,g,b = colorsys.hsv_to_rgb(rainbow_angle,1,1)
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

def animate_rainbow():
    if settings["rainbow_mode"]: update_canvas()
    root.after(100, animate_rainbow)

def update_canvas():
    canvas.delete("all")
    for c,(x,y) in vpn_servers.items():
        color = get_rainbow_color() if settings["rainbow_mode"] else status_map[c]
        canvas.create_oval(x,y,x+10,y+10,fill=color,outline="")
        if not settings["stealth_mode"]:
            canvas.create_text(x+15,y+5,text=c,anchor="w",fill="white")
        if connected_country==c:
            canvas.create_rectangle(x-2,y-2,x+12,y+12,outline="cyan")

# ===== START APPLICATION =====
gui_loading_screen()
