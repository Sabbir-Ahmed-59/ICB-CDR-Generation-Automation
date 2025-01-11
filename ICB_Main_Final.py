import tkinter as tk
import subprocess

# Function to run the selected Python script
def run_script(script_name):
    try:
        subprocess.run(["python", script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running {script_name}: {e}")

# Function to run all scripts
def run_all_scripts():
    scripts = ["ICB_GPRS_CDR_3.0.py", "ICB_SMSMO_CDR_3.0.py", "ICB_VoiceMO_CDR_3.0.py", "ICB_VoiceMT_CDR_3.0.py"]
    for script in scripts:
        run_script(script)

# Create the main GUI window
root = tk.Tk()
root.title("ICB CDR Generation Script")
root.geometry("300x300")

# Title Label
title_label = tk.Label(root, text="ICB CDR Generation Script", font=('Arial', 14, 'bold'))
title_label.pack(pady=20)

# Buttons for each event script
button_gprs = tk.Button(root, text="GPRS_CDR", command=lambda: run_script("ICB_GPRS_CDR_3.0.py"), font=('Arial', 10))
button_gprs.pack(pady=5)

button_smsmo = tk.Button(root, text="SMSMO_CDR", command=lambda: run_script("ICB_SMSMO_CDR_3.0.py"), font=('Arial', 10))
button_smsmo.pack(pady=5)

button_voicemo = tk.Button(root, text="VoiceMO_CDR", command=lambda: run_script("ICB_VoiceMO_CDR_3.0.py"), font=('Arial', 10))
button_voicemo.pack(pady=5)

button_voicemt = tk.Button(root, text="VoiceMT_CDR", command=lambda: run_script("ICB_VoiceMT_CDR_3.0.py"), font=('Arial', 10))
button_voicemt.pack(pady=5)

# Master button to run all scripts
button_run_all = tk.Button(root, text="CDR for All Events", command=run_all_scripts, font=('Arial', 10, 'bold'), fg='white', bg='red')
button_run_all.pack(pady=20)

# Run the GUI loop
root.mainloop()
