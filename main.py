import tkinter as tk
from tkinter import filedialog, messagebox
import os
from utils import process_passport_photos


# Developer Info
DEVELOPER_INFO = """Developed by:
Kasim K
HSST Computer Science
Govt. Seethi Haji HSS Edavanna
Mob: 8547005187
"""

def browse_input_file():
    filename = filedialog.askopenfilename(
        title="Select input image file",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
    )
    if filename:
        input_path.set(filename)

def browse_output_folder():
    folder = filedialog.askdirectory(title="Select output folder")
    if folder:
        output_path.set(folder)

def extract_photos():
    in_file = input_path.get()
    out_folder = output_path.get()
    try:
        w = int(width.get())
        h = int(height.get())
        max_kb_value = int(max_kb.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for width, height, and max KB")
        return

    if not in_file or not out_folder:
        messagebox.showerror("Error", "Please select input file and output folder")
        return

    face_only = face_only_var.get()

    try:
        process_passport_photos(
            in_file, out_folder, w, h, max_kb_value, face_only
        )
        messagebox.showinfo("Success", "Photos extracted successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def show_about():
    messagebox.showinfo("About", DEVELOPER_INFO)


# GUI
root = tk.Tk()
root.title("Passport Photo Extractor")

input_path = tk.StringVar()
output_path = tk.StringVar()
width = tk.StringVar(value="300")
height = tk.StringVar(value="400")
max_kb = tk.StringVar(value="100")
face_only_var = tk.BooleanVar(value=True)

tk.Label(root, text="Input File:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
tk.Entry(root, textvariable=input_path, width=40).grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=browse_input_file).grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="Output Folder:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
tk.Entry(root, textvariable=output_path, width=40).grid(row=1, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=browse_output_folder).grid(row=1, column=2, padx=5, pady=5)

tk.Label(root, text="Width (px):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
tk.Entry(root, textvariable=width, width=10).grid(row=2, column=1, sticky="w", padx=5, pady=5)

tk.Label(root, text="Height (px):").grid(row=3, column=0, sticky="w", padx=5, pady=5)
tk.Entry(root, textvariable=height, width=10).grid(row=3, column=1, sticky="w", padx=5, pady=5)

tk.Label(root, text="Max Size (KB):").grid(row=4, column=0, sticky="w", padx=5, pady=5)
tk.Entry(root, textvariable=max_kb, width=10).grid(row=4, column=1, sticky="w", padx=5, pady=5)

tk.Checkbutton(root, text="Face Only", variable=face_only_var).grid(row=5, column=0, columnspan=2, padx=5, pady=5)

tk.Button(root, text="Extract", command=extract_photos).grid(row=6, column=0, columnspan=3, pady=10)
tk.Button(root, text="About", command=show_about).grid(row=7, column=0, columnspan=3, pady=5)

root.mainloop()
