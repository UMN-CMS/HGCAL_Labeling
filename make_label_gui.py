#!/usr/bin/python3

from zpl import Label
import os
import argparse
import time
from PIL import Image
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
import io

class myLabel(Label):
    
    def __init__(self, height=25.4, width=88.9, dpmm=8.0):
        Label.__init__(self,height, width, dpmm)

    def write_datamatrix(self, height=1, orientation='N', sq=200, aspect=1):

        self.code += ("^BX{},{},{},,,,,{}").format(orientation, height, sq, aspect)

    def preview(self, index=0, outfile="tmp/tmp_label.png"):
        try:
            url = 'http://api.labelary.com/v1/printers/%idpmm/labels/%fx%f/%i/' % (
                self.dpmm, self.width/25.4, self.height/25.4, index)
            res = urlopen(url, self.dumpZPL().encode()).read()
            im = Image.open(io.BytesIO(res))
            #im.show()
            im.save(outfile)
        except IOError as e:
            print(e)
            raise Exception("Invalid preview received, mostlikely bad ZPL2 code uploaded.")

class Barcode:
    
    def __init__(self, label_dict, tile=False, module=False, hexaboard=False, MAC="", ROC="", vendor="", production=False):
        print("In __init__ in class Barcode")
        self.serial = str(label_dict['sn'])

        self.first = '320' #if not label_dict['prod'] else '320'
        self.majorname = label_dict["major_name"]
        self.nickname = label_dict["sub_name"]

        if tile:
            self.subtype = "{:02d}".format(int(label_dict['major_sn'])) + "{:02d}".format(int(label_dict['size'])) + "{:04d}".format(int(label_dict['batch']))
            self.batch = int(label_dict['batch'])
            self.size = "{:02d}".format(int(label_dict['size']))
            self.subcode = "{:02d}".format(int(label_dict['size'])) + "{:04d}".format(int(label_dict['batch']))
            self.mag = label_dict['mag_code']
            self.code = label_dict["major_code"] + self.subcode
            self.full_serial = self.first + self.code + self.mag + "{:03d}".format(int(self.serial))
            print("FULL SERIAL: ", self.full_serial)
        elif module:
            self.subtype = "{:02d}".format(int(label_dict['major_sn'])) + "{:03d}".format(int(label_dict['sub_sn']))
            self.subcode = label_dict["major_code"] + label_dict['sub_code']+ ROC 
            self.mac_code = MAC
            self.code = label_dict["major_code"] + label_dict["sub_code"] + ROC + self.mac_code 
            self.major_code = label_dict["major_code"]
            self.sub_code = label_dict["sub_code"]
            self.full_serial = self.first + self.code + "{:04d}".format(int(self.serial))
            print(self.full_serial)
            self.roc_version = ROC
            self.thickness = "300um" if label_dict['sub_sn'][1] is "3" else "200um"
        elif hexaboard:
            self.subcode = label_dict["sub_code"]
            self.code = label_dict["major_code"] + label_dict["sub_code"]
            self.full_serial = self.first + self.code + "{:05d}".format(int(self.serial))
            self.nickname = self.nickname.split(" ")
            self.shape_gen = str(self.nickname[0])
            self.roc = self.nickname[1]
            self.va = " ".join(self.nickname[2:])
        else:
            self.subtype = "{:02d}".format(int(label_dict['major_sn'])) + label_dict['sub_sn']
            self.subcode = label_dict["sub_code"]
            self.code = label_dict["major_code"] + label_dict["sub_code"]
            if vendor != "":
                self.full_serial = self.first + self.code + "{}{:05d}".format(vendor, int(self.serial))
                self.vendor = vendor
            else:
                self.full_serial = self.first + self.code + "{:06d}".format(int(self.serial))
        
    def get_nickname(self):

        labels = {  
                    "060001":  "LD HB1 P",
                    "060002":  "LD HB1 E",
                    "100000":  "EngV1",
                    "100001":  "EngV2",
                    "100002":  "EngV2b",
                    "100300":  "EngV3",
                    "100100":  "Eng",
                    "110002":  "WagV2-E",
                    "110003":  "WagV2-W",
                    "123101":  "Wag3W01",
                    "123201":  "Wag3E01",
                    "500001":  "TBT",
                    "500002":  "TBT2",
                    "500011":  "HXCTR",
                    "510001":  "IntrPos",
                    "510011":  "WagW-TBT",
                    "510012":  "WagE-TBT",
                    "510021":  "FMC-EngV2",
                    "990001":  "Test"
                 }
    
        self.nickname = labels[str(self.subtype)]
        return self.nickname

    def get_label_name(self):
        return self.nickname


