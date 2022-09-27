#!/usr/bin/python

import tkinter as tk

from PIL import ImageTk, Image
from tkinter import ttk
from static.MajorTypes import get_majortypes, get_subtypes
from make_label_gui import load_barcodes

# Class to make previewing widget of labels
class LabelPreview(tk.Frame):
    
    def __init__(self, parent, *args, **kwargs):

        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.grid_propagate(0)
        self.parent = parent

        self.pack(side="left", padx=20, pady=20, fill=tk.Y)
        
        self.top_lbl = tk.Label(self, text = "Label Preview", font=('Ariel', 48))
        self.top_lbl.pack(padx=20, pady=20)

        self.create_img_widget()

    def create_img_widget(self, im_path="./tmp/tmp_label.png"):

        self.im = ImageTk.PhotoImage(Image.open(im_path))
        
        self.im_lbl = tk.Label(self, image = self.im, width = 800, height = 600)
        self.im_lbl.pack()

        self.update_btn = tk.Button(self, text = "Update", font=('Ariel', 24), command=self.update_img_widget)
        self.update_btn.pack(padx=20, pady=20)

    def update_img_widget(self, im_path="./tmp/tmp_label.png"):
        
        self.im_lbl.destroy()
        self.update_btn.destroy()

        self.im = ImageTk.PhotoImage(Image.open(im_path))
        
        self.im_lbl = tk.Label(self, image = self.im, width = 800, height = 600)
        self.im_lbl.pack()
         
        self.update_btn = tk.Button(self, text = "Update", font=('Ariel', 24), command=self.update_img_widget)
        self.update_btn.pack(padx=20, pady=20)

class PrintOut(tk.Frame):

    def __init__(self, parent, *args, **kwargs):

        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.grid_propagate(0)
        self.parent = parent

        self.pack(side = "left", padx=20, pady=20, fill=tk.X)

    def create_output_widgets(self):
        self.printout_frame = tk.Frame(self)
        self.printout_frame.pack(padx=20,pady=20)

        self.top_lbl = tk.Label(self.printout_frame, text = "Output", font=('Ariel', 48))
        self.top_lbl.pack(padx=20, fill=tk.X)

        self.main_tb = tk.Text(self.printout_frame, width=400, height=15, wrap=tk.WORD)
        self.scroll = tk.Scrollbar(self.printout_frame)
        self.scroll.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.main_tb.insert(tk.END, "Output")
        self.main_tb.pack(side=tk.LEFT, fill=tk.Y)
        self.scroll.config(command=self.main_tb.yview)
        self.main_tb.config(yscrollcommand=self.scroll.set)
        
        self.print_btn = tk.Button(self, text="Print", command=self.print_label)
        self.print_btn.pack(padx=20,pady=20)
    
    def update_text(self, text):
        self.main_tb.insert(tk.END, "\nLabel ZPL:\n{}\n".format(text))

    def print_label(self):
        self.main_tb.insert(tk.END, "\nPrinting Label...\n")

