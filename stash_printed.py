import json
import os

class Stasher:

    def __init__(self, barcode_info, cache_path="./static/printed_barcodes.json"):

        self.cache_path = cache_path
        self.barcode_info = barcode_info        

        self.reader = self.open_read(cache_path)

    def stash(self, serial):

        reader = self.open_read(self.cache_path)
        temp_dict = json.load(reader)
        reader.close()

        write = self.open(self.cache_path)

        sn_dict = {}
        sn_dict[serial] = serial

        temp_dict.update(sn_dict)

        json.dump(temp_dict, write)
        write.close()
       
        print("Stashed printed labels in {}".format(self.cache_path))

    def load(self):
        
        cache = json.load(self.reader)

        return cache

    def open_read(self, cache_path="./static/printed_barcodes.json"):
        
        return open(cache_path, 'r')

    def open(self, cache_path="./static/printed_barcodes.json"):
        
        if os.path.isfile(cache_path):

            os.system("cp {}.backup {}".format(cache_path, cache_path))
            
            return open(cache_path, 'w')

        elif os.path.isfile(cache_path + ".backup"):

            os.system("cp {}.backup {}".format(cache_path, cache_path))

            return open(cache_path, 'a')

        else:
            return open(cache_path, 'w')

    def backup(self, cache_path="./static/printed_barcodes.json"):

        print("Backing up list of printed barcodes...")

        os.system("cp {} {}.backup".format(cache_path, cache_path))
        
    def search(self):
        cache = self.load()

        overlap = False
        serials = []       
 
        for b in self.barcode_info:
            if b.full_serial not in cache:
                self.stash(b.full_serial)
                serial = ""
            else:
                overlap = True 
                serials.append(b.full_serial)

        return overlap, serials
                
if __name__ == "__main__":
    s = Stasher(cache_path="./static/printed_barcodes.json")

    s.backup()