def produce_barcode(barcode, x_offset=0, y_offset=0):

    l = myLabel(9.525, 9.525, dpmm=8.0)

    l.origin(0.25,0.75)
    l.write_text(barcode.nickname, char_height=2, char_width=2, line_width=8, orientation='R', justification='L')
    l.endorigin()

    l.origin(2.75, 0.75)
    l.write_datamatrix(height=3, orientation='N', sq=200, aspect=1)
    l.write_text('{}'.format(barcode.full_serial))
    l.endorigin()

    l.origin(1.70, 6.25)
    l.write_text("{:06d}".format(int(barcode.serial)), char_height=2, char_width=2, line_width=6.3, orientation='N', justification='R')
    l.endorigin()
    
    print(l.dumpZPL())
    #l.preview()

    with open("{}/{}.zpl".format(barcode.get_nickname(), barcode.get_label_name()),'w') as f:
        f.write(l.dumpZPL())
    f.close()
    l.preview()

    return l

def produce_wagon_barcode(barcode, barcode_dict, x_offset=0, y_offset=0):

    l = myLabel(9.525, 50.8, dpmm=8.0)

    l.origin(0.75, 0.75)
    l.write_datamatrix(height=4, orientation='N', sq=200, aspect=1)
    l.write_text('{}'.format(barcode.full_serial))
    l.endorigin()

    l.origin(9.6, 1.25)
    l.write_text(barcode.serial, char_height=2, char_width=2, line_width=7.25, orientation='B', justification='C')
    l.endorigin()

    l.origin(9.1, 1.0)
    l.draw_box(20, 62, thickness=2, color='B', rounding=0)
    l.endorigin()
    
    l.origin(12, 1.8)
    l.write_text("{}".format(), char_height=3, char_width=3, line_width=40, orientation='N', justification='L')
    l.endorigin()

    l.origin(12, 5.6)
    l.write_text("West [3+0]", char_height=3, char_width=3, line_width=40, orientation='N', justification='L')
    l.endorigin()

    l.origin(27, 0.5)
    l.draw_box(2, 68, thickness=1, color='B', rounding=0)
    l.endorigin()

    l.origin(28, 1.8)
    l.write_text("\"Righty Python\"", char_height=3, char_width=3, line_width=40, orientation='N', justification='L')
    l.endorigin()

    l.origin(28, 5.6)
    l.write_text("S/N: {}".format(barcode.serial), char_height=3, char_width=3, line_width=40, orientation='N', justification='L')
    l.endorigin()

    print(l.dumpZPL())
    #l.preview()

    #with open("{}/{}.zpl".format(barcode.get_nickname(), barcode.get_label_name()),'w') as f:
    #    f.write(l.dumpZPL())
    #f.close()
    l.preview()

    return l

def add_to_megalabel(megalabel, barcode, x_offset=1.5875, y_offset=1.5875, tile=False, hexaboard=False, borders=False):

    if tile:
        if borders:
            megalabel.origin(-0.125+x_offset,-0.125+y_offset)
            megalabel.draw_box(153, 153, thickness=1, color='B', rounding=2)
            megalabel.endorigin()

        megalabel.origin(2.25+x_offset,2.5+y_offset)
        if barcode.majorname == 'Wrapped Cast Machined Tile':
            megalabel.write_text(barcode.get_label_name(), char_height=2.5, char_width=2.5, line_width=16, orientation='N', justification='L')
    else:
        if borders:
            megalabel.origin(-0.125+x_offset,-0.125+y_offset)
            megalabel.draw_box(76, 76, thickness=1, color='B', rounding=2)
            megalabel.endorigin()
        if hexaboard:
            megalabel.origin(0.50+x_offset,0.85+y_offset)
            megalabel.write_text(barcode.shape_gen, char_height=2, char_width=2, line_width=8, orientation='R', justification='L')
            megalabel.endorigin()
            
            if barcode.roc == '2':
                megalabel.origin(0.75+x_offset, 3.25+y_offset)
                megalabel.reverse_print()
                megalabel.draw_box(14.5, 16, thickness=14)
                megalabel.endorigin()
            elif barcode.roc == 'C':
                megalabel.origin(0.25+x_offset, 3.25+y_offset)
                megalabel.draw_box(18, 16, thickness=1)
                megalabel.endorigin()

            megalabel.origin(0.50+x_offset,3.75+y_offset)
            megalabel.write_text(barcode.roc, char_height=2, char_width=2, line_width=8, orientation='R', justification='L')
            megalabel.endorigin()

            megalabel.reverse_print(active='N')

            megalabel.origin(0.50+x_offset,5.65+y_offset)
            megalabel.write_text(barcode.va, char_height=2, char_width=2, line_width=8, orientation='R', justification='L')
            megalabel.endorigin()

        if not hexaboard:
            megalabel.origin(0.25+x_offset,0.75+y_offset)
            megalabel.write_text(barcode.get_label_name(), char_height=2, char_width=2, line_width=8, orientation='R', justification='L')
    megalabel.endorigin()

    if tile:
        megalabel.origin(6.0+x_offset, 2.5+y_offset) #Changed x offset from 4.5 to 6 and y off set from 0.75 to 0.25
        megalabel.write_datamatrix(height=5, orientation='N', sq=200, aspect=1)
    else:
        megalabel.origin(2.75+x_offset, 0.75+y_offset)
        megalabel.write_datamatrix(height=3, orientation='N', sq=200, aspect=1)
    megalabel.write_text('{}'.format(barcode.full_serial))
    megalabel.endorigin()

    if tile:
