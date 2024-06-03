import requests
import json
from static.MajorTypes import majortypes

def update_tables():
    #first makes sure that the Major Type, Sub Type, and Major Sub Stitch tables are up to date
    r = requests.post('http://cmslab3.spa.umn.edu/~cros0400/public_html/cgi-bin/LabelDB/update_metatables.py', data={'majortypes': majortypes})

def upload_label(labels_json):
    # could do this multiple different ways, one is to pass the function some json with all the labels to be sent to the database
    # a different way would be to get rid of the for loop and just pass this function the individual labels
    label_dict = json.load(labels_json)

    for label in label_dict:
        r = requests.post('http://cmslab3.spa.umn.edu/~cros0400/public_html/cgi-bin/LabelDB/add_label.py', data={'label': label})

        # this gets the printed statements
        lines = r.text.split('\n')

        begin = lines.index("Begin") + 1
        end = lines.index("End")

        for i in range(begin, end):
            # right now this just prints out the line that was entered into the database
            # this could be switched out for a return function or could append to an array that is then returned at the end

            # lines come out in this format:
            # label, str(type_sn), type_code, sn, str(major_type_id), str(sub_type_id)
            print(lines[i])
