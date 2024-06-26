#!/usr/bin/python3

import tkinter as tk
import tkinter.messagebox
import os

from PIL import ImageTk, Image
from tkinter import ttk
from static.MajorTypes import get_majortypes, get_subtypes, get_macs, get_vendors, get_assemblers, get_shapes, get_magazines
from make_label_gui import load_barcodes
from stash_printed import Stasher
from argparse import ArgumentParser

# Class to make previewing widget of labels
class LabelPreview(tk.Frame):
    
    def __init__(self, parent, *args, **kwargs):

        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.grid_propagate(0)
        self.parent = parent

        self.pack(side="left", padx=10, pady=20, fill=tk.Y)
        
        self.top_lbl = tk.Label(self, text = "Label Preview", font=('Ariel', 48))
        self.top_lbl.pack(padx=20, pady=20)

        self.create_img_widget()

    def create_img_widget(self, im_path="./tmp/tmp_label.png"):

        self.im = ImageTk.PhotoImage(Image.open(im_path))
        
        self.im_lbl = tk.Label(self, image = self.im, width = 700, height = 600) #height 600
        self.im_lbl.pack(fill=tk.X)

        self.update_btn = tk.Button(self, text = "Update", font=('Ariel', 24), command=self.update_img_widget)
        self.update_btn.pack(padx=20, pady=20)

    def update_img_widget(self, im_path="./tmp/tmp_label.png"):
        
        self.im_lbl.destroy()
        self.update_btn.destroy()

        self.im = ImageTk.PhotoImage(Image.open(im_path))
        
        self.im_lbl = tk.Label(self, image = self.im, width = 700, height = 600)
        self.im_lbl.pack(fill=tk.X)
         
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
        self.printout_frame.pack(padx=20)

        self.top_lbl = tk.Label(self.printout_frame, text = "Output", font=('Ariel', 48))
        self.top_lbl.pack(padx=20, fill=tk.X)

        self.main_tb = tk.Text(self.printout_frame, width=400, height=10, wrap=tk.WORD)
        self.scroll = tk.Scrollbar(self.printout_frame)
        self.scroll.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.main_tb.insert(tk.END, "Fill inputs above with label major type and subtype\nSpecify the number of labels and starting serial number\nLabels will be created sequentially by final 5 digits of serial number\n")
        self.main_tb.see(tk.END)
        self.main_tb.pack(side=tk.LEFT, fill=tk.Y)
        self.scroll.config(command=self.main_tb.yview)
        self.main_tb.config(yscrollcommand=self.scroll.set)
        
        self.print_btn = tk.Button(self, text="Print", command=self.print_label)
        self.print_btn.pack(padx=20,pady=20)
    
    def update_text(self, text):
        self.main_tb.insert(tk.END, "{}\n".format(text))
        self.main_tb.see(tk.END)

    def print_label(self):
        self.main_tb.insert(tk.END, "\nPrinting Label...\n")
        #self.stasher.backup()
        os.system("lp -d Zebra -o raw tmp/tmp.zpl")

    def repack_print(self):
        self.print_btn.destroy()

        self.print_btn = tk.Button(self, text="Print", command=self.print_label)
        self.print_btn.pack(padx=20, pady=20)

