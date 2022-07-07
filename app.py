import tkinter as tk
import tkinter.font as tkFont
import main
from os.path import abspath, exists
from tkinter import Toplevel, ttk

class App:
    def __init__(self, root):
        self.root = root
        #setting title
        root.title("MyCAT")
        #setting window size
        width=400
        height=230
        self.screenwidth = root.winfo_screenwidth()
        self.screenheight = root.winfo_screenheight()
        self.center_alignstr = '%dx%d+%d+%d' % (width, height, (self.screenwidth - width) / 2, (self.screenheight - height) / 2)
        root.geometry(self.center_alignstr)
        root.resizable(width=False, height=False)

        btn_start=ttk.Button(root, text="Start", command=self.btn_start_command)
        btn_start.pack(side='bottom', pady=25)

        lbl_translation_config=tk.Label(root)
        ft = tkFont.Font(size=14)
        lbl_translation_config["font"] = ft
        lbl_translation_config["fg"] = "#000000"
        lbl_translation_config["justify"] = "center"
        lbl_translation_config["text"] = "Translation configuration file (*.tr):"
        lbl_translation_config.place(x=(width//2)-150,y=30,width=300,height=25)

        lbl_pdf=tk.Label(root)
        ft = tkFont.Font(size=14)
        lbl_pdf["font"] = ft
        lbl_pdf["fg"] = "#000000"
        lbl_pdf["justify"] = "center"
        lbl_pdf["text"] = "PDF file (*.pdf):"
        lbl_pdf.place(x=(width//2)-100,y=110,width=200,height=25)

        self.ent_translation_config=tk.Entry(root)
        self.ent_translation_config["borderwidth"] = "1px"
        ft = tkFont.Font(size=12)
        self.ent_translation_config["font"] = ft
        self.ent_translation_config["fg"] = "#000000"
        self.ent_translation_config["justify"] = "left"
        self.ent_translation_config["text"] = "*.tr"
        self.ent_translation_config.place(x=30,y=60,width=350,height=25)

        self.ent_pdf=tk.Entry(root)
        self.ent_pdf["borderwidth"] = "1px"
        ft = tkFont.Font(size=12)
        self.ent_pdf["font"] = ft
        self.ent_pdf["fg"] = "#000000"
        self.ent_pdf["justify"] = "left"
        self.ent_pdf["text"] = "*.pdf"
        self.ent_pdf.place(x=30,y=140,width=350,height=25)

    def btn_start_command(self) -> None:
        try:
            pdf_path: str = abspath(self.ent_pdf.get())
            tr_path: str = abspath(self.ent_translation_config.get())
            cfg: main.TranslationConfig = None
            if not exists(pdf_path):
                print(pdf_path)
                raise FileNotFoundError("The given PDF path does not exist!")
            # This and the elif below are bad code; fix the logic.
            # Actually, this whole method needs restructuring.
            if tr_path == '' and exists(f"{pdf_path.split('.')[0]}.tr"):
                tr_path = f"{pdf_path.split('.')[0]}.tr"
                f.open(tr_path, 'w+')
                f.close()
            elif not exists(tr_path):
                output_path: str = self.open_prompt("Please enter your desired output PDF path:")
                if exists(output_path):
                    raise FileExistsError("The given PDF path already exists!")
                f = open(output_path, 'w+')
                f.close()
                cfg = main.TranslationConfig(originalFileName=pdf_path, outputFileName=output_path)
                print(cfg.to_dict())
            else:
                cfg = main.import_tr_to_translationconfig(tr_path)
            cfg.save()
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
    root = tk.Tk()
    app = App(root)
    root.mainloop()
