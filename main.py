
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
from tkinter import filedialog
import cv2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import ImageEnhance

class ImageProcessingApp:
    def __init__(self, master):
        self.master = master
        master.title("Image Processing App")
        master.geometry("1500x900")  # Fix window size


        # Initialize image variables
        self.image_path = None
        self.original_image = None
        self.processed_image = None

        # Left panel (controls) with fixed width
        self.controls_frame = tk.Frame(master, width=200)
        self.controls_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Top section: Image frame with border
        self.image_frame = tk.Frame(master, bd=2, relief=tk.SUNKEN, height=900)
        self.image_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Bottom section: Histogram frame with border (same width as image)
        self.histogram_frame = tk.Frame(master, bd=2, relief=tk.SUNKEN, height=450)
        self.histogram_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Create image label
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack()


         # Contrast slider
        self.contrast_var = tk.DoubleVar(value=1.0)  # Initial contrast value
        self.contrast_slider = tk.Scale(self.controls_frame, from_=0, to_=0.5, orient=tk.HORIZONTAL, variable=self.contrast_var, command=self.adjust_contrast)
        self.contrast_slider.pack()
        self.contrast_label = tk.Label(self.controls_frame, text="Contrast")
        self.contrast_label.pack()

        # Luminance slider
        self.luminance_var = tk.DoubleVar(value=0.0)  # Initial luminance value
        self.luminance_slider = tk.Scale(self.controls_frame, from_=-1, to_=1, orient=tk.HORIZONTAL, variable=self.luminance_var, command=self.adjust_luminance)
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
        self.histogram_button.bind("<Button-1>", self.show_histogram())
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

        # Resize image (optional, adjust width and height as needed)
        max_width, max_height = self.image_frame.winfo_width(), self.image_frame.winfo_height()  # Get frame dimensions
        self.processed_image = self.original_image.resize((int(1500*0.5), int(800*0.5)))  # Resize with antialiasing
        #   Update histogram on image load
        self.update_image_display()
        self.show_histogram()

    def update_image_display(self):
        if self.processed_image is not None:
            print("NOT NOOOOOOOOOOOOOOOOOOOOOONNNNEEEEEEEEEEEEEEEEE")
            image_data = np.array(self.processed_image)
            image = ImageTk.PhotoImage(image=Image.fromarray(image_data))
            self.image_label.configure(image=image)
            self.image_label.image = image


    def adjust_contrast(self, event):
        if self.processed_image is not None:
            contrast_value = self.contrast_var.get() / 100.0  # Get contrast value from the slider (0 to 1)

            # Convert image to PIL format if it's not already in RGB
            if self.processed_image.mode != "RGB":
                adjustedLuminanceImage = self.processed_image.convert("RGB")

            # Adjust contrast
            enhancer = ImageEnhance.Contrast(adjustedLuminanceImage)
            adjustedLuminanceImage = enhancer.enhance(contrast_value)

            # Update image display
            self.update_image_display()
            self.show_histogram()
    def adjust_luminance(self, event):
        if self.processed_image is not None:
            luminance_value = self.luminance_var.get() - 50  # Get luminance value from the slider (-50 to 50)

            # Convert image to PIL format if it's not already in RGB
            if self.processed_image.mode != "RGB":
                adjustedLuminanceImage = self.processed_image.convert("RGB")

            # Adjust luminance
            r, g, b = adjustedLuminanceImage.split()
            r = r.point(lambda i: i + luminance_value)
            g = g.point(lambda i: i + luminance_value)
            b = b.point(lambda i: i + luminance_value)
            adjustedLuminanceImage = Image.merge("RGB", (r, g, b))

            # Update image display
            self.update_image_display()
            self.show_histogram()
    def convert_grayscale(self,event):
        pass
    
    def apply_blur_filter(self , event):
        pass

    def detect_edges(self , event):
        pass

    def show_histogram(self):
        if self.processed_image is not None:
            if self.processed_image.mode != "RGB":
                rgb_image = self.processed_image.convert("RGB")
            else:
                rgb_image = self.processed_image

            # Clear existing plot (optional)
            for widget in self.histogram_frame.winfo_children():
                widget.destroy()

            # Calculate histograms for each channel
            red_hist, _ = np.histogram(np.array(rgb_image)[:,:,0].ravel(), bins=256, range=[0, 256])
            green_hist, _ = np.histogram(np.array(rgb_image)[:,:,1].ravel(), bins=256, range=[0, 256])
            blue_hist, _ = np.histogram(np.array(rgb_image)[:,:,2].ravel(), bins=256, range=[0, 256])

            # Create a matplotlib figure and plot the histograms
            fig, ax = plt.subplots(figsize=(7, 4))  # Adjust figure size as needed
            ax.plot(red_hist, color='red', label='Red')
            ax.plot(green_hist, color='green', label='Green')
            ax.plot(blue_hist, color='blue', label='Blue')
            ax.set_xlabel("Pixel Intensity")
            ax.set_ylabel("Frequency")
            ax.set_title("RGB Histogram")
            ax.legend()

            # Embed the matplotlib plot within the histogram frame
            canvas = FigureCanvasTkAgg(fig, master=self.histogram_frame)
            canvas.draw()
            canvas.get_tk_widget().pack()

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