
import os
import sys

# Automatically use the directory this file is in
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Try to run the main script file
main_files = ["RedTiger.py", "main.py", "app.py"]

for file in main_files:
    if os.path.exists(file):
        os.system(f"python3 {file}")
        sys.exit()

print("❌ Could not find a main Python file to run (RedTiger.py, main.py, or app.py).")
