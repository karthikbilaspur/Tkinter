from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog

class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")
        self.root.geometry("800x600")  # Increased window size

        self.images = []
        self.image_index = 0

        self.label = Label(image=None)
        self.label.grid(row=1, column=0, columnspan=3, padx=10, pady=10)  # Added padding

        self.button_frame = Frame(root)
        self.button_frame.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        self.button_back = Button(self.button_frame, text="Back", command=self.back, state=DISABLED)
        self.button_back.pack(side=LEFT, padx=10)

        self.button_exit = Button(self.button_frame, text="Exit", command=root.quit)
        self.button_exit.pack(side=LEFT, padx=10)

        self.button_forward = Button(self.button_frame, text="Forward", command=self.forward, state=DISABLED)
        self.button_forward.pack(side=LEFT, padx=10)

        self.button_load = Button(root, text="Load Images", command=self.load_images)
        self.button_load.grid(row=0, column=0, columnspan=3, padx=10, pady=10)  # Added padding

        self.status_bar = Label(root, text="", relief=SUNKEN, anchor=W)
        self.status_bar.grid(row=6, column=0, columnspan=3, sticky="ew")  # Added sticky

        self.image_info_label = Label(root, text="")
        self.image_info_label.grid(row=2, column=0, columnspan=3, padx=10, pady=10)  # Added image info label

    def load_images(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", ".png .jpg .jpeg")])
        if file_paths:
            self.images = [ImageTk.PhotoImage(Image.open(file_path)) for file_path in file_paths]
            self.image_index = 0
            self.label.config(image=self.images[self.image_index])
            self.button_back.config(state=DISABLED)
            self.button_forward.config(state=NORMAL)
            self.status_bar.config(text=f"{len(self.images)} images loaded")
            self.update_image_info()

    def back(self):
        if self.image_index > 0:
            self.image_index -= 1
            self.label.config(image=self.images[self.image_index])
            self.button_forward.config(state=NORMAL)
            if self.image_index == 0:
                self.button_back.config(state=DISABLED)
            self.update_image_info()

    def forward(self):
        if self.image_index < len(self.images) - 1:
            self.image_index += 1
            self.label.config(image=self.images[self.image_index])
            self.button_back.config(state=NORMAL)
            if self.image_index == len(self.images) - 1:
                self.button_forward.config(state=DISABLED)
            self.update_image_info()

    def update_image_info(self):
        image = self.images[self.image_index]
        width, height = image.width(), image.height()
        self.image_info_label.config(text=f"Image {self.image_index+1} of {len(self.images)} - {width}x{height}")

root = Tk()
viewer = ImageViewer(root)
root.mainloop()