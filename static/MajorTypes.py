sub_ldengine = {}
sub_hdengine = {}
sub_ldwagoneast = {
    "East 1A":      {"sub_sn": "10A1"},
    "East 2A":      {"sub_sn": "20A1"},
    "East 2B":      {"sub_sn": "20B1"},
    "East 3A":      {"sub_sn": "30A1"},
    "East T":       {"sub_sn": "30A3"},
}
sub_ldwagonwest = {
    "West 1A":      {"sub_sn": "10A1"},
    "West 2A":      {"sub_sn": "20A1"},
    "West 3A":      {"sub_sn": "30A1"},
    "West T":       {"sub_sn": "30A3"},
    "Lefty Python": {"sub_sn": "30A2"}
}
sub_hdwagon = {}
sub_econ = {}
sub_dcdc = {}
sub_zipper = {}

majortypes = {
    '':                         {"major_sn": 0, "subtypes": {"sub_sn": "None"}},
    "LD Engine":                {"major_sn": 10, "subtypes": sub_ldengine},
    "HD Engine":                {"major_sn": 11, "subtypes": sub_hdengine},
    "LD Wagon East":            {"major_sn": 12, "subtypes": sub_ldwagoneast},
    "LD Wagon West":            {"major_sn": 13, "subtypes": sub_ldwagonwest},
    "HD Wagon":                 {"major_sn": 14, "subtypes": sub_hdwagon},
    "Concentrator Mezzanine":   {"major_sn": 15, "subtypes": sub_econ},
    "DCDC Board":               {"major_sn": 16, "subtypes": sub_dcdc},
    "Zipper Board":             {"major_sn": 17, "subtypes": sub_zipper}
}    

def get_majortypes():
    return majortypes

def get_subtypes(key):
    return majortypes[key]["subtypes"] 
