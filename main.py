
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import cv2

class ImageProcessingApp:
    def __init__(self, master):
        self.master = master
        master.title("Image Processing App")
        master.geometry("1500x800")  # Fix window size


        # Initialize image variables
        self.image_path = None
        self.original_image = None
        self.processed_image = None

        # Image display frame (fixed size)
        self.image_frame = tk.Frame(master, width=300, height=400)
        self.image_frame.pack(side=tk.LEFT, padx=10, pady=10)

# Controls frame (fixed size)
        self.controls_frame = tk.Frame(master, width=130, height=400)
        self.controls_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Histogram frame (fixed size)
        self.histogram_frame = tk.Frame(master, width=450, height=200)
        self.histogram_frame.pack(side=tk.TOP, fill=tk.X)

        # Create image label
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack()

         # Contrast slider
        self.contrast_var = tk.DoubleVar(value=1.0)  # Initial contrast value
        self.contrast_slider = tk.Scale(self.controls_frame, from_=0, to_=100, orient=tk.HORIZONTAL, variable=self.contrast_var, command=self.adjust_contrast)
        self.contrast_slider.pack()
        self.contrast_label = tk.Label(self.controls_frame, text="Contrast")
        self.contrast_label.pack()

        # Luminance slider
        self.luminance_var = tk.DoubleVar(value=0.0)  # Initial luminance value
        self.luminance_slider = tk.Scale(self.controls_frame, from_=0, to_=100, orient=tk.HORIZONTAL, variable=self.luminance_var, command=self.adjust_luminance)
        self.luminance_slider.pack()
        self.luminance_label = tk.Label(self.controls_frame, text="Luminance")
        self.luminance_label.pack()

        self.grayscale_button = tk.Button(self.controls_frame, text="Convert to Grayscale")
        self.grayscale_button.bind("<Button-1>", self.convert_grayscale)
        self.grayscale_button.pack()

        self.blur_button = tk.Button(self.controls_frame, text="Apply Blur Filter")
        self.blur_button.bind("<Button-1>", self.apply_blur_filter)
        self.blur_button.pack()

        self.edge_detection_button = tk.Button(self.controls_frame, text="Detect Edges")
        self.edge_detection_button.bind("<Button-1>", self.detect_edges)
        self.edge_detection_button.pack()

        self.histogram_button = tk.Button(self.controls_frame, text="Show Histogram")
        self.histogram_button.bind("<Button-1>", self.show_histogram)
        self.histogram_button.pack()

        self.save_button = tk.Button(self.controls_frame, text="Save Image")
        self.save_button.bind("<Button-1>", self.save_image)
        self.save_button.pack()

        self.print_button = tk.Button(self.controls_frame, text="Print Image")
        self.print_button.bind("<Button-1>", self.print_image)
        self.print_button.pack()

        # Create menu bar
        menubar = tk.Menu(master)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.open_image)
        filemenu.add_command(label="Exit", command=master.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        master.config(menu=menubar)

    def open_image(self):
        self.image_path = tk.filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.jpg *.png *.bmp")])
        if self.image_path:
            self.load_image()

    def load_image(self):
        self.original_image = Image.open(self.image_path)
        self.processed_image = self.original_image.copy()
        self.update_image_display()

    def update_image_display(self):
        if self.processed_image is not None:
            image_data = np.array(self.processed_image)
            image = ImageTk.PhotoImage(image_data)
            self.image_label.configure(image=image)
            self.image_label.image = image
    def adjust_contrast(self, event):
        # Implement contrast adjustment functionality
        pass

    def adjust_luminance(self, event):
        # Implement luminance adjustment functionality
        pass
    
    def convert_grayscale(self,event):
        pass
    
    def apply_blur_filter(self , event):
        pass

    def detect_edges(self , event):
        pass

    def show_histogram(self , event):
        pass

    def save_image(self , event):
        pass

    def print_image(self , event):
        pass

def main():
  root = tk.Tk()
  app = ImageProcessingApp(root)
  root.mainloop()            

if __name__ == "__main__":
  main()