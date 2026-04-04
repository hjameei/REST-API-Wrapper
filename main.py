import tkinter as tk
from PIL import Image, ImageTk
import io
from dotenv import load_dotenv
import os
from thecatapi.cat_api import TheCatApi, TheCatAPIException
from thecatapi.models import *

cat_api = None

class KittyTimeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Kitty Time!')
        self.geometry('1024x768')
        self.resizable(False, False)

class KittyFrame(tk.Frame):
    def __init__(self, root: tk.Tk):
        super().__init__(root)

        # Member variables
        self.kitty = None
        self.kitty_img = None
        self.kitty_photo_img = None

        # Frame geometry setup
        self.grid(row=0, column=0, sticky='news')
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Top row buttons and label
        self.get_kitty_button = tk.Button(self, text='Get a Kitty')
        self.get_kitty_button['command'] = self.get_kitty_button_clicked
        self.get_kitty_button.grid(row=0, column=0, padx=10, pady=10, sticky='NW')

        self.save_kitty_button = tk.Button(self, text='Save Kitty')
        self.save_kitty_button['command'] = self.save_kitty_button_clicked
        self.save_kitty_button.grid(row=0, column=1, padx=10, pady=10, sticky='NW')

        self.url_label = tk.Label(self, text="Yay! It's kitty time!")
        self.url_label.grid(row=0, column=2, padx=10, pady=10, sticky='NSE')
        self.update()

        # Next row of another frame
        width = root.winfo_width()
        height = root.winfo_height()
        borderwidth = 5
        self.picture_frame = tk.Frame(self, borderwidth=borderwidth, relief='ridge', width=width, height=height)
        self.picture_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.picture_frame.update()
        pf_width = self.picture_frame.winfo_width()
        pf_height = self.picture_frame.winfo_height()

        self.picture_frame_canvas = tk.Canvas(self.picture_frame, width=pf_width, height=pf_height)
        self.picture_frame_canvas.grid(row=0, column=0)
        self.picture_frame.rowconfigure(0, weight=1)
        self.picture_frame.columnconfigure(0, weight=1)
    
    def get_kitty_button_clicked(self):
        # get kitty url and download kitty image to memory
        self.kitty = cat_api.get_kitty()
        self.url_label.config(text=self.kitty.url)
        cat_api.fetch_image_data(self.kitty)  # type: ImageShort

        # get picture frame size
        self.picture_frame.update()
        pf_width = self.picture_frame.winfo_width()
        pf_height = self.picture_frame.winfo_height()
        pf_ratio = pf_width / pf_height

        # convert and resize kitty Image
        self.kitty_img = Image.open(io.BytesIO(self.kitty.data))
        img_ratio = self.kitty_img.width / self.kitty_img.height
        if img_ratio > pf_ratio:
            resized_image = self.kitty_img.resize((pf_width, int(pf_width * (1 / img_ratio))), Image.Resampling.LANCZOS)
        else:
            resized_image = self.kitty_img.resize((int(pf_height * img_ratio), pf_height), Image.Resampling.LANCZOS)
        self.kitty_photo_img = ImageTk.PhotoImage(image=resized_image)

        self.picture_frame_canvas.create_image((int(pf_width / 2), int(pf_height / 2)), image=self.kitty_photo_img)

    def save_kitty_button_clicked(self):
        self.kitty.save_to()

if __name__ == '__main__':
    load_dotenv() 
    api_key = os.getenv("API_KEY")
    cat_api = TheCatApi(api_key = api_key)
    app = KittyTimeApp()
    frame = KittyFrame(app)
    app.mainloop()