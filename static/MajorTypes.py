sub_ldengine = {
    "V1":           {"sub_sn": "0000", "sub_code": "0000"},
    "V2":           {"sub_sn": "0100", "sub_code": "0100"},
    "V2b":          {"sub_sn": "0200", "sub_code": "0200"},
    "V3":           {"sub_sn": "0300", "sub_code": "0300"},
    "V3L":          {"sub_sn": "0310", "sub_code": "0310"}
}
sub_hdengine = {
    "HDEV3":        {"sub_sn": "0300", "sub_code": "0300"}
}
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
sub_hdwagon = {
    "Prototype":        {"sub_sn": "020A", "sub_code": "020A"},
    "Straight 3":       {"sub_sn": "130A", "sub_code": "130A"},
    "Triangle 3":       {"sub_sn": "130B", "sub_code": "130B"},
    "Straight 3 Small": {"sub_sn": "130C", "sub_code": "130C"},
    "Straight 3.5":     {"sub_sn": "131A", "sub_code": "131A"},
    "L-Shaped 3.5":     {"sub_sn": "131B", "sub_code": "131B"},
    "Straight 2":       {"sub_sn": "120A", "sub_code": "120A"},
    "Straight 2.5":     {"sub_sn": "121A", "sub_code": "121A"},
}
sub_econ = {}
sub_dcdc = {
    "Test":         {"sub_sn": "9001", "sub_code": "TST1"}
}
sub_zipper = {
    "Standard":     {"sub_sn": "1000", "sub_code": "1000"},
    "LPGBT":        {"sub_sn": "2000", "sub_code": "2000"}
}

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
