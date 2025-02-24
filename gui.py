import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import process_image
import os
from ttkbootstrap import Style
from tkinter import ttk

# === SETUP WINDOW ===
root = tk.Tk()
root.title("Marksheet OCR Extractor")
root.geometry("600x700")

# Apply Bootstrap Style
style = Style(theme="cosmo")

# Set Background Image
BG_IMAGE_PATH = "assets\bg.jpg"

if os.path.exists(BG_IMAGE_PATH):
    bg_image = Image.open(BG_IMAGE_PATH)
    bg_image = bg_image.resize((600, 700))
    bg_image = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)

# Heading
title_label = tk.Label(root, text="Marksheet OCR Extractor", font=("Arial", 18, "bold"), bg="#e0f7fa", fg="black")
title_label.pack(pady=10)

# Image Preview
image_label = tk.Label(root, text="No Image Selected", font=("Arial", 10), bg="#f4f4f4", fg="gray")
image_label.pack(pady=10)

# Table for results
columns = ("Question Number", "Marks Scored")
tree = ttk.Treeview(root, columns=columns, show="headings", height=8)
tree.heading("Question Number", text="Question Number")
tree.heading("Marks Scored", text="Marks Scored")
tree.pack(pady=10)


def upload_image():
    """Handles file upload through GUI."""
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        return

    # Load and display image
    img = Image.open(file_path)
    img.thumbnail((300, 300))
    img = ImageTk.PhotoImage(img)
    image_label.config(image=img, text="")
    image_label.image = img

    # Process image
    extracted_data = process_image.process_image(file_path)

    # Clear previous data
    tree.delete(*tree.get_children())

    # Insert Register Number as the first row
    tree.insert("", "end", values=("Register No.", extracted_data["register_number"]))

    # Insert 2-Marks Data
    for q, mark in zip(range(1, len(extracted_data["TWO_marks"]) + 1), extracted_data["TWO_marks"]):
        tree.insert("", "end", values=(f"Q{q}", mark))

    # Insert Big Question Data
    for q, mark in zip(range(11, 11 + len(extracted_data["BIG_QUES"])-4), extracted_data["BIG_QUES"]):
        tree.insert("", "end", values=(f"Q{q}", mark))

    messagebox.showinfo("Success", "Data Extracted and Saved to Excel!")


# Upload Button
upload_btn = tk.Button(root, text="Choose Image", command=upload_image, bg="#007bff", fg="white", padx=10, pady=5)
upload_btn.pack(pady=10)

# Run Tkinter loop
root.mainloop()
