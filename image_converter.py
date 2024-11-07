import tkinter as tk
from tkinter import filedialog, scrolledtext
from PIL import Image, ImageTk
import pytesseract
from pathlib import Path
import os

# Set the path to Tesseract executable (this line should come AFTER importing pytesseract)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class ImageToTextConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to Text Converter")
        self.root.geometry("800x600")
        
        # Configure grid weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        
        # Variables
        self.image_path = None
        self.preview_image = None
        
        # Create widgets
        self.create_widgets()
        
    def create_widgets(self):
        # Select Image Button
        self.select_btn = tk.Button(
            self.root,
            text="Select Image",
            command=self.select_image,
            padx=10,
            pady=5
        )
        self.select_btn.grid(row=0, column=0, pady=10)
        
        # Image Preview Label
        self.preview_label = tk.Label(
            self.root,
            text="No image selected",
            width=40,
            height=10
        )
        self.preview_label.grid(row=1, column=0, pady=10)
        
        # Text Output Area
        self.text_output = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            width=60,
            height=15
        )
        self.text_output.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        # Convert Button
        self.convert_btn = tk.Button(
            self.root,
            text="Convert to Text",
            command=self.convert_image,
            state=tk.DISABLED,
            padx=10,
            pady=5
        )
        self.convert_btn.grid(row=3, column=0, pady=10)
        
        # Save Button
        self.save_btn = tk.Button(
            self.root,
            text="Save Text",
            command=self.save_text,
            state=tk.DISABLED,
            padx=10,
            pady=5
        )
        self.save_btn.grid(row=4, column=0, pady=10)
        
    def select_image(self):
        filetypes = (
            ('Image files', '*.png *.jpg *.jpeg *.bmp *.gif'),
            ('All files', '*.*')
        )
        
        filename = filedialog.askopenfilename(
            title='Select an image',
            filetypes=filetypes
        )
        
        if filename:
            self.image_path = filename
            self.load_image_preview()
            self.convert_btn.config(state=tk.NORMAL)
            
    def load_image_preview(self):
        # Open and resize image for preview
        image = Image.open(self.image_path)
        # Calculate aspect ratio
        aspect_ratio = image.width / image.height
        new_width = 300
        new_height = int(new_width / aspect_ratio)
        
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.preview_image = ImageTk.PhotoImage(image)
        self.preview_label.config(image=self.preview_image)
        
    def convert_image(self):
        try:
            # Convert image to text using Tesseract
            image = Image.open(self.image_path)
            text = pytesseract.image_to_string(image)
            
            # Clear previous text and insert new text
            self.text_output.delete(1.0, tk.END)
            self.text_output.insert(tk.END, text)
            
            # Enable save button
            self.save_btn.config(state=tk.NORMAL)
            
        except Exception as e:
            self.text_output.delete(1.0, tk.END)
            self.text_output.insert(tk.END, f"Error: {str(e)}")
            
    def save_text(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension='.txt',
            filetypes=[('Text files', '*.txt'), ('All files', '*.*')]
        )
        
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.text_output.get(1.0, tk.END))

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageToTextConverter(root)
    root.mainloop()