# Class to create and control all of the input for labels
class InputWidgets(tk.Frame):

    def __init__(self, parent, preview, printout, *args, **kwargs):

        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.grid_propagate(0)
        self.parent = parent
        self.preview = preview
        self.printout = printout

        self.pack(side = "left", padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.top_lbl = tk.Label(self, text = "Label Information", font=('Ariel', 48))
        self.top_lbl.pack(padx=20, pady=20)

        self.create_input_widgets()

        self.printout.create_output_widgets()

    def create_input_widgets(self):

        self.input_frame = tk.Frame(self, highlightbackground="black", highlightthickness = 2)
        self.input_frame.pack(padx=20, pady=10, fill=tk.X)
        
        self.type_frame = tk.Frame(self.input_frame)
        self.type_frame.pack(padx=20, pady=10, fill=tk.X)

        self.maj_lbl = tk.Label(self.type_frame, text="Major Type:", font=('Ariel', 24))
        self.maj_lbl.pack(side="left", padx=20, pady=10)

        majortypes = self.get_majortypes()

        self.majortype = tk.StringVar()

        self.maj_combo = ttk.Combobox(self.type_frame, textvariable=self.majortype, values = self.get_majortypes().keys())
        self.maj_combo.pack(side="left", padx=20, pady=10)

        self.sub_lbl = tk.Label(self.type_frame, text="Sub Type:", font=('Ariel', 24))
        self.sub_lbl.pack(side="left", padx=20, pady=10)

        self.subtype = tk.StringVar()
        self.sub_combo = ttk.Combobox(self.type_frame, textvariable=self.subtype, values = self.get_subtypes().values(), state="disable")
        self.sub_combo.pack(side="left", padx=20, pady=10)
        self.majortype.trace('w', self.enable_subtype)

        self.num_frame = tk.Frame(self.input_frame)
        self.num_frame.pack(padx=20, pady=10, fill=tk.X)

        self.num_lbl = tk.Label(self.num_frame, text="Number of Labels:", font =('Ariel', 24))
        self.num_lbl.pack(side="left", padx=20, pady=10)

        self.num = tk.StringVar()
        self.num_spin = tk.Spinbox(self.num_frame, from_=14, to=1000, increment=14, textvariable=self.num, state="disable")
        self.num_spin.pack(side="left", padx=20, pady=10)

        self.sn_lbl = tk.Label(self.num_frame, text="S/N:", font =('Ariel', 24))
        self.sn_lbl.pack(side="left", padx=20, pady=10)

        self.sn = tk.StringVar()
        self.sn_spin = tk.Spinbox(self.num_frame, from_=1, to=99999, textvariable=self.sn, state="disable")
        self.sn_spin.pack(side="left", padx=20, pady=10)

        self.subtype.trace('w', self.enable_num)

        self.prod_frame = tk.Frame(self.input_frame)
        self.prod_frame.pack(side="left", padx=20, pady=10)
        
        self.prod_lbl = tk.Label(self.prod_frame, text="Production Version:", font=('Ariel', 24))
        self.prod_lbl.pack(side="left", padx=20, pady=10)

        self.prod = tk.StringVar()
        self.prod_radio = tk.Radiobutton(self.prod_frame, text="Production", variable=self.prod, value="Production")
        self.prod_radio.pack(side="left", padx=20, pady=10)

        self.proto_radio = tk.Radiobutton(self.prod_frame, text="Prototype", variable=self.prod, value="Prototype")
        self.proto_radio.pack(side="left", padx=20, pady=10)

        self.make_btn = tk.Button(self, text="Make Labels", font=('Ariel', 24), command=self.get_label)
        self.make_btn.pack(padx=20, pady=20)

        self.printout = PrintOut(self)

    # Function for parsing input and making new label
    def get_label(self):
        
        lbl_info = self.get_label_info()

        print(lbl_info)

        print("Making Labels...")
        if lbl_info[0]["major_sn"] == "12" or lbl_info[0]["major_sn"] == "13":
            zpl = load_barcodes(lbl_info, wagon=True)
        else:
            zpl = load_barcodes(lbl_info)

        with open("tmp/tmp_zpl.txt", 'w') as f:
            f.write(zpl)
        f.close()

        self.preview.update_img_widget()
        
        self.printout.update_text(zpl)

    def get_label_info(self):

        majortypes = self.get_majortypes()
        subtypes = self.get_subtypes()

        self.label_info = []

        num_lbl = int(self.num.get())
        start = int(self.sn.get())

        for i in range(start, start+num_lbl):
            temp_lbl_info = {}
            temp_lbl_info["major_sn"] = str(majortypes[self.majortype.get()]["major_sn"])
            temp_lbl_info["sub_sn"] = str(subtypes[self.subtype.get()]["sub_sn"])
            temp_lbl_info["sn"] = i 
            temp_lbl_info["prod"] = self.prod == "Production"
            temp_lbl_info["major_name"] = self.majortype.get()
            temp_lbl_info["major_code"] = majortypes[self.majortype.get()]["major_code"]
            temp_lbl_info["sub_name"] = self.subtype.get()
            temp_lbl_info["sub_code"] = subtypes[self.subtype.get()]["sub_code"]
            self.label_info.append(temp_lbl_info)

        print(self.label_info)       
        return self.label_info

    #Helper functions to make interface nicer
    def enable_subtype(self, *args):
        new_vals = self.get_subtypes().keys()
        self.sub_combo['values'] = new_vals
        self.sub_combo['state'] = "normal"

    def enable_num(self, *args):
        self.sn_spin['state'] = "normal"
        self.num_spin['state'] = "normal"

        if self.majortype.get().find("Wagon") != -1:
            self.num_spin["increment"] = 2
            self.num_spin["from_"] = 2
            self.num.set("2")

    def make_preview(self):
        return
                
    def get_majortypes(self):
        return get_majortypes()

    def get_subtypes(self):
        return get_subtypes(self.majortype.get())


# Main application class
class LabelMakerApp(tk.Frame):

    def __init__(self, parent, *args, **kwargs):

        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.lbl_preview = LabelPreview(self.parent, width=600, height=1100, highlightbackground="black", highlightthickness = 2)
        self.printout = PrintOut(self.parent)
        self.lbl_inputs = InputWidgets(self.parent, self.lbl_preview, self.printout, width=1100, height = 1100, highlightbackground="black", highlightthickness = 2)



if __name__ == "__main__":
    root = tk.Tk()

    root.geometry("1800x1200")

    LabelMakerApp(root)

    root.mainloop()