# Class to create and control all of the input for labels
class InputWidgets(tk.Frame):

    def __init__(self, parent, preview, printout, borders, *args, **kwargs):

        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.grid_propagate(0)
        self.parent = parent
        self.preview = preview
        self.printout = printout
        self.temp_widgets = []

        self.borders = borders

        self.pack(side = "left", padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.top_lbl = tk.Label(self, text = "Label Information", font=('Ariel', 12))
        self.top_lbl.pack(padx=20, pady=20)

        self.create_input_widgets()

        self.printout.create_output_widgets()

    def clear_temp_widgets(self):

        for wid in self.temp_widgets:
            wid.destroy()

        self.temp_widgets = []

    def create_input_widgets(self):
        print("In LabelMaker.py: create_input_widgets")

        os.system("lp -d Zebra -o raw setLabelLength_Nominal.zpl")

        self.input_frame = tk.Frame(self, highlightbackground="black", highlightthickness = 2)
        self.input_frame.pack(padx=20, pady=5, fill=tk.X)
        
        self.type_frame = tk.Frame(self.input_frame)
        self.type_frame.pack(padx=20, pady=5, fill=tk.X)

        self.maj_lbl = tk.Label(self.type_frame, text="Major Type:", font=('Ariel', 16))
        self.maj_lbl.pack(side="left", padx=20, pady=5)

        self.majortype = tk.StringVar()

        self.maj_combo = ttk.Combobox(self.type_frame, textvariable=self.majortype, values = list(self.get_majortypes().keys()))
        self.maj_combo.pack(side="left", padx=20, pady=5)

        self.majortype.trace('w', self.enable_other_widgets)

        self.sub_lbl = tk.Label(self.type_frame, text="Sub Type:", font=('Ariel', 16))
        self.sub_lbl.pack(side="left", padx=20, pady=5)

        self.subtype = tk.StringVar()
        self.sub_combo = ttk.Combobox(self.type_frame, textvariable=self.subtype, values = list(self.get_subtypes().values()), state="normal")
        self.sub_combo.pack(side="left", padx=20, pady=5)
        self.majortype.trace('w', self.enable_subtype)

        print(self.sub_combo.get(), "!!")

        self.make_btn = tk.Button(self, text="Make Labels", font=('Ariel', 16), command=self.get_label)
        self.make_btn.pack(padx=20, pady=20)

        self.printout = PrintOut(self)
        print(self.printout)

    def create_module_inputs(self):

        os.system("lp -d Zebra -o raw setLabelLength_Module.zpl")

        self.clear_temp_widgets()

        self.rows_frame = tk.Frame(self.input_frame)
        self.rows_frame.pack(padx=20, pady=5, fill=tk.X)

        self.temp_widgets.append(self.rows_frame)

        self.num_frame = tk.Frame(self.input_frame)
        self.num_frame.pack(padx=20, pady=5, fill=tk.X)

        self.temp_widgets.append(self.num_frame)

        self.sn_frame = tk.Frame(self.input_frame)
        self.sn_frame.pack(padx=20, pady=5, fill=tk.X)

        self.temp_widgets.append(self.sn_frame)

        self.prod_frame = tk.Frame(self.input_frame)
        self.prod_frame.pack(padx=20, pady=5, fill=tk.X)
        
        self.temp_widgets.append(self.prod_frame)

        self.num_lbl = tk.Label(self.num_frame, text="Number of Labels:", font =('Ariel', 16))
        self.num_lbl.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.num_lbl)

        self.num = tk.StringVar()
        self.num_spin = tk.Spinbox(self.num_frame, from_=10, to=1000, increment=10, textvariable=self.num, state="normal")
        self.num_spin.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.num_spin)

        self.MAC_lbl = tk.Label(self.num_frame, text="MAC:", font=('Ariel', 16))
        self.MAC_lbl.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.MAC_lbl)

        self.mac = tk.StringVar()
        self.mac_combo = ttk.Combobox(self.num_frame, textvariable=self.mac, values = list(get_macs().keys()))
        self.mac_combo.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.mac_combo)

        self.roc_lbl = tk.Label(self.sn_frame, text="ROC Version:", font=('Ariel', 16))
        self.roc_lbl.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.roc_lbl)

        self.roc_num = tk.StringVar()
        print(['X'] + [str(x) for x in range(1,5)])
        self.roc_combo = ttk.Combobox(self.sn_frame, textvariable=self.roc_num, values = ['X'] + [str(x) for x in range(1,5)])
        self.roc_combo.pack(side="left", padx=20, pady=5)

        #self.roc_spin = tk.Spinbox(self.sn_frame, from_=1, to=10, increment=1, textvariable=self.roc_num, state="normal")
        #self.roc_spin.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.roc_combo)

        self.sn_lbl = tk.Label(self.sn_frame, text="S/N:", font =('Ariel', 16))
        self.sn_lbl.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.sn_lbl)

        self.sn = tk.StringVar()
        self.sn_spin = tk.Spinbox(self.sn_frame, from_=1, to=999999, textvariable=self.sn, state="normal")
        self.sn_spin.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.sn_spin)

        self.prod_lbl = tk.Label(self.prod_frame, text="Production Version:", font=('Ariel', 16))
        self.prod_lbl.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.prod_lbl)

        self.prod = tk.StringVar()
        self.prod_radio = tk.Radiobutton(self.prod_frame, text="Production", variable=self.prod, value="Production")
        self.prod_radio.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.prod_radio)

        self.proto_radio = tk.Radiobutton(self.prod_frame, text="Prototype", variable=self.prod, value="Prototype")
        self.proto_radio.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.proto_radio)

        self.make_btn["command"] = self.get_label
        self.printout.repack_print()

    def create_hexaboard_inputs(self):

        os.system("lp -d Zebra -o raw setLabelLength_Nominal.zpl")

        self.clear_temp_widgets()

        self.sub_combo["state"] = "disable"

        self.rows_frame = tk.Frame(self.input_frame)
        self.rows_frame.pack(padx=20, pady=5, fill=tk.X)

        self.temp_widgets.append(self.rows_frame)

        self.num_frame = tk.Frame(self.input_frame)
        self.num_frame.pack(padx=20, pady=5, fill=tk.X)

        self.temp_widgets.append(self.num_frame)

        self.roc_frame = tk.Frame(self.input_frame)
        self.roc_frame.pack(padx=20, pady=5, fill=tk.X)

        self.temp_widgets.append(self.roc_frame)

        self.prod_frame = tk.Frame(self.input_frame)
        self.prod_frame.pack(padx=20, pady=5, fill=tk.X)
        
        self.temp_widgets.append(self.prod_frame)

        self.sn_frame = tk.Frame(self.input_frame)
        self.sn_frame.pack(padx=20, pady=5, fill=tk.X)

        self.temp_widgets.append(self.sn_frame)

        self.num_lbl = tk.Label(self.num_frame, text="Number of Labels:", font =('Ariel', 16))
        self.num_lbl.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.num_lbl)

        self.num = tk.StringVar()
        self.num_spin = tk.Spinbox(self.num_frame, from_=14, to=10000, increment=14, textvariable=self.num, state="normal")
        self.num_spin.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.num_spin)

        self.gen_lbl = tk.Label(self.roc_frame, text="Generation:", font=('Ariel', 16))
        self.gen_lbl.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.gen_lbl)

        self.gen_num = tk.StringVar()
        self.gen_combo = ttk.Combobox(self.roc_frame, textvariable=self.gen_num, values = list(range(0,5)))
        self.gen_combo.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.gen_combo)

        self.roc_lbl = tk.Label(self.roc_frame, text="ROC Version:", font=('Ariel', 16))
        self.roc_lbl.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.roc_lbl)

        self.roc_num = tk.StringVar()
        self.roc_combo = ttk.Combobox(self.roc_frame, textvariable=self.roc_num, values = ['2', '4', 'C'])
        self.roc_combo.pack(side="left", padx=20, pady=5)

        #self.roc_spin = tk.Spinbox(self.roc_frame, from_=1, to=10, increment=1, textvariable=self.roc_num, state="normal")
        #self.roc_spin.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.roc_combo)

        self.vendor_lbl = tk.Label(self.prod_frame, text="PCB Vendor:", font=('Ariel', 16))
        self.vendor_lbl.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.vendor_lbl)

        self.vendor = tk.StringVar()
        self.vendor_combo = ttk.Combobox(self.prod_frame, textvariable=self.vendor, values = list(get_vendors().keys()))
        self.vendor_combo.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.vendor_combo)

        self.assembler_lbl = tk.Label(self.prod_frame, text="Assembler:", font=('Ariel', 16))
        self.assembler_lbl.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.assembler_lbl)

        self.assembler = tk.StringVar()
        self.assembler_combo = ttk.Combobox(self.prod_frame, textvariable=self.assembler, values = list(get_assemblers().keys()))
        self.assembler_combo.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.assembler_combo)

        #self.prod_lbl = tk.Label(self.prod_frame, text="Production Version:", font=('Ariel', 16))
        #self.prod_lbl.pack(side="left", padx=20, pady=5)

        #self.temp_widgets.append(self.prod_lbl)

        #self.prod = tk.StringVar()
        #self.prod_radio = tk.Radiobutton(self.prod_frame, text="Production", variable=self.prod, value="Production")
        #self.prod_radio.pack(side="left", padx=20, pady=5)

        #self.temp_widgets.append(self.prod_radio)

        #self.proto_radio = tk.Radiobutton(self.prod_frame, text="Prototype", variable=self.prod, value="Prototype")
        #self.proto_radio.pack(side="left", padx=20, pady=5)

        #self.temp_widgets.append(self.proto_radio)

        self.shape_lbl = tk.Label(self.sn_frame, text="Shape:", font=('Ariel', 16))
        self.shape_lbl.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.shape_lbl)

        self.shape = tk.StringVar()
        self.shape_combo = ttk.Combobox(self.sn_frame, textvariable=self.shape, values = list(get_shapes().keys()))
        self.shape_combo.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.shape_combo)

        self.temp_widgets.append(self.vendor_combo)
        self.sn_lbl = tk.Label(self.sn_frame, text="S/N:", font =('Ariel', 16))
        self.sn_lbl.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.sn_lbl)

        self.sn = tk.StringVar()
        self.sn_spin = tk.Spinbox(self.sn_frame, from_=1, to=999999, textvariable=self.sn, state="normal")
        self.sn_spin.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.sn_spin)

        self.make_btn["command"] = self.get_label_hexaboard
        self.printout.repack_print()

    def create_tile_inputs(self):

        os.system("lp -d Zebra -o raw setLabelLength_Tile.zpl")

        self.clear_temp_widgets()

        self.printout.update_text("\nNote: Subtype must be constructed from size for Tiles")

        self.sub_combo["state"] = "disable"

        self.rows_frame = tk.Frame(self.input_frame)
        self.rows_frame.pack(padx=20, pady=5, fill=tk.X)

        self.temp_widgets.append(self.rows_frame)

        self.num_frame = tk.Frame(self.input_frame)
        self.num_frame.pack(padx=20, pady=5, fill=tk.X)

        self.temp_widgets.append(self.num_frame)

        ##########
        self.magazine_lbl = tk.Label(self.num_frame, text="Initial Magazine:", font=('Ariel', 12))
        self.magazine_lbl.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.magazine_lbl)

        self.magazine = tk.StringVar()
        self.magazine_spin = ttk.Combobox(self.num_frame, textvariable=self.magazine, state="normal", values = list(get_magazines()))
        self.magazine_spin.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.magazine_spin)
        #############

        self.num_lbl = tk.Label(self.num_frame, text="Number of Labels:", font =('Ariel', 16))
        self.num_lbl.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.num_lbl)

        self.num = tk.StringVar()
        self.num_spin = tk.Spinbox(self.num_frame, from_=8, to=1000, increment=8, textvariable=self.num, state="normal")
        self.num_spin.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.num_spin)