#        megalabel.write_text("B{:04d} #{:01d}".format(int(barcode.batch),int(barcode.serial)), char_height=3, char_width=3, line_width=12.5, orientation='N', justification='R')
        if barcode.majorname == 'Wrapped Injection-Molded Tile':
            megalabel.origin(2.25+x_offset,2.5+y_offset) 
            megalabel.write_text("B#{:04d}".format(int(barcode.batch)), char_height=3, char_width=3, line_width=12.5, orientation='R', justification='L')
        else:
            megalabel.origin(1.75+x_offset, 5.5+y_offset)
            megalabel.write_text("{:04d}".format(int(barcode.batch)), char_height=3, char_width=3, line_width=12.5, orientation='R', justification='L')
        megalabel.endorigin()

        megalabel.origin(4+x_offset, 14.0+y_offset)
        megalabel.write_text("{}.{:03d}".format(str(barcode.mag), int(barcode.serial)), char_height=3, char_width=3, line_width=12.5, orientation='N', justification='R')
        megalabel.endorigin()

        megalabel.origin(3+x_offset, 14.0+y_offset)
        megalabel.write_text("{:02d}".format(int(barcode.size)), char_height=3, char_width=3, line_width=12.5, orientation='N', justification='L')
        megalabel.endorigin()

        if barcode.majorname == 'Wrapped Injection-Molded Tile':
            megalabel.origin(2.25+x_offset, 13.0+y_offset)
            megalabel.reverse_print()
            megalabel.draw_box(35, 35, thickness=30)
            megalabel.endorigin()
        else:
            megalabel.origin(2.25+x_offset, 13.0+y_offset)
            megalabel.draw_box(35, 35, thickness=1)
            megalabel.endorigin()
 
        megalabel.reverse_print(active='N')
    elif hexaboard:
        megalabel.reverse_print(active='N')
        megalabel.origin(0.25+x_offset, 7.00+y_offset)
        megalabel.write_text("{:05d}".format(int(barcode.serial)), char_height=2, char_width=2, line_width=8.50, orientation='N', justification='R')
    else:
        megalabel.origin(2.75+x_offset, 7.00+y_offset)
        megalabel.write_text("{:06d}".format(int(barcode.serial)), char_height=2, char_width=2, line_width=6.00, orientation='N', justification='R')
    megalabel.endorigin()
    
