#!/usr/bin/python3

from zpl import Label
import os
import argparse
from PIL import Image
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
import io

class myLabel(Label):
    
    def __init__(self, height=25.4, width=88.9, dpmm=8.0):
        super().__init__(height, width, dpmm)

    def write_datamatrix(self, height=1, orientation='N', sq=200, aspect=1):

        self.code += ("^BX{},{},{},,,,,{}").format(orientation, height, sq, aspect)

    def preiew(self, index=0, outfile="tmp.png"):
        try:
            url = 'http://api.labelary.com/v1/printers/%idpmm/labels/%fx%f/%i/' % (
                self.dpmm, self.width/25.4, self.height/25.4, index)
            res = urlopen(url, self.dumpZPL().encode()).read()
            im = Image.open(io.BytesIO(res)).show()
            im.save(outfile)
        except IOError:
            raise Exception("Invalid preview received, mostlikely bad ZPL2 code uploaded.")

class Barcode:
    
    def __init__(self, payload):
        self.serial = payload[-5:]
        self.subtype = payload[4:-5]
        self.first = payload[:4]

        self.full_serial = payload

        self.get_nickname()

    
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
        return self.get_nickname() + self.serial


def produce_barcode(barcode, x_offset=0, y_offset=0):

    l = myLabel(9.525, 9.525, dpmm=8.0)

    l.origin(0.25,0.75)
    l.write_text(barcode.get_nickname(), char_height=2, char_width=2, line_width=8, orientation='R', justification='L')
    l.endorigin()

    l.origin(2.75, 0.75)
    l.write_datamatrix(height=3, orientation='N', sq=200, aspect=1)
    l.write_text('{}'.format(barcode.full_serial))
    l.endorigin()

    l.origin(2.75, 6.25)
    l.write_text(barcode.serial, char_height=2, char_width=2, line_width=5.25, orientation='N', justification='R')
    l.endorigin()
    
    print(l.dumpZPL())
    #l.preview()

    with open("{}/{}.zpl".format(barcode.get_nickname(), barcode.get_label_name()),'w') as f:
        f.write(l.dumpZPL())
    f.close()
    l.preview()

    return l

def add_to_megalabel(megalabel, barcode, x_offset=1.5875, y_offset=1.5875):

    megalabel.origin(0.25+x_offset,0.75+y_offset)
    megalabel.write_text(barcode.get_nickname(), char_height=2, char_width=2, line_width=8, orientation='R', justification='L')
    megalabel.endorigin()

    megalabel.origin(2.75+x_offset, 0.75+y_offset)
    megalabel.write_datamatrix(height=3, orientation='N', sq=200, aspect=1)
    megalabel.write_text('{}'.format(barcode.full_serial))
    megalabel.endorigin()

    megalabel.origin(2.75+x_offset, 6.25+y_offset)
    megalabel.write_text(barcode.serial, char_height=2, char_width=2, line_width=5.25, orientation='N', justification='R')
    megalabel.endorigin()
    

def produce_strips(barcodes):

    if not os.path.isdir(barcodes[0].get_nickname()):
        os.makedirs(barcodes[0].get_nickname())

    l = myLabel(25.4, 88.9, dpmm=8.0)

    left = 2.175
    top = 3.175
    spacing = 12.7

    for y in range(0, 2):
        for x in range(0, 7):
            add_to_megalabel(l, barcodes[y*7+x], x_offset=left+x*spacing, y_offset=top+y*spacing)

    print(l.dumpZPL())
    l.preview()

    with open("label.zpl", 'w') as f:
        f.write(l.dumpZPL())
    f.close()

    return l
    
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