####################################################################################
        self.size_lbl = tk.Label(self.rows_frame, text="Size:", font=('Ariel', 16))
        self.size_lbl.pack(side="left", padx=20, pady=5)
        
        self.temp_widgets.append(self.size_lbl)

        self.size = tk.StringVar()
        self.size_spin = tk.Spinbox(self.rows_frame, from_=1, to=1000, increment=1, textvariable=self.size, state="normal")
        self.size_spin.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.size_spin)

        self.batch_lbl = tk.Label(self.rows_frame, text="Batch:", font=('Ariel', 16))
        self.batch_lbl.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.batch_lbl)

        self.batch = tk.StringVar()
        self.batch_spin = tk.Spinbox(self.rows_frame, from_=1, to=9999, increment=1, textvariable=self.batch, state="normal")
        self.batch_spin.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.batch_spin)

#################################################
        self.sn_frame = tk.Frame(self.input_frame)
        self.sn_frame.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.sn_frame)

        self.sn_lbl = tk.Label(self.sn_frame, text="S/N:", font =('Ariel', 16))
        self.sn_lbl.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.sn_lbl)

        self.sn = tk.StringVar()
        self.sn_spin = tk.Spinbox(self.sn_frame, from_=1, to=999999, textvariable=self.sn, state="normal")
        self.sn_spin.pack(side="left", padx=20, pady=5)
        if self.majortype.get().find("Tile PCB") != -1:
            self.create_tile_pcb_mod_inputs("PCB")

        self.temp_widgets.append(self.sn_spin)