def add_to_megalabel_module(megalabel, barcode, x_offset=1.5875, y_offset=1.5875, borders=False):

    if borders:
        megalabel.origin(-0.125+x_offset,-0.125+y_offset)
        megalabel.draw_box(102, 89, thickness=1, color='B', rounding=2)
        megalabel.endorigin()

    megalabel.origin(0.50+x_offset,0.50+y_offset)
    megalabel.write_text("{} {} {}".format(barcode.major_code, barcode.sub_code, barcode.roc_version), char_height=2, char_width=2, line_width=12, orientation='N', justification='C')
    megalabel.endorigin()

    megalabel.origin(0.50+x_offset,2.50+y_offset)
    megalabel.write_text("{} {:04d}".format(barcode.mac_code, int(barcode.serial)), char_height=2, char_width=2, line_width=12, orientation='N', justification='C')
    megalabel.endorigin()

    megalabel.origin(0.75+x_offset, 4.5+y_offset)
    megalabel.write_datamatrix(height=3, orientation='N', sq=200, aspect=1)
    megalabel.write_text('{}'.format(barcode.full_serial))
    megalabel.endorigin()

    if "300" in barcode.thickness:
        megalabel.origin(7.5+x_offset, 5.00+y_offset)
        megalabel.reverse_print()
        megalabel.draw_box(35, 40, thickness=35)
        megalabel.endorigin()

    else:
        megalabel.origin(7.5+x_offset, 5.00+y_offset)
        megalabel.draw_box(35, 40, thickness=2)
        megalabel.endorigin()


    megalabel.origin(8.75+x_offset, 6.50+y_offset)
    megalabel.write_text("{}".format(barcode.roc_version), char_height=3, char_width=3, line_width=1, orientation='N', justification='C')
    megalabel.endorigin()
    
    if "300" in barcode.thickness:
        megalabel.reverse_print(active="N")

    #megalabel.origin(5.0+x_offset, 5.50+y_offset)
    #megalabel.write_text("ROC:{}".format(barcode.roc_version), char_height=2.5, char_width=2.5, line_width=8, orientation='N', justification='L')
    #megalabel.endorigin()

    #megalabel.origin(5.0+x_offset, 7.50+y_offset)
    #megalabel.write_text("{}".format(barcode.thickness), char_height=2.5, char_width=2.5, line_width=8, orientation='N', justification='L')
    #megalabel.endorigin()

    #megalabel.origin(4.5+x_offset, 11.5+y_offset) #Changed char height & width from 2.5 to 3 and line width from 10 to 12.5
    #megalabel.write_text("B{:04d} #{:01d}".format(int(barcode.batch),int(barcode.serial)), char_height=3, char_width=3, line_width=12.5, orientation='N', justification='R')
    #megalabel.endorigin()

def add_to_megalabel_tile(megalabel, barcode, x_offset=1.5875, y_offset=1.5875, tile=False, borders=False):

    if borders:
        megalabel.origin(-0.125+x_offset,-0.125+y_offset)
        megalabel.draw_box(153, 153, thickness=1, color='B', rounding=2)
        megalabel.endorigin()

    megalabel.origin(0.25+x_offset,1.75+y_offset)
    megalabel.write_text(barcode.get_label_name(), char_height=2, char_width=2, line_width=8, orientation='R', justification='L')
    megalabel.endorigin()

    megalabel.origin(2.75+x_offset, 1.75+y_offset)
    megalabel.write_datamatrix(height=3, orientation='N', sq=200, aspect=1)
    megalabel.write_text('{}'.format(barcode.full_serial))
    megalabel.endorigin()

    megalabel.origin(2.75+x_offset, 8.00+y_offset)
    if tile:
        megalabel.write_text("{:04d}:{:01d}".format(int(barcode.batch),int(barcode.serial)), char_height=2, char_width=2, line_width=6.00, orientation='N', justification='R')
    else:
        megalabel.write_text("{:06d}".format(int(barcode.serial)), char_height=2, char_width=2, line_width=6.00, orientation='N', justification='R')
    megalabel.endorigin()
    
