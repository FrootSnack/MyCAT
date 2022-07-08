import tkinter
import main
import os
import tkinter as tk
import tkinter.font as tkFont
from os.path import abspath, exists
from pdf2image import convert_from_path
from PIL import Image, ImageTk
from tkinter import Toplevel, ttk


class App:
    def __init__(self, root):
        self.root = root
        #setting title
        root.title("MyCAT")
        #setting window size
        width=400
        height=120
        self.screenwidth = root.winfo_screenwidth()
        self.screenheight = root.winfo_screenheight()
        self.center_alignstr = '%dx%d+%d+%d' % (width, height, (self.screenwidth - width) / 2, (self.screenheight - height) / 2)
        root.geometry(self.center_alignstr)
        root.resizable(width=False, height=False)

        btn_start=ttk.Button(root, text="Start", command=self.btn_start_command)
        btn_start.pack(side='bottom', pady=25)

        lbl_pdf=tk.Label(root)
        ft = tkFont.Font(size=14)
        lbl_pdf["font"] = ft
        lbl_pdf["fg"] = "#000000"
        lbl_pdf["justify"] = "center"
        lbl_pdf["text"] = "PDF file (*.pdf):"
        lbl_pdf.place(x=(width//2)-100,y=15,width=200,height=25)

        self.ent_pdf=tk.Entry(root)
        self.ent_pdf["borderwidth"] = "1px"
        ft = tkFont.Font(size=12)
        self.ent_pdf["font"] = ft
        self.ent_pdf["fg"] = "#000000"
        self.ent_pdf["justify"] = "left"
        self.ent_pdf["text"] = "*.pdf"
        self.ent_pdf.place(x=30,y=40,width=350,height=25)

    def btn_start_command(self) -> None:
        try:
            cfg: main.TranslationConfig = self.process_config()
            images: list = self.pdf_as_image_list(cfg)
            self.annotate_pdf(cfg, images)
        except Exception as e:
            self.open_popup(repr(e))

    def process_config(self) -> main.TranslationConfig:
        try:
            pdf_path_abs: str = abspath(self.ent_pdf.get())
            cfg: main.TranslationConfig = None
            
            if pdf_path_abs == '' or not exists(pdf_path_abs):
                raise FileNotFoundError("The given PDF path does not exist!")
            
            output_pdf_path_abs: str = abspath(self.open_prompt("Please enter your desired output PDF path:"))

            if output_pdf_path_abs == '':
                raise ValueError("Please enter a valid path for the output PDF!")
            
            elif not exists(output_pdf_path_abs):
                f = open(output_pdf_path_abs, 'w+')
                f.close()
                cfg = main.TranslationConfig(originalFileName=pdf_path_abs, outputFileName=output_pdf_path_abs)
            
            else:
                derived_tr_path: str = f"{output_pdf_path_abs.split('.')[0]}.tr"
                if exists(derived_tr_path):
                    cfg = main.import_tr_to_translationconfig(derived_tr_path)
                else:
                    cfg = main.TranslationConfig(pdf_path_abs, output_pdf_path_abs)
            print(cfg.to_dict())
            cfg.save()
            return cfg
        except Exception as e:
            self.open_popup(repr(e))

    def annotate_pdf(self, config: main.TranslationConfig, images: list) -> None:
        top = Toplevel(self.root)
        open_img = Image.open('test.jpg')
        canvas = tk.Canvas(top, width=open_img.width, height=open_img.height, background='blue', borderwidth=0)
        canvas.pack()
        img = ImageTk.PhotoImage(open_img)
        img_sprite = canvas.create_image(0, 0, anchor=tk.NW, image=img)
        self.root.mainloop()
        return
        try:
            image_index: int = 0

            top = Toplevel(self.root)
            top.geometry('%dx%d+%d+%d' % (400, 100, (self.screenwidth - 400) / 2, (self.screenheight - 100) / 2))

            size_ratio: int = 0.1
            canvas_width: int = int(self.screenwidth*8.5*size_ratio)
            canvas_height: int = int(self.screenheight*11*size_ratio)
            # make sure width and height are product of 8.5x11 measurements
            canvas = tk.Canvas(top, width=canvas_width, height=canvas_height)
            canvas.grid(row=0, column=0)

            images = [i.resize((canvas_width, canvas_height), Image.ANTIALIAS) for i in images]

            btn_left=ttk.Button(top, text="<-", command=top.destroy)
            btn_left.grid(row=0, column=0)
            
            btn_right=ttk.Button(top, text="->", command=top.destroy)
            btn_right.grid(row=0, column=1)

            # pdf_image = ImageTk.PhotoImage(images[0])
            pdf_image = ImageTk.PhotoImage(Image.open("local/test.jpg"))
            canvas.create_image(self.screenwidth*8.5*size_ratio, self.screenheight*11*size_ratio, image=pdf_image)  # tuple index issue is on this line

            top.columnconfigure(0, weight=1)
            top.rowconfigure(0, weight=1)

        except Exception as e:
            self.open_popup(repr(e))

    def pdf_as_image_list(self, config: main.TranslationConfig) -> list:
        """Convert the PDF found in the given config to a PIL Image list."""
        try:
            return convert_from_path(config.originalFileName)
        except Exception as e:
            self.open_popup(repr(e))

    def open_popup(self, text: str) -> None:
        top = Toplevel(self.root)
        top.geometry('%dx%d+%d+%d' % (400, 100, (self.screenwidth - 400) / 2, (self.screenheight - 100) / 2))
        top.title("Error")
        tk.Label(top, text=text, justify='center').grid(column=0, row=0)
        top.columnconfigure(0, weight=1)
        top.rowconfigure(0, weight=1)

    def open_prompt(self, text: str) -> str:
        popup = Toplevel(self.root)
        var = tk.IntVar()
        popup.geometry('%dx%d+%d+%d' % (400, 100, (self.screenwidth - 400) / 2, (self.screenheight - 100) / 2))
        popup.title("Input")
        
        btn_enter=ttk.Button(popup, text="Enter", command=lambda: var.set(1))
        btn_enter.pack(side='bottom', expand=True)

        ent_prompt=tk.Entry(popup)
        ent_prompt.pack(side='bottom', expand=True)
        
        lbl_prompt=tk.Label(popup, text=text, justify='center')
        lbl_prompt.pack(side='bottom', expand=True)
        
        popup.columnconfigure(0, weight=1)
        popup.rowconfigure(0, weight=1)
        
        btn_enter.wait_variable(var)
        entered_str: str = ent_prompt.get()
        popup.destroy()
        return entered_str



if __name__ == "__main__":
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    root = tk.Tk()
    app = App(root)
    root.mainloop()
