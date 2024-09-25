import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import os

# Function to upload PDF
def upload_file():
    # Select file from file dialog
    file_path = filedialog.askopenfilename(
        title="Select a PDF",
        filetypes=[("PDF files", "*.pdf")]
    )

    if not file_path:
        messagebox.showerror("Error", "No file selected!")
        return

    # Get additional form data
    title = title_entry.get()
    answer_sequence = answer_sequence_entry.get()

    if not title or not answer_sequence:
        messagebox.showerror("Error", "Title and Answer Sequence are required!")
        return

    # Prepare file and data to send
    url = "http://127.0.0.1:5000/upload"
    files = {'pdf': open(file_path, 'rb')}
    data = {
        'title': title,
        'answer_sequence': answer_sequence
    }

    # Send POST request
    try:
        response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            messagebox.showinfo("Success", "File uploaded successfully!")
        else:
            messagebox.showerror("Error", f"Upload failed! Status code: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create the Tkinter window
window = tk.Tk()
window.title("PDF Upload")

# Create UI elements
tk.Label(window, text="Title:").grid(row=0, column=0, padx=10, pady=10)
title_entry = tk.Entry(window)
title_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(window, text="Answer Sequence:").grid(row=1, column=0, padx=10, pady=10)
answer_sequence_entry = tk.Entry(window)
answer_sequence_entry.grid(row=1, column=1, padx=10, pady=10)

upload_button = tk.Button(window, text="Upload PDF", command=upload_file)
upload_button.grid(row=2, column=1, padx=10, pady=10)

# Run the application
window.mainloop()
