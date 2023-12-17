import tkinter as tk
from PIL import Image, ImageTk
import os
import csv

class ImageLabeler:
    def __init__(self, root, image_folder):
        self.root = root
        self.root.geometry("1024x768")  # Initial window size
        self.root.resizable(True, True)  # Make window resizable

        self.image_folder = image_folder
        self.images = [img for img in os.listdir(image_folder) if img.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
        self.current_image = 0
        self.label_data = self.load_existing_labels()
        self.setup_ui()

    def setup_ui(self):
        self.status_bar = tk.Label(self.root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.image_counter = tk.Label(self.root, text="")
        self.image_counter.pack()

        self.label_entry = tk.Entry(self.root)
        self.label_entry.pack()

        submit_button = tk.Button(self.root, text="Submit", command=self.save_label)
        submit_button.pack()

        next_button = tk.Button(self.root, text="Next", command=self.next_image)
        next_button.pack()

        prev_button = tk.Button(self.root, text="Previous", command=self.prev_image)
        prev_button.pack()

        self.root.bind('<Return>', lambda event: self.save_label())
        self.root.bind('<Right>', lambda event: self.next_image())
        self.root.bind('<Left>', lambda event: self.prev_image())

        self.display_image()

    def load_existing_labels(self):
        if not os.path.exists('labels.csv'):
            return {}
        with open('labels.csv', mode='r', newline='') as file:
            reader = csv.reader(file)
            return {rows[0]: rows[1] for rows in reader}

    def display_image(self):
        if not self.images:
            self.status_bar.config(text="No images found")
            return

        img_path = os.path.join(self.image_folder, self.images[self.current_image])
        try:
            img = Image.open(img_path)
            img = self.scale_image(img, 800, 600)
            img = ImageTk.PhotoImage(img)

            if hasattr(self, 'panel'):
                self.panel.configure(image=img)
                self.panel.image = img
            else:
                self.panel = tk.Label(self.root, image=img)
                self.panel.image = img
                self.panel.pack()

            current_label = self.label_data.get(self.images[self.current_image], "")
            self.label_entry.delete(0, 'end')
            self.label_entry.insert(0, current_label)

            self.update_image_counter()
            self.label_entry.focus_set()
        except IOError:
            self.status_bar.config(text="Error loading image")
            return

    def scale_image(self, img, max_width, max_height):
        original_width, original_height = img.size
        ratio = min(max_width/original_width, max_height/original_height)
        new_size = (int(original_width * ratio), int(original_height * ratio))
        return img.resize(new_size, Image.Resampling.LANCZOS)

    def next_image(self):
        if self.current_image < len(self.images) - 1:
            self.current_image += 1
            self.display_image()

    def prev_image(self):
        if self.current_image > 0:
            self.current_image -= 1
            self.display_image()

    def save_label(self):
        label = self.label_entry.get()
        if label:
            image_name = self.images[self.current_image]
            self.label_data[image_name] = label
            self.save_labels_to_csv()
            self.status_bar.config(text="Label saved")
            if self.current_image < len(self.images) - 1:
                self.current_image += 1
                self.display_image()
        else:
            self.status_bar.config(text="Please enter a label")
        self.label_entry.focus_set()

    def save_labels_to_csv(self):
        with open('labels.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for key, value in self.label_data.items():
                writer.writerow([key, value])

    def update_image_counter(self):
        text = f"Image {self.current_image + 1} of {len(self.images)}"
        self.image_counter.config(text=text)

root = tk.Tk()
app = ImageLabeler(root, "../TestImages/")
root.mainloop()