###
        self.nummag_lbl = tk.Label(self.sn_frame, text="Number of Labels/Magazine:", font =('Ariel', 12))
        self.nummag_lbl.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.nummag_lbl)

        self.nummag = tk.StringVar()
        self.nummag_spin = tk.Spinbox(self.sn_frame, from_=1, to=1000, textvariable=self.nummag, state="normal")
        self.nummag_spin.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.nummag_spin)
##

        self.make_btn["command"] = self.get_label_tile
        self.printout.repack_print()

    def create_tile_pcb_mod_inputs(self, pcb_mod):

        self.clear_temp_widgets()

        self.printout.update_text("\nNote: Subtype must be constructed from shape, rows, geometry, and SiPM for Tile PCB and Tile Modules")

        self.sub_combo["state"] = "disable"

        self.rows_frame = tk.Frame(self.input_frame)
        self.rows_frame.pack(padx=20, pady=5, fill=tk.X)

        self.temp_widgets.append(self.rows_frame)

        self.size_lbl = tk.Label(self.rows_frame, text="Tile Shape:", font=('Ariel', 16))
        self.size_lbl.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.size_lbl)

        self.size = tk.StringVar()
        self.size_combo = ttk.Combobox(self.rows_frame, textvariable=self.size, values = ['A', 'B', 'C', 'D', 'E', 'G', 'J', 'K'], state="normal")
        self.size_combo.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.size_combo)

        self.rows_lbl = tk.Label(self.rows_frame, text="Rows:", font=('Ariel', 16))
        self.rows_lbl.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.rows_frame)

        self.rows = tk.StringVar()
        self.rows_combo = ttk.Combobox(self.rows_frame, textvariable=self.rows, values = ['11', '12'])
        self.rows_combo.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.rows_combo)

        self.sipm_frame = tk.Frame(self.input_frame)
        self.sipm_frame.pack(padx=20, pady=5, fill=tk.X)

        self.temp_widgets.append(self.sipm_frame)

        self.geometry_lbl = tk.Label(self.sipm_frame, text="Geometry:", font=('Ariel', 16))
        self.geometry_lbl.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.geometry_lbl)

        self.geometry = tk.StringVar()
        self.geometry_combo = ttk.Combobox(self.sipm_frame, textvariable=self.geometry, values = ['L', 'R', 'F'])
        self.geometry_combo.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.geometry_combo)

        self.sipm_lbl = tk.Label(self.sipm_frame, text="SiPM:", font=('Ariel', 16))
        self.sipm_lbl.pack(side='left', padx=20, pady=5)

        self.temp_widgets.append(self.sipm_lbl)

        if pcb_mod == "PCB":
            self.sipm = tk.StringVar()
            self.sipm_combo = ttk.Combobox(self.sipm_frame, textvariable=self.sipm, values = ['4', '9'])
            self.sipm_combo.pack(side="left", padx=20, pady=5)
        else:
            self.sipm = tk.StringVar()
            self.sipm_combo = ttk.Combobox(self.sipm_frame, textvariable=self.sipm, values = ['C', 'M', '9'])
            self.sipm_combo.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.sipm_combo)

        self.sn_frame = tk.Frame(self.input_frame)
        self.sn_frame.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.sn_frame)

        self.sn_lbl = tk.Label(self.sn_frame, text="S/N:", font =('Ariel', 16))
        self.sn_lbl.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.sn_lbl)

        self.sn = tk.StringVar()
        self.sn_spin = tk.Spinbox(self.sn_frame, from_=1, to=999999, textvariable=self.sn, state="normal")
        self.sn_spin.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.sn_spin)

        self.make_btn["command"] = self.get_label_tile
        self.printout.repack_print()

    def create_general_inputs(self):

        self.clear_temp_widgets()

        self.sub_combo["state"] = "normal"

        self.num_frame = tk.Frame(self.input_frame)
        self.num_frame.pack(padx=20, pady=5, fill=tk.X)

        self.temp_widgets.append(self.num_frame)

        self.num_lbl = tk.Label(self.num_frame, text="Number of Labels:", font =('Ariel', 16))
        self.num_lbl.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.num_lbl)

        self.num = tk.StringVar()
        self.num_spin = tk.Spinbox(self.num_frame, from_=14, to=1000, increment=14, textvariable=self.num, state="normal")
        self.num_spin.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.num_spin)

        self.sn_lbl = tk.Label(self.num_frame, text="S/N:", font =('Ariel', 16))
        self.sn_lbl.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.sn_lbl)

        self.sn = tk.StringVar()
        self.sn_spin = tk.Spinbox(self.num_frame, from_=1, to=999999, textvariable=self.sn, state="normal")
        self.sn_spin.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.sn_spin)

        self.subtype.trace('w', self.enable_num)

        self.prod_frame = tk.Frame(self.input_frame)
        self.prod_frame.pack(side="left", padx=20, pady=5)
        
        self.temp_widgets.append(self.prod_frame)

        self.prod_lbl = tk.Label(self.prod_frame, text="Production Version:", font=('Ariel', 16))
        self.prod_lbl.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.prod_lbl)

        self.prod = tk.StringVar()
        self.prod_radio = tk.Radiobutton(self.prod_frame, text="Production", variable=self.prod, value="Production")
        self.prod_radio.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.prod_radio)

        self.proto_radio = tk.Radiobutton(self.prod_frame, text="Prototype", variable=self.prod, value="Prototype")
        self.proto_radio.pack(side="left", padx=20, pady=5)

        self.temp_widgets.append(self.proto_radio)

        self.make_btn["command"] = self.get_label
        self.printout.repack_print()

    # Function for parsing input and making new label
    def get_label(self):
        print("LabelMaker.py: get_label") 

        lbl_info = self.get_label_info()

        print(lbl_info)

        print("Making Labels...")
        if lbl_info[0]["major_sn"] in ["12", "13", "14", "15"]: #remove 29
            zpl, barcodes = load_barcodes(lbl_info, wagon=True, borders = self.borders)
        elif lbl_info[0]["major_sn"] in ["29"]:
            if lbl_info[0]["sub_code"] in ["FFH3"] or lbl_info[0]["sub_code"] in ["FBH3"]:
                os.system("lp -d Zebra -o raw setLabelLength_Flex.zpl")
                zpl, barcodes = load_barcodes(lbl_info, flex=True, borders = self.borders)
            else:
                zpl, barcodes = load_barcodes(lbl_info, wagon=True, borders = self.borders)
        elif lbl_info[0]["major_sn"] in ["8","9"]:
            print(self.mac.get(), self.roc_num.get())
            zpl, barcodes = load_barcodes(lbl_info, module=True, MAC=get_macs()[self.mac.get()]["mac_code"], ROC=self.roc_num.get(), borders = self.borders)
        else:
            zpl, barcodes = load_barcodes(lbl_info, borders = self.borders)

        self.stasher = Stasher(barcodes)
        overlap, serial = self.stasher.search()

        if overlap:
            message = "The following serial numbers have already been printed:\n"
            for s in serial:
                message += "{}\n".format(s)
            message += "Continue anyway?"
            override = tkinter.messagebox.askyesno('Warning!', message)
            if not override: return
            else:
                override = tkinter.messagebox.askyesno('Final Warning!', 'You are risking printing the same label twice which could cause major confusion. Are you sure?')
                if not override: return

        with open("tmp/tmp.zpl", 'w') as f:
            f.write(zpl)
        f.close()

        self.preview.update_img_widget()
       
        for i in barcodes:
            self.printout.update_text("Making label with S/N: {}".format(i.full_serial))

    def get_label_info(self):

        print("Getting label info")

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

        return self.label_info

    def get_label_tile(self):
        
        lbl_info = self.get_label_info_tile()

        print(lbl_info)

        print("Making Labels...")
        zpl, barcodes = load_barcodes(lbl_info, tile=True, borders = self.borders)

        self.stasher = Stasher(barcodes)
        overlap, serial = self.stasher.search()

        if overlap:
            message = "The following serial numbers have already been printed:\n"
            for s in serial:
                message += "{}\n".format(s)
            message += "Continue anyway?"
            override = tkinter.messagebox.askyesno('Warning!', message)
            if not override: return
            else:
                override = tkinter.messagebox.askyesno('Final Warning!', 'You are risking printing the same label twice which could cause major confusion. Are you sure?')
                if not override: return

        with open("tmp/tmp.zpl", 'w') as f:
            f.write(zpl)
        f.close()

        self.preview.update_img_widget()
       
        for i in barcodes:
            self.printout.update_text("Making label with S/N: {}".format(i.full_serial))

    def get_label_hexaboard(self):
        
        lbl_info = self.get_label_info_hexaboard()
        print(lbl_info)

        print("Making Labels...")
        zpl, barcodes = load_barcodes(lbl_info, hexaboard=True, borders = self.borders)

        self.stasher = Stasher(barcodes)
        overlap, serial = self.stasher.search()

        if overlap:
            message = "The following serial numbers have already been printed:\n"
            for s in serial:
                message += "{}\n".format(s)
            message += "Continue anyway?"
            override = tkinter.messagebox.askyesno('Warning!', message)
            if not override: return
            else:
                override = tkinter.messagebox.askyesno('Final Warning!', 'You are risking printing the same label twice which could cause major confusion. Are you sure?')
                if not override: return

        with open("tmp/tmp.zpl", 'w') as f:
            f.write(zpl)
        f.close()

        self.preview.update_img_widget()
       
        for i in barcodes:
            self.printout.update_text("Making label with S/N: {}".format(i.full_serial))

    def get_label_info_hexaboard(self):

        majortypes = self.get_majortypes()
        subtypes = self.get_subtypes()

        roc_version = self.roc_num.get()
        gen_version = self.gen_num.get()

        shape = self.shape.get()
        vendor = self.vendor.get()
        assembler = self.assembler.get()

        shape_code = get_shapes()[shape]["shape_code"]
        vendor_code = get_vendors()[vendor]["vendor_code"]
        assembler_code = get_assemblers()[assembler]["assembler_code"]

        self.label_info = []

        num_lbl = int(self.num.get())
        start = int(self.sn.get())
        adjust_serial = 0

        for i in range(start, start+num_lbl):
            temp_lbl_info = {}
            temp_lbl_info["major_sn"] = str(majortypes[self.majortype.get()]["major_sn"])
            #temp_lbl_info["sub_sn"] = str(subtypes[self.subtype.get()]["sub_sn"])
            #temp_lbl_info["pcb_vendor"] = get_vendors()[vendor]["vendor_code"]
            #temp_lbl_info["assembler"] = get_vendors()[assembler]["assembler_code"]
            temp_lbl_info["sn"] = i - adjust_serial
            temp_lbl_info["major_name"] = self.majortype.get()
            temp_lbl_info["major_code"] = majortypes[self.majortype.get()]["major_code"]
            temp_lbl_info["sub_name"] = "{}{} {} {}{}".format(shape_code, gen_version, roc_version, vendor_code, assembler_code)
            temp_lbl_info["sub_code"] = "{}{}{}{}{}".format(shape_code, gen_version, roc_version, vendor_code, assembler_code)
            self.label_info.append(temp_lbl_info)

        print(self.label_info)       
        return self.label_info

    def get_label_info_tile(self):

        majortypes = self.get_majortypes()
        size = self.size.get()
        batch = self.batch.get()
        startmag = self.magazine.get()
        mag_index = get_magazines().index(startmag) 
