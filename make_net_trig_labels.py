#!/usr/bin/python3

from zpl import Label
import os
import argparse


class myLabel(Label):
    
    def __init__(self, height=25.4, width=88.9, dpmm=8.0):
        super().__init__(height, width, dpmm)

    def write_datamatrix(self, height=1, orientation='N', sq=200, aspect=1):

        self.code += ("^BX{},{},{},,,,,{}").format(orientation, height, sq, aspect)

def make_net():
    l = myLabel(9.525, 9.525, dpmm=8.0)

    l.origin(0.25, 3.75)
    l.write_text("NET", char_height=3, char_width=3, line_width=9.525, orientation='N', justification='C')
    l.endorigin()
    
    print(l.dumpZPL())

    with open("NET.zpl",'w') as f:
        f.write(l.dumpZPL())
    f.close()

    return l

def make_trig():

    l = myLabel(9.525, 9.525, dpmm=8.0)

    l.origin(0.25, 3.75)
    l.write_text("TRIG", char_height=3, char_width=3, line_width=9.525, orientation='N', justification='C')
    l.endorigin()
    
    print(l.dumpZPL())

    with open("TRIG.zpl",'w') as f:
        f.write(l.dumpZPL())
    f.close()

    return l

def add_to_megalabel(megalabel, word, x_offset=1.5875, y_offset=1.5875):

    megalabel.origin(0.25+x_offset,3.75+y_offset)
    megalabel.write_text(word, char_height=3, char_width=3, line_width=9.525, orientation='N', justification='C')
    megalabel.endorigin()

def produce_strips():

    l = myLabel(25.4, 88.9, dpmm=8.0)

    left = 2.175
    top = 3.175
    spacing = 12.7

    for y in range(0, 6):
        for x in range(0, 7):
            if y < 3:
                word = "NET"
            else:
                word = "TRIG"
            add_to_megalabel(l, word, x_offset=left+x*spacing, y_offset=top+y%2*spacing)

        if y % 2 == 1:
            l.preview()
            print(l.dumpZPL())
            l = myLabel(25.4, 88.9, dpmm=8.0)
            
            

    with open("label.zpl", 'w') as f:
        f.write(l.dumpZPL())
    f.close()

    return l
    
def main():
    net = make_net()
    trig = make_trig()

    produce_strips()
    

if __name__ == "__main__":
    main()
