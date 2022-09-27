sub_ldengine = {
    "V1":         {"sub_sn": "0000", "sub_code": "0000"},
    "V2":         {"sub_sn": "0100", "sub_code": "0100"},
    "V2b":        {"sub_sn": "0200", "sub_code": "0200"},
    "V3":         {"sub_sn": "0300", "sub_code": "0300"}
}
sub_hdengine = {}
sub_ldwagoneast = {
    "East 1A":      {"sub_sn": "10A1", "sub_code": "10A1"},
    "East 2A":      {"sub_sn": "20A1", "sub_code": "20A1"},
    "East 2B":      {"sub_sn": "20B1", "sub_code": "20B1"},
    "East 3A":      {"sub_sn": "30A1", "sub_code": "30A1"},
    "East T":       {"sub_sn": "30A3", "sub_code": "30A3"}
}
sub_ldwagonwest = {
    "West 1A":      {"sub_sn": "10A1", "sub_code": "10A1"},
    "West 2A":      {"sub_sn": "20A1", "sub_code": "20A1"},
    "West 3A":      {"sub_sn": "30A1", "sub_code": "30A1"},
    "Lefty Python": {"sub_sn": "30A2", "sub_code": "30A2"},
    "West T":       {"sub_sn": "30A3", "sub_code": "30A3"}
}
sub_hdwagon = {}
sub_econ = {}
sub_dcdc = {}
sub_zipper = {}

majortypes = {
    '':                         {"major_sn": 0, "major_code": "","subtypes": {"sub_sn": "None"}},
    "LD Engine":                {"major_sn": 10, "major_code": "EL", "subtypes": sub_ldengine},
    "HD Engine":                {"major_sn": 11, "major_code": "EH", "subtypes": sub_hdengine},
    "LD Wagon East":            {"major_sn": 12, "major_code": "WE", "subtypes": sub_ldwagoneast},
    "LD Wagon West":            {"major_sn": 13, "major_code": "WW", "subtypes": sub_ldwagonwest},
    "HD Wagon":                 {"major_sn": 14, "major_code": "WH", "subtypes": sub_hdwagon},
    "Concentrator Mezzanine":   {"major_sn": 15, "major_code": "CM", "subtypes": sub_econ},
    "DCDC Board":               {"major_sn": 16, "major_code": "DC", "subtypes": sub_dcdc},
    "Zipper Board":             {"major_sn": 17, "major_code": "ZP", "subtypes": sub_zipper}
}    

def get_majortypes():
    return majortypes

def get_subtypes(key):
    return majortypes[key]["subtypes"] 