#        print("!!!!", magindex)
        self.label_info = []
        magperlab = int(self.nummag.get())
        num_lbl = int(self.num.get())
        start = int(self.sn.get())
        adjust_serial = 0
        adjust_mag = 0
        label_count = 0

        for i in range(start, start+num_lbl):
            print("i:", i)
            if i % magperlab == start and i != start:
                adjust_serial += magperlab
            print("Adjust serial:", adjust_serial)
            temp_lbl_info = {}
            temp_lbl_info["major_sn"] = str(majortypes[self.majortype.get()]["major_sn"])
            temp_lbl_info["size"] = str(size)
            temp_lbl_info["batch"] = str(batch)
            temp_lbl_info["sn"] = i - adjust_serial
            print("i - adjust_serial (SN):", temp_lbl_info["sn"])
            temp_lbl_info["major_name"] = self.majortype.get()
            temp_lbl_info["major_code"] = majortypes[self.majortype.get()]["major_code"]
            if temp_lbl_info["major_code"] == "TC":
                temp_lbl_info["sub_name"] = "PL"
            else:
                temp_lbl_info["sub_name"] = "B"
       
            mag_index = (i-1) // (magperlab)
            print("Mag index:", mag_index)
            temp_lbl_info["mag_code"] = "{}".format(get_magazines()[mag_index])
            print("Mag Code:", temp_lbl_info["mag_code"])
            self.label_info.append(temp_lbl_info)
        print(self.label_info)       
        return self.label_info
    #Helper functions to make interface nicer
    def enable_subtype(self, *args):
        new_vals = list(self.get_subtypes().keys())
        self.sub_combo['values'] = new_vals
        self.sub_combo['state'] = "normal"

    def enable_num(self, *args):
        self.sn_spin['state'] = "normal"
        self.num_spin['state'] = "normal"

        if self.majortype.get().find("Wagon") != -1 or self.majortype.get().find("Concentrator") != -1 or self.majortype.get().find("TB Cable") != 1:
            self.num_spin["increment"] = 2
            self.num_spin["from_"] = 2
            self.num.set("2")
        elif "Tile" in self.majortype.get():
            self.num_spin["increment"] = 8
            self.num_spin["from_"] = 8
            self.num_spin.set("8")
        elif any(x in self.majortype.get() for x in ["LD Module", "HD Module"]):
            self.num_spin["increment"] = 10
            self.num_spin["from_"] = 10
            self.num_spin.set("10")
        else:
            self.num_spin["increment"] = 14
            self.num_spin["from_"] = 14
            self.num.set("14")

    def enable_other_widgets(self, *args):
        if self.majortype.get().find("Tile PCB") != -1:
            self.create_tile_pcb_mod_inputs("PCB")
        elif self.majortype.get().find("Tile Module") != -1:
            self.create_tile_pcb_mod_inputs("Module")
        elif self.majortype.get().find("Bare") != -1 or self.majortype.get().find("Wrapped") != -1:
            self.create_tile_inputs()
        elif "Module" in self.majortype.get():
            self.create_module_inputs()
        elif "Hexaboard" in self.majortype.get():
            self.create_hexaboard_inputs()
        else:
            self.create_general_inputs()

    def make_preview(self):
        return
                
    def get_majortypes(self):
        return get_majortypes()

    def get_subtypes(self):
        return get_subtypes(self.majortype.get())

    def get_mag(self):
        return get_magazines()

# Main application class
class LabelMakerApp(tk.Frame):

    def __init__(self, parent, *args, **kwargs):

        self.borders = kwargs["borders"]
        temp_kwargs = {}
        for key,item in kwargs.items():
            if key != "borders":
                temp_kwargs[key] = item

        kwargs = temp_kwargs

        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.lbl_preview = LabelPreview(self.parent, width=600, height=1100, highlightbackground="black", highlightthickness = 2) #change height from 1100 to 650
        self.printout = PrintOut(self.parent)
        self.lbl_inputs = InputWidgets(self.parent, self.lbl_preview, self.printout, borders = self.borders,width=1100, height = 1100, highlightbackground="black", highlightthickness = 2) #change height from 1100 to 500



if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument("--borders", action="store_true", default=False, help="Show borders around labels in preview (will also print)")

    args = parser.parse_args()

    root = tk.Tk()

    root.geometry("1800x1200") #originally 1800x1200

    LabelMakerApp(root, borders = args.borders)

    root.mainloop()