def add_to_megalabel_wagon(megalabel, barcode, x_offset=2.0875, y_offset=1.5875, borders=False):

    if borders:
        megalabel.origin(-0.125+x_offset,-0.125+y_offset)
        megalabel.draw_box(400, 76, thickness=1, color='B', rounding=2)
        megalabel.endorigin()

    megalabel.origin(1.75+x_offset, 1.75+y_offset)
    megalabel.write_datamatrix(height=3, orientation='N', sq=200, aspect=1)
    megalabel.write_text('{}'.format(barcode.full_serial))
    megalabel.endorigin()

    megalabel.origin(9.6+x_offset, 1.1+y_offset)
    megalabel.write_text(barcode.code, char_height=2, char_width=2, line_width=7.75, orientation='B', justification='C')
    megalabel.endorigin()

    megalabel.origin(9.1+x_offset, 0.9+y_offset)
    megalabel.draw_box(20, 66, thickness=2, color='B', rounding=0)
    megalabel.endorigin()

    if "East" in barcode.majorname or "West" in barcode.majorname:
        title = "{} {}".format(barcode.majorname.split(" ")[:2][0], barcode.majorname.split(" ")[:2][1])
        sub = "{} [{}+{}]".format(barcode.majorname.split(" ")[2:3][0], barcode.subcode[0], barcode.subcode[1])
        nickname = barcode.nickname
    elif "Wagon" in barcode.majorname:
        title = barcode.majorname
        sub = "[{}+{}]".format(barcode.subcode[1], barcode.subcode[2])
        nickname = barcode.nickname
    elif "Twin" in barcode.nickname:
        title = barcode.nickname.split(" ")[0]
        nickname = "".join(barcode.nickname.split(" ")[2:])
        sub = barcode.nickname.split(" ")[1] 
    else:
        title = "Con Mezz"
        sub = barcode.nickname.replace(",", " ").split(" ")[1].replace("-", " ")
        try:
            nickname = barcode.nickname.split(",")[1][1:]
        except: 
            nickname = barcode.nickname.split(" ")[0]
    megalabel.origin(12+x_offset, 1.8+y_offset)
    megalabel.write_text(title, char_height=3, char_width=3, line_width=40, orientation='N', justification='L')
    megalabel.endorigin()

    megalabel.origin(12+x_offset, 5.6+y_offset)
    megalabel.write_text(sub, char_height=3, char_width=3, line_width=40, orientation='N', justification='L')
    megalabel.endorigin()

    megalabel.origin(27+x_offset, 0.5+y_offset)
    megalabel.draw_box(2, 68, thickness=1, color='B', rounding=0)
    megalabel.endorigin()

    megalabel.origin(28+x_offset, 1.8+y_offset)
    megalabel.write_text("\"{}\"".format(nickname), char_height=3, char_width=3, line_width=40, orientation='N', justification='L')
    megalabel.endorigin()

    megalabel.origin(28+x_offset, 5.6+y_offset)
    megalabel.write_text("S/N: {:06d}".format(int(barcode.serial)), char_height=3, char_width=3, line_width=40, orientation='N', justification='L')
    megalabel.endorigin()

    #print(megalabel.dumpZPL())
    #l.preview()

    #with open("{}/{}.zpl".format(barcode.get_nickname(), barcode.get_label_name()),'w') as f:
    #    f.write(l.dumpZPL())
    #f.close()
    #megalabel.preview()
   
def add_to_megalabel_flex(megalabel, barcode, x_offset=2.0875, y_offset=1.5875, borders=False):
    print("Inside add_to_megalabel_flex")
    if borders:
        megalabel.origin(-0.125+x_offset,-0.125+y_offset)
        megalabel.draw_box(203, 51, thickness=1, color='B', rounding=2)
        megalabel.endorigin()

    megalabel.origin(1.75+x_offset, 1+y_offset)
    megalabel.write_datamatrix(height=2.5, orientation='N', sq=200, aspect=1)
    megalabel.write_text('{}'.format(barcode.full_serial))
    megalabel.endorigin()

    megalabel.origin(7.5+x_offset, 1.2+y_offset)
    megalabel.write_text(barcode.subcode, char_height=2, char_width=2, line_width=10, orientation='N', justification='C')
    megalabel.endorigin()

    megalabel.origin(9.75+x_offset, 0.775+y_offset)
    megalabel.draw_box(45, 22, thickness=2, color='B', rounding=0)
    megalabel.endorigin()

#    megalabel.origin(13+x_offset, y_offset)
#    megalabel.draw_box(2, 50, thickness=1, color='B', rounding=0)
#    megalabel.endorigin()

#    megalabel.origin(28+x_offset, 1.8+y_offset)
#    megalabel.write_text("\"{}\"".format(nickname), char_height=3, char_width=3, line_width=40, orientation='N', justification='L')
#    megalabel.endorigin()

    megalabel.origin(7.5+x_offset, 3.7+y_offset)
    megalabel.write_text("S/N: {:06d}".format(int(barcode.serial)), char_height=2, char_width=2, line_width=40, orientation='N', justification='L')
    megalabel.endorigin()

    megalabel.origin(19.5+x_offset, 1+y_offset)
    megalabel.write_datamatrix(height=2.5, orientation='N', sq=200, aspect=1)
    megalabel.write_text('{}'.format(barcode.full_serial))
    megalabel.endorigin()

