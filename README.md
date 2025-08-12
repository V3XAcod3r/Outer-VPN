🌌 OuterVPN - Full Visual Edition 🚀
A visually immersive, feature-packed VPN simulator with proxy support, animated effects, and stealth utilities. Built with 💜 Tkinter and Python magic.



<img width="1285" height="757" alt="Screenshot 2025-08-12 at 2 11 29 AM" src="https://github.com/user-attachments/assets/e53dbf81-34cf-4857-85cc-3b15e1dbf0f5" />


✨ Features
🛡️ Secure & Smart

🔒 Kill Switch – Prevents leaks during drops

🦠 Anti-Malware Simulation – Fake-scan before connect

⛔ Auto Disconnect Timer – Set and forget auto-off

🌈 Visual & Customizable

🌈 Rainbow Mode – Real-time animated server indicators

🕵️ Stealth Mode – Disables logs and hides GUI texts

🎨 Dynamic Background Picker – Theme it your way

🌍 Global Connectivity

🌐 Connect to 40+ Countries – USA, India, UK, Japan, etc.

🔁 Proxy Integration – Simulated proxy switching

📶 Latency Display – Shows real ping simulation

💡 Server Status LEDs – Green / Yellow / Red logic

🚀 Next-Level Interface

💻 Fullscreen Optical Loading Screen

🧠 Smart Simulated IP Switching

📜 Scrollable Logs (unless in stealth mode)

🖱️ Dropdown Server Selection & Proxy Choice

🧩 Custom-built Canvas Animation Engine

🖼️ Sneak Peek
Loading Screen	Server Map	Settings Panel

🧰 Tech Stack
Python 3.10+

Tkinter (GUI)

requests (for real IP querying)

colorsys, math, random (visuals & logic)

Optional: threading, time, scrolledtext, colorchooser

🛠️ Setup & Run
bash
Copy
Edit
git clone https://github.com/yourname/OuterVPN.git
cd OuterVPN
python main.py
No actual VPN tunneling occurs — this is a simulated educational tool with visual flair.

🔮 Planned Features
✅ Server latency graphs

✅ Sound toggle (coming without .wav usage!)

✅ Auto-Rotate Best Proxy

🔲 Real IP switch (WIP)

🔲 Ad Blocker / Malware Filter Extensions

🔲 Premium Mode with Custom Features

📜 License
MIT License © [V3XA]


<img width="974" height="724" alt="Screenshot 2025-08-12 at<img width="983" height="713" alt="Screenshot 2025-08-12 at 2 06 28 AM" src="https://github.com/user-attachments/assets/86bad448-a28d-4116-8365-aaeffc40e9b4" />
 2 05 58 AM" src="https://github.com/user-attachments/assets/15c7264d-65b4-42f8-a29b-0093c9eefd31" />






🚨 Reminder
This still is proxy-based a real encrypted VPN tunnel. 

Actually changes your IP for many apps

Works on macOS + Windows

_______INSTALL INSTRUCTIONS______________

⚙️ Installation & Launch Guide for OuterVPN - Full Visual Edition 🌐
Simulated VPN with real proxy switching, animated visuals, and stealth power — now with system-wide proxy control on macOS & Windows! 💻🔥

🚀 Prerequisites
Make sure you have:

✅ Python 3.10+ installed
✅ Git (optional, for cloning)
✅ Internet connection (for proxy testing)

Check Python version:

bash
Copy
Edit
python --version
📥 1. Clone or Download the Repo
Option A – Using Git:
bash
Copy
Edit
git clone https://github.com/yourusername/OuterVPN.git
cd OuterVPN
Option B – Manual Download:
Click Code > Download ZIP

Extract it and open the folder in your terminal

📦 2. Install Required Packages
This project uses only standard Python libraries!
But for safety, install requests if it’s not already installed:

bash
Copy
Edit
pip install requests
🖥️ 3. How to Run the App
From inside the project folder, run:

bash
Copy
Edit
python outervpn.py
Replace outervpn.py with the actual name of your script.

🧪 4. Test Proxy Switching (macOS / Windows)
Choose a proxy from the dropdown

Hit Connect

System proxy will update 🌀

You can check your IP via: https://whatismyipaddress.com

🛑 Hit Disconnect to turn off the system proxy.

🛠️ Admin Tip
For proxy changes to take effect system-wide:

On macOS, run with permission:

bash
Copy
Edit
sudo python outervpn.py
On Windows, run from Command Prompt as Administrator

⚠️ Note on Proxies
This app uses public HTTP proxies. You can:

Replace them in the proxies = {...} dict

Use premium proxies for stability

Add SOCKS support with PySocks (if needed)

🧼 Uninstall / Reset System Proxy
If system proxy doesn’t reset:

macOS:

bash
Copy
Edit
networksetup -setwebproxystate Wi-Fi off
networksetup -setsecurewebproxystate Wi-Fi off
Windows:

bash
Copy
Edit
reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings\" /v ProxyEnable /t REG_DWORD /d 0 /f

