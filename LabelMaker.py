#!/usr/bin/python

import tkinter as tk

from PIL import ImageTk, Image
from tkinter import ttk
from static.MajorTypes import get_majortypes, get_subtypes


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
        
        self.im_lbl = tk.Label(self, image = self.im, width = 600, height = 600)
        self.im_lbl.pack()

        self.update_btn = tk.Button(self, text = "Update", font=('Ariel', 24), command=self.update_img_widget)
        self.update_btn.pack(padx=20, pady=20)

    def update_img_widget(self, im_path="./tmp/tmp_label2.png"):
        
        self.im_lbl.destroy()
        self.update_btn.destroy()

        self.im = ImageTk.PhotoImage(Image.open(im_path))
        
        self.im_lbl = tk.Label(self, image = self.im, width = 600, height = 600)
        self.im_lbl.pack()
         
        self.update_btn = tk.Button(self, text = "Update", font=('Ariel', 24), command=self.update_img_widget)
        self.update_btn.pack(padx=20, pady=20)

# Class to create and control all of the input for labels
class InputWidgets(tk.Frame):

    def __init__(self, parent, preview, *args, **kwargs):

        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.grid_propagate(0)
        self.parent = parent
        self.preview = preview

        self.pack(side = "left", padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.top_lbl = tk.Label(self, text = "Label Information", font=('Ariel', 48))
        self.top_lbl.pack(padx=20, pady=20)

        self.create_input_widgets()

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
        self.num_spin = tk.Spinbox(self.num_frame, from_=1, to=5000, textvariable=self.num, state="disable")
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

        self.make_btn = tk.Button(self, text="Make Labels", font=('Ariel', 24), command=self.get_label_info)
        self.make_btn.pack(padx=20, pady=20)

    # Function for parsing input and making new label
    def get_label(self):
        
        self.get_label_info()
        
        return

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
        self.lbl_inputs = InputWidgets(self.parent, self.lbl_preview, width=1100, height = 1100, highlightbackground="black", highlightthickness = 2)


if __name__ == "__main__":
    root = tk.Tk()

    root.geometry("1800x1200")

    LabelMakerApp(root)

    root.mainloop()