def produce_strips(barcodes, tile=False, hexaboard=False, preview=False, borders=False):

    if hexaboard:
        if not os.path.isdir(barcodes[0].get_label_name()[0]+barcodes[0].get_label_name()[1]+barcodes[0].get_label_name()[2]):
            os.makedirs(barcodes[0].get_label_name()[0]+barcodes[0].get_label_name()[1]+barcodes[0].get_label_name()[2])
    else:
        if not os.path.isdir(barcodes[0].get_label_name()):
            os.makedirs(barcodes[0].get_label_name())


    if tile:
        l = myLabel(44.75, 88.9, dpmm=8.0)

        left = 1.5875
        top = 2.0
        spacing = 22.225

        cols = 4
    else:
        l = myLabel(25.375, 88.9, dpmm=8.0)

        left = 2.175
        top = 3.175
        spacing = 12.7

        cols = 7

    rows = int(len(barcodes) / cols) + 1

    for y in range(0, rows):
        for x in range(0, cols):
            if y*cols + x == len(barcodes): break
            add_to_megalabel(l, barcodes[y*cols+x], x_offset=left+x*spacing, y_offset=top+y*spacing, tile=tile, hexaboard=hexaboard, borders=borders)

    zpl = l.dumpZPL()
    if preview: 
        l.preview()

    with open("label.zpl", 'w') as f:
        f.write(l.dumpZPL())
    f.close()

    return l, zpl
   
def produce_strips_module(barcodes, MAC="", preview=False, borders=False):

    if not os.path.isdir(barcodes[0].get_label_name()):
        os.makedirs(barcodes[0].get_label_name())

    l = myLabel(28.575, 79.375, dpmm=8.0)

    left = 1.5875
    top = 1.5875
    x_spacing = 15.875
    y_spacing = 14.2875

    cols = 5

    rows = int(len(barcodes) / cols) + 1

    for y in range(0, rows):
        for x in range(0, cols):
            if y*cols + x == len(barcodes): break
            add_to_megalabel_module(l, barcodes[y*cols+x], x_offset=left+x*x_spacing, y_offset=top+y*y_spacing, borders=borders)

    zpl = l.dumpZPL()
    if preview: 
        l.preview()

    with open("label.zpl", 'w') as f:
        f.write(l.dumpZPL())
    f.close()

    return l, zpl

def produce_strips_wagon(barcodes, preview=False, borders=False):

    if not os.path.isdir(barcodes[0].get_label_name()):
        os.makedirs(barcodes[0].get_label_name())

    l = myLabel(25.375, 53.975, dpmm=8.0)

    left = 1.5875
    top = 1.5875
    spacing = 12.7

    rows = 2 

    for y in range(0, rows):
        add_to_megalabel_wagon(l, barcodes[y], x_offset=left, y_offset=top+y*spacing, borders=borders)

    zpl = l.dumpZPL()
    if preview: 
        l.preview()

    with open("label.zpl", 'w') as f:
        f.write(l.dumpZPL())
    f.close()

    return l, zpl

def produce_strips_flex(barcodes, preview=False, borders=False):

    print("Inside produce_strips_flex")

    if not os.path.isdir(barcodes[0].get_label_name()):
        os.makedirs(barcodes[0].get_label_name())

    l = myLabel(19.375, 28.375, dpmm=8.0)

    left = 1.5875
    top = 1.5875
    spacing = 9.5

    rows = 2

#    print("ROWS", rows)
    for y in range(0, rows):
        add_to_megalabel_flex(l, barcodes[y], x_offset=left, y_offset=top+y*spacing, borders=borders)

    zpl = l.dumpZPL()
    if preview:
        l.preview()

    with open("label.zpl", 'w') as f:
        f.write(l.dumpZPL())
    f.close()

    return l, zpl

