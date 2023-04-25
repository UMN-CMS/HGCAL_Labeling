'''
 For additions in the future
 ---------------------------
 Format of major type:
    'Major Type Full Name': {
        "major_sn": <major type serial number (2)>, 
        "major_code": <Letters representing major type>,
        "subtypes": <subtype dictionary>
    }

 Format for subtypes:
    "Nickname on Label": {
        "sub_sn":   <subtype serial number>,
        "sub_code": <same as above (placeholder if we can't use letters)>,
    }

'''

sub_ldhexaboard = {
    "XLFL01":         {"sub_sn": "1001", "sub_code": "1001"},
    "XLFL02":         {"sub_sn": "1002", "sub_code": "1002"},
    "XLFL03":         {"sub_sn": "1003", "sub_code": "1003"},
    "XLSL03":         {"sub_sn": "2103", "sub_code": "2103"},
    "XLSR03":         {"sub_sn": "2203", "sub_code": "2203"},
}
sub_ldengine = {
    "EngV1":        {"sub_sn": "0000", "sub_code": "0000"},
    "EngV2":        {"sub_sn": "0100", "sub_code": "0100"},
    "EngV2b":       {"sub_sn": "0200", "sub_code": "0200"},
    "EngV3":        {"sub_sn": "0300", "sub_code": "0300"},
    "EngV3L":       {"sub_sn": "0310", "sub_code": "0310"},
    "EngDmy":       {"sub_sn": "0310", "sub_code": "0900"}
}
sub_hdengine = {
    "HDEV3":        {"sub_sn": "0300", "sub_code": "0300"}
}
sub_ldwagoneast = {
    "East 1A":      {"sub_sn": "10A1", "sub_code": "10A1"},
    "East 2A":      {"sub_sn": "20A1", "sub_code": "20A1"},
    "East 2B":      {"sub_sn": "20B1", "sub_code": "20B1"},
    "East 3A":      {"sub_sn": "30A1", "sub_code": "30A1"},
    "East T":       {"sub_sn": "30A3", "sub_code": "30A3"},
    "East 1 Debug": {"sub_sn": "10Z1", "sub_code": "10Z1"}
}
sub_ldwagonwest = {
    "West 1A":      {"sub_sn": "10A1", "sub_code": "10A1"},
    "West 2A":      {"sub_sn": "20A1", "sub_code": "20A1"},
    "West 3A":      {"sub_sn": "30A1", "sub_code": "30A1"},
    "Lefty Python": {"sub_sn": "30A2", "sub_code": "30A2"},
    "West T":       {"sub_sn": "30A3", "sub_code": "30A3"},
    "West 1 Debug": {"sub_sn": "10Z1", "sub_code": "10Z1"}
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
sub_econ = {
    "CM Full, ECON-T COB":  {"sub_sn": "1F11", "sub_code": "1F11"},
    "CM Full, ECON-T":      {"sub_sn": "1F12", "sub_code": "1F12"},
    "CM Full, ECON-T+D":    {"sub_sn": "1F20", "sub_code": "1F20"},
    "CM Full, Dummy":       {"sub_sn": "1F90", "sub_code": "1F90"}
}
sub_dcdc = {
    "TST1":         {"sub_sn": "9001", "sub_code": "9001"}
}
sub_zipper = {
    "Standard":     {"sub_sn": "1000", "sub_code": "1000"},
    "LPGBT":        {"sub_sn": "2000", "sub_code": "2000"}
}
sub_tester = {
    "TBT":          {"sub_sn": "0001", "sub_code": "0001"},
    "TBT2":         {"sub_sn": "0002", "sub_code": "0002"},
    "HXCTR":        {"sub_sn": "0011", "sub_code": "0011"},
    "ZCU102":       {"sub_sn": "0021", "sub_code": "0021"},
    "WagT":         {"sub_sn": "0031", "sub_code": "0031"},
    "WagWhl":       {"sub_sn": "0032", "sub_code": "0032"},
    "WagAdE":       {"sub_sn": "0033", "sub_code": "0033"},
    "WagAdW":       {"sub_sn": "0034", "sub_code": "0034"},
    "EngTE":        {"sub_sn": "0041", "sub_code": "0041"},
    "EngTW":        {"sub_sn": "0042", "sub_code": "0042"}
}

majortypes = {
    '':                         {"major_sn": 0, "major_code": "","subtypes": {"sub_sn": "None"}},
    'LD Hexaboard':             {"major_sn": 3, "major_code": "XL","subtypes": sub_ldhexaboard},
    "LD Engine":                {"major_sn": 10, "major_code": "EL", "subtypes": sub_ldengine},
    "HD Engine":                {"major_sn": 11, "major_code": "EH", "subtypes": sub_hdengine},
    "LD Wagon East":            {"major_sn": 12, "major_code": "WE", "subtypes": sub_ldwagoneast},
    "LD Wagon West":            {"major_sn": 13, "major_code": "WW", "subtypes": sub_ldwagonwest},
    "HD Wagon":                 {"major_sn": 14, "major_code": "WH", "subtypes": sub_hdwagon},
    "Concentrator Mezzanine":   {"major_sn": 15, "major_code": "CM", "subtypes": sub_econ},
    "DCDC Board":               {"major_sn": 16, "major_code": "DC", "subtypes": sub_dcdc},
    "Zipper Board":             {"major_sn": 17, "major_code": "ZP", "subtypes": sub_zipper},
    'Tester':                   {"major_sn": 90, "major_code": "TS","subtypes": sub_tester}
}    

def get_majortypes():
    return majortypes

def get_subtypes(key):
    return majortypes[key]["subtypes"] 
