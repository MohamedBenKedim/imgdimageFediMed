
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
from tkinter import filedialog
import cv2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import ImageEnhance
#import win32print
#import win32ui

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
        self.contrast_slider = tk.Scale(self.controls_frame, from_=0, to_=100, orient=tk.HORIZONTAL, variable=self.contrast_var, command=self.adjust_contrast)
        self.contrast_slider.pack()
        self.contrast_slider.set(50)
        self.contrast_label = tk.Label(self.controls_frame, text="Contrast")
        self.contrast_label.pack()

        # Luminance slider
        self.luminance_var = tk.DoubleVar(value=0.0)  # Initial luminance value
        self.luminance_slider = tk.Scale(self.controls_frame, from_=0, to_=100, orient=tk.HORIZONTAL, variable=self.luminance_var, command=self.adjust_luminance)
        self.luminance_slider.pack()
        self.luminance_slider.set(50)
        self.luminance_label = tk.Label(self.controls_frame, text="Luminance")
        self.luminance_label.pack()

        self.grayscale_button = tk.Button(self.controls_frame, text="Convert to Grayscale")
        self.grayscale_button.bind("<Button-1>", self.convert_grayscale)
        self.grayscale_button.pack()

        # Blur slider
        self.blur_var = tk.DoubleVar(value=0.0)  # Initial blur value
        self.blur_slider = tk.Scale(self.controls_frame, from_=0, to_=100, orient=tk.HORIZONTAL, variable=self.blur_var, command=self.apply_blur_filter)
        self.blur_slider.pack()
        self.blur_label = tk.Label(self.controls_frame, text="Blur")
        self.blur_label.pack()

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
        self.image_path = tk.filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.jpg *.png *.bmp *.jpeg")])
        if self.image_path:
            self.load_image()

    def load_image(self):
        self.original_image = Image.open(self.image_path)

        # Resize image (optional, adjust width and height as needed)
        max_width, max_height = self.image_frame.winfo_width(), self.image_frame.winfo_height()  # Get frame dimensions
        resized_width = min(max_width, int(self.original_image.width * 0.5))
        resized_height = min(max_height, int(self.original_image.height * 0.5))
        self.processed_image = self.original_image.resize((resized_width, resized_height), Image.LANCZOS) # Resize with antialiasing

        # Update histogram on image load
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
        contrast_value = self.contrast_var.get() / 50.0  # Scale the contrast value between 0 and 2

        # Apply contrast enhancement
        enhanced_image = ImageEnhance.Contrast(self.original_image).enhance(contrast_value)

        # Update processed image and display
        self.processed_image = enhanced_image
        self.update_image_display()
        self.show_histogram()
    def adjust_luminance(self, event):
        if self.original_image is not None:
          luminance_value = self.luminance_var.get() - 50  # Get luminance value from the slider (-50 to 50)

          # Convert image to PIL format if it's not already in RGB
          if self.original_image.mode != "RGB":
              original_image_rgb = self.original_image.convert("RGB")
          else:
              original_image_rgb = self.original_image.copy()

          # Adjust luminance
          r, g, b = original_image_rgb.split()
          r = r.point(lambda i: i + luminance_value)
          g = g.point(lambda i: i + luminance_value)
          b = b.point(lambda i: i + luminance_value)
          adjusted_image_rgb = Image.merge("RGB", (r, g, b))

          # Update processed image
          self.processed_image = adjusted_image_rgb

          # Update image display
          self.update_image_display()
          self.show_histogram()
    def convert_grayscale(self,event):
        if self.original_image is not None:
          # Convert image to grayscale
          grayscale_image = self.original_image.convert("L")

          # Set grayscale image as both original and processed image
          self.original_image = grayscale_image
          self.processed_image = grayscale_image

          # Update image display
          self.update_image_display()
          self.show_histogram()
    
    def apply_blur_filter(self, event=None):
      if self.original_image is not None:
          blur_value = int(self.blur_var.get())  # Get blur value from the slider

          # Convert image to numpy array
          image_np = np.array(self.original_image)

          # Apply blur filter
          if blur_value > 0:
              blurred_image_np = cv2.GaussianBlur(image_np, (blur_value, blur_value), 0)  
          else:
              blurred_image_np = image_np

          # Convert back to PIL image
          blurred_image = Image.fromarray(blurred_image_np)

          # Update processed image
          self.processed_image = blurred_image

          # Update image display
          self.update_image_display()
          self.show_histogram()



    def detect_edges(self, event):
      if self.original_image is not None:
          # Convert image to numpy array
          image_np = np.array(self.original_image)

          # Convert to grayscale
          gray_image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

          # Apply Canny edge detection
          edges_image_np = cv2.Canny(gray_image_np, 50, 150)  # Adjust threshold values as needed

          # Convert edges image back to PIL image
          edges_image = Image.fromarray(edges_image_np)

          # Update processed image
          self.processed_image = edges_image

          # Update image display
          self.update_image_display()
          self.show_histogram()

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

    def save_image(self, event=None):
      if self.processed_image is not None:
          # Ask user for file path to save the image
          file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])

          # Check if a file path was provided
          if file_path:
              # Save the processed image
              self.processed_image.save(file_path)

              # Optionally, show a message to confirm that the image has been saved
              messagebox.showinfo("Image Saved", "The image has been saved successfully.")

    
    '''def print_image(self, event=None):
      if self.processed_image is not None:
          # Convert processed image to a format compatible with Tkinter
          image_tk = ImageTk.PhotoImage(self.processed_image)

          # Create a temporary root window for printing
          print_root = tk.Tk()
          print_root.withdraw()  # Hide the root window

          # Get default printer
          printer_name = win32print.GetDefaultPrinter()

          # Create a printer DC
          printer_dc = win32ui.CreateDC()

          # Set the printer to the default printer
          printer_dc.CreatePrinterDC(printer_name)

          # Start a print job
          printer_dc.StartDoc('Print Image')
          printer_dc.StartPage()

          # Print the image
          printer_dc.StretchBlt((0, 0, self.processed_image.width(), self.processed_image.height()), 
                                image_tk, (0, 0, self.processed_image.width(), self.processed_image.height()), 
                                win32con.SRCCOPY)

          # End the print job
          printer_dc.EndPage()
          printer_dc.EndDoc()

          # Destroy the printer DC
          printer_dc.DeleteDC()

          # Destroy the temporary root window
          print_root.destroy()'''
def main():
  root = tk.Tk()
  app = ImageProcessingApp(root)
  root.mainloop()            

if __name__ == "__main__":
  main()