def load_barcodes(barcode_list, wagon=False, flex=False, tile=False, module=False, hexaboard=False, MAC="", ROC="", borders=False):

    print("Inside load_barcodes")

    zpl = ""

    all_barcodes = []

    if wagon:
        for i in range(0,len(barcode_list),2):
            barcodes = [Barcode(x) for x in barcode_list[i:i+2]]
            should_preview = i + 2 == len(barcode_list)
            l, temp_zpl = produce_strips_wagon(barcodes, preview=should_preview, borders=borders)

            all_barcodes += barcodes
            zpl = temp_zpl + "\n" + zpl
    elif flex:
        for i in range(0,len(barcode_list),2):
            barcodes = [Barcode(x) for x in barcode_list[i:i+2]]
            should_preview = i + 2 == len(barcode_list)
            l, temp_zpl = produce_strips_flex(barcodes, preview=should_preview, borders=borders)

            all_barcodes += barcodes
            zpl = temp_zpl + "\n" + zpl
    elif tile:
        for i in range(0,len(barcode_list),8): #Changed from 14 to 8
            barcodes = [Barcode(x, tile=tile) for x in barcode_list[i:i+8]] #Changed from 14 to 8
            print("i:", i)
            print("len:", len(barcode_list))
            should_preview = i + 8 == len(barcode_list)
            l, temp_zpl = produce_strips(barcodes, tile=True, preview=should_preview, borders=borders)

            all_barcodes += barcodes
            zpl = temp_zpl + "\n" + zpl
    elif module:
        for i in range(0,len(barcode_list),10):
            barcodes = [Barcode(x, module=True, MAC=MAC, ROC=ROC) for x in barcode_list[i:i+10]] 
            should_preview = i + 10 == len(barcode_list)
            l, temp_zpl = produce_strips_module(barcodes, preview=should_preview, borders=borders)

            all_barcodes += barcodes
            zpl = temp_zpl + "\n" + zpl
    elif hexaboard:
        for i in range(0,len(barcode_list),14):
            barcodes = [Barcode(x, hexaboard=True) for x in barcode_list[i:i+14]]
            should_preview = i + 14 == len(barcode_list)
            l, temp_zpl = produce_strips(barcodes, hexaboard=True, preview=should_preview, borders=borders)

            zpl = temp_zpl + "\n" + zpl
            all_barcodes += barcodes
    else:
        for i in range(0,len(barcode_list),14):
            barcodes = [Barcode(x) for x in barcode_list[i:i+14]]
            should_preview = i + 14 == len(barcode_list)
            l, temp_zpl = produce_strips(barcodes, preview=should_preview, borders=borders)

            zpl = temp_zpl + "\n" + zpl
            all_barcodes += barcodes


    return zpl, all_barcodes

### DEPRECIATED BELOW UNTIL MAIN ##########

    '''im = Image.open(name)
    im = ImageOps.contain(im, (54,54), method=Image.NEAREST)
    border = 22

    im = ImageOps.expand(im, border, 255)
    im = im.crop((0, 22, 76, 98))

    font1 = ImageFont.truetype("MotorolaScreentype.ttf", 16)

    if len(label) > 8:
        font2 = ImageFont.truetype("MotorolaScreentype.ttf", 16)
    elif len(label) > 6:
        font2 = ImageFont.truetype("MotorolaScreentype.ttf", 16)
    else:
        font2 = ImageFont.truetype("MotorolaScreentype.ttf", 16)

    ImageDraw.Draw(im).text((28, 50), payload[-5:], font=font1)
    im = im.rotate(90)
    ImageDraw.Draw(im).text((6, 50), label, font=font2)
    im = im.rotate(-90)
    #im = ImageOps.expand(im, 1, 230)
    im.save(name)

    return im
    '''
    
def main():
    parser = argparse.ArgumentParser(description="Make data matrix labels for HGCAL electronics")
    parser.add_argument("-m", "--majortype", action="store", type=str, dest="majortype", default="Test", help="Major type name for component (e.g. Engine, Wagon, Concentrator Mezzanine). See documentation for full list of major types")
    parser.add_argument("-p", "--production", action="store_true", dest="production", default=False, help="Add flag if component is final production")
    parser.add_argument("-s", "--subtype", action="store", type=str, dest="subtype", default=None, help="Version specification for prototypes (e.g. V1, V2, V2b)")
    parser.add_argument("-a", "--adapter", action = "store", type=str, dest="adapter", default=None, help="Name of adapter (if applicable)")
    parser.add_argument("-t", "--tester", action = "store", type=str, dest="tester", default=None, help="Name of tester (if applicable)")
    parser.add_argument("-x", "--hexaboard", action = "store", type=int, dest="hexaboard", default=None, help="Specify the whether partial or full production or prototype  (Full prototype = 0, partial prototype = 1, partial production = 2, full production = 3, if applicable)")
    parser.add_argument("-v", "--vendor", action = "store", type=str, dest="vendor", default=None, help="Specify the vendor for hexaboard (P or E, if applicable)")
    parser.add_argument("-w", "--wagon", action = "store", type=str, dest="wagon", default=None, help="Specify west or east wagon subtype (W or E)")
    parser.add_argument("-n", "--number", action = "store", type=int, dest="n", default=1, help="Number of labels to make with given specifications")
    parser.add_argument("--serial", action="store", type=int, dest="serial", default=0, help="Specify serial number at which to start")
    args = parser.parse_args()

    types = {
                "ldhexaboard"               :   6,
                "hdhexaboard"               :   7,
                "ldengine"                  :   10,
                "ldwagon"                   :   12,
                "concentratormezzanine"     :   14,
                "boardtester"               :   50,
                "adapter"                   :   51,
                "test"                      :   99,
            } 

    wagons = {
                "w"  :   1,
                "e"  :   2,
             }

    adapters = {
                    "interposer"    :   1,
                    "wagonwest"     :   11,
                    "wagoneast"     :   12,
                    "fmctoengine"   :   21,
               }

    testers = {
                "tileboardtester"       :   1,
                "tileboardtesterv2"     :   2, 
                "hexacontroller"        :   11, 
              }

    subtypes = {
                "v1"    :   0,
                "v2"    :   1,
                "v2b"   :   2,
                "v3"    :   3,
               }

    labels = {  
                "060001":  "LD HB1 P",
                "060002":  "LD HB1 E",
                "100000":  "EngV1",
                "100001":  "EngV2",
                "100002":  "EngV2b",
                "100300":  "EngV3",
                "100100":  "Eng",
                "110002":  "WagV2-E",
                "110003":  "WagV2-W",
                "123101":  "Wag3W01",
                "123201":  "Wag3E01",
                "500001":  "TBT",
                "500002":  "TBT2",
                "500011":  "HXCTR",
                "510001":  "IntrPos",
                "510011":  "WagW-TBT",
                "510012":  "WagE-TBT",
                "510021":  "FMC-EngV2",
                "990001":  "Test"
             }

    majortype = types[args.majortype.lower()]

    if majortype == 6 and (args.vendor == None or args.hexaboard == None):
        print("Specify both a vendor and production type for hexaboard")
        return
    elif majortype == 11 and args.wagon == None:
        print("Specify whether is is an east or west wagon, use -w with W or E")
    elif majortype == 50 and args.tester == None:
        print("No tester type specified, use -t with name of tester")
        return
    elif majortype == 51 and args.adapter == None:
        print("No adapter type specified, use -a with name of adapter")
        return
    elif majortype == 6:
        if args.vendor.lower() == "p":
            vendor = 1
        elif args.vendor.lower() == "e":
            vendor = 2
        else:
            print("Please specify the correct vendor indicator")
            return
        sub = args.hexaboard * 100 + vendor
    elif majortype == 10:
        subtype = subtypes[args.subtype]
        sub = 100 * subtype
    elif majortype == 12:
        we = 100 * wagons[args.wagon.lower()]
        vers = 1000 * subtypes[args.subtype.lower()]
        sub = vers + we + 1
        print(sub)
    elif majortype == 50:
        sub = testers[args.tester.lower()]
    elif majortype == 51:
        sub = adapters[args.adapter.lower()]
    else:
        sub = None


    production = 1 if args.production else 0
    if production == 1 and args.version != None:
        print("Subtype not needed for production components")
        subtype = "0"
    elif majortype != 50 and majortype != 51 and majortype != 6 and majortype != 11:
        subtype = subtypes[args.subtype.lower()]
       
 
    names = []
    images = []
    #Do fancy database checking here to not double use serial numbers
    barcodes = []

    for i in range(1,args.n + 1):
        serial = args.serial + i

        if sub == None:
            payload = "3205{0:02d}{1:02d}{2:02d}{4:05d}".format(majortype, production, subtype, 0, serial)
        else:
            payload = "3205{0:02d}{1:04d}{2:05d}".format(majortype, sub, serial)
        
        label = labels[str(payload[4:10])] 
        print("Making barcode for {}  with value: {}".format(label, payload))

        barcode = Barcode(payload)

        l = produce_barcode(barcode)

        barcodes.append(barcode)

    if len(barcodes) > 1:
        produce_strips(barcodes)

        '''
        width, height = images[0].size

        rows = []

        new_image = Image.new("L", (args.n * (width + 25), height + 25))
        i_row = 0
        j = 0
        for i in range(args.n):
            if i % 2 == 0:
                new_image.paste(images[i], ((width + 13) * i, 13))
            else:
                new_image.paste(images[i], ((width + 12) * i, 13))
            
            if (i + 1) % 7 == 0:
                j += 1
                new_image.save("{0}/{0}{1}.png".format(label, j))
                rows.append(new_image)
                new_image = Image.new("L", (args.n * (width + 13), height + 25))

        if (i + 1) % 7 != 0:
            j += 1
            new_image.save("{0}/{0}{1}.png".format(label,j))
            rows.append(new_image)
    
        if j > 1:
            height = sum([r.height for r in rows])
            print(rows[0].width, rows[0].height)
            new_image = Image.new("L", (rows[0].width, height))
            
            for i,r in enumerate(rows):
                new_image.paste(r, (0, i*(height + 26)))
        
            new_image.save("{0}/{0}.png".format(label, label))

        '''

if __name__ == "__main__":
    main()
