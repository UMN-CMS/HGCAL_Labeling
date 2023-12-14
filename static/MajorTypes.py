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

sub_ldmodule = {
    "Full, 300 um, CuW baseplate":         {"sub_sn": "031", "sub_code": "F3W"},
    "Full, 300 um, PCB baseplate":         {"sub_sn": "032", "sub_code": "F3P"},
    "Full, 300 um, Carbon Fiber baseplate":         {"sub_sn": "032", "sub_code": "F3C"},
    "Full, 200 um, CuW baseplate":         {"sub_sn": "021", "sub_code": "F2W"},
    "Full, 200 um, PCB baseplate":         {"sub_sn": "022", "sub_code": "F2P"},
    "Full, 200 um, Carbon Fiber baseplate":         {"sub_sn": "022", "sub_code": "F2C"},
    "Right, 300 um, CuW baseplate":         {"sub_sn": "031", "sub_code": "R3W"},
    "Right, 300 um, PCB baseplate":         {"sub_sn": "032", "sub_code": "R3P"},
    "Right, 300 um, Carbon Fiber baseplate":         {"sub_sn": "032", "sub_code": "R3C"},
    "Right, 200 um, CuW baseplate":         {"sub_sn": "021", "sub_code": "R2W"},
    "Right, 200 um, PCB baseplate":         {"sub_sn": "022", "sub_code": "R2P"},
    "Right, 200 um, Carbon Fiber baseplate":         {"sub_sn": "022", "sub_code": "R2C"},
    "Top, 300 um, CuW baseplate":         {"sub_sn": "031", "sub_code": "T3W"},
    "Top, 300 um, PCB baseplate":         {"sub_sn": "032", "sub_code": "T3P"},
    "Top, 300 um, Carbon Fiber baseplate":         {"sub_sn": "032", "sub_code": "T3C"},
    "Top, 200 um, CuW baseplate":         {"sub_sn": "021", "sub_code": "T2W"},
    "Top, 200 um, PCB baseplate":         {"sub_sn": "022", "sub_code": "T2P"},
    "Top, 200 um, Carbon Fiber baseplate":         {"sub_sn": "022", "sub_code": "T2C"},
    "Left, 300 um, CuW baseplate":         {"sub_sn": "031", "sub_code": "L3W"},
    "Left, 300 um, PCB baseplate":         {"sub_sn": "032", "sub_code": "L3P"},
    "Left, 300 um, Carbon Fiber baseplate":         {"sub_sn": "032", "sub_code": "L3C"},
    "Left, 200 um, CuW baseplate":         {"sub_sn": "021", "sub_code": "L2W"},
    "Left, 200 um, PCB baseplate":         {"sub_sn": "022", "sub_code": "L2P"},
    "Left, 200 um, Carbon Fiber baseplate":         {"sub_sn": "022", "sub_code": "L2C"},
    "Five, 300 um, CuW baseplate":         {"sub_sn": "031", "sub_code": "53W"},
    "Five, 300 um, PCB baseplate":         {"sub_sn": "032", "sub_code": "53P"},
    "Five, 300 um, Carbon Fiber baseplate":         {"sub_sn": "032", "sub_code": "53C"},
    "Five, 200 um, CuW baseplate":         {"sub_sn": "021", "sub_code": "52W"},
    "Five, 200 um, PCB baseplate":         {"sub_sn": "022", "sub_code": "52P"},
    "Five, 200 um, Carbon Fiber baseplate":         {"sub_sn": "022", "sub_code": "52C"},
}

sub_hdmodule = {
    "Full, 200 um, CuW baseplate":         {"sub_sn": "021", "sub_code": "F2W"},
    "Full, 200 um, PCB baseplate":         {"sub_sn": "022", "sub_code": "F2P"},
    "Full, 200 um, Carbon Fiber baseplate":         {"sub_sn": "022", "sub_code": "F2C"},
    "Full, 120 um, CuW baseplate":         {"sub_sn": "011", "sub_code": "F1W"},
    "Full, 120 um, PCB baseplate":         {"sub_sn": "012", "sub_code": "F1P"},
    "Full, 120 um, Carbon Fiber baseplate":         {"sub_sn": "012", "sub_code": "F1C"},
    "Right, 200 um, CuW baseplate":         {"sub_sn": "021", "sub_code": "R2W"},
    "Right, 200 um, PCB baseplate":         {"sub_sn": "022", "sub_code": "R2P"},
    "Right, 200 um, Carbon Fiber baseplate":         {"sub_sn": "022", "sub_code": "R2C"},
    "Right, 120 um, CuW baseplate":         {"sub_sn": "011", "sub_code": "R1W"},
    "Right, 120 um, PCB baseplate":         {"sub_sn": "012", "sub_code": "R1P"},
    "Right, 120 um, Carbon Fiber baseplate":         {"sub_sn": "012", "sub_code": "R1C"},
    "Top, 200 um, CuW baseplate":         {"sub_sn": "021", "sub_code": "T2W"},
    "Top, 200 um, PCB baseplate":         {"sub_sn": "022", "sub_code": "T2P"},
    "Top, 200 um, Carbon Fiber baseplate":         {"sub_sn": "022", "sub_code": "T2C"},
    "Top, 120 um, CuW baseplate":         {"sub_sn": "011", "sub_code": "T1W"},
    "Top, 120 um, PCB baseplate":         {"sub_sn": "012", "sub_code": "T1P"},
    "Top, 120 um, Carbon Fiber baseplate":         {"sub_sn": "012", "sub_code": "T1C"},
    "Left, 200 um, CuW baseplate":         {"sub_sn": "021", "sub_code": "L2W"},
    "Left, 200 um, PCB baseplate":         {"sub_sn": "022", "sub_code": "L2P"},
    "Left, 200 um, Carbon Fiber baseplate":         {"sub_sn": "022", "sub_code": "L2C"},
    "Left, 120 um, CuW baseplate":         {"sub_sn": "011", "sub_code": "L1W"},
    "Left, 120 um, PCB baseplate":         {"sub_sn": "012", "sub_code": "L1P"},
    "Left, 120 um, Carbon Fiber baseplate":         {"sub_sn": "012", "sub_code": "L1C"},
    "Five, 200 um, CuW baseplate":         {"sub_sn": "021", "sub_code": "52W"},
    "Five, 200 um, PCB baseplate":         {"sub_sn": "022", "sub_code": "52P"},
    "Five, 200 um, Carbon Fiber baseplate":         {"sub_sn": "022", "sub_code": "52C"},
    "Five, 120 um, CuW baseplate":         {"sub_sn": "011", "sub_code": "51W"},
    "Five, 120 um, PCB baseplate":         {"sub_sn": "012", "sub_code": "51P"},
    "Five, 120 um, Carbon Fiber baseplate":         {"sub_sn": "012", "sub_code": "51C"},
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
    "HDEF3":        {"sub_sn": "0300", "sub_code": "03F0"}
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

sub_tile_2 = {
        "":     {"sub_sn": "", "sub_code": ""},
}

sub_tile_4 = {
        "TPBC":       {"sub_sn": "{}{}{}{}", "sub_code": "{}{}{}{}"},
        "TPBCNO":     {"sub_sn": "{}{}{}{}", "sub_code": "{}{}{}{}"},
        "Twin-Ax Cable Type A":       {"sub_sn": "1112", "sub_code": "TXA2"},
        "Twin-Ax Cable Type B":       {"sub_sn": "1122", "sub_code": "TXB2"},
        "Twin-Ax Cable Type C":       {"sub_sn": "1132", "sub_code": "TXC2"},
        "Twin-Ax Cable Type D":       {"sub_sn": "1142", "sub_code": "TXD2"},
}

majortypes = {
    '':                              {"major_sn": 0, "major_code": "","subtypes": {"sub_sn": "None"}},
    'LD Hexaboard':                  {"major_sn": 3, "major_code": "XL","subtypes": sub_ldhexaboard},
    'LD Module':                     {"major_sn": 8,  "major_code": "ML","subtypes": sub_ldmodule},
    'HD Module':                     {"major_sn": 8,  "major_code": "MH","subtypes": sub_hdmodule},
    "LD Engine":                     {"major_sn": 10, "major_code": "EL", "subtypes": sub_ldengine},
    "HD Engine":                     {"major_sn": 11, "major_code": "EH", "subtypes": sub_hdengine},
    "LD Wagon East":                 {"major_sn": 12, "major_code": "WE", "subtypes": sub_ldwagoneast},
    "LD Wagon West":                 {"major_sn": 13, "major_code": "WW", "subtypes": sub_ldwagonwest},
    "HD Wagon":                      {"major_sn": 14, "major_code": "WH", "subtypes": sub_hdwagon},
    "Concentrator Mezzanine":        {"major_sn": 15, "major_code": "CM", "subtypes": sub_econ},
    "DCDC Board":                    {"major_sn": 16, "major_code": "DC", "subtypes": sub_dcdc},
    "Zipper Board":                  {"major_sn": 17, "major_code": "ZP", "subtypes": sub_zipper},
    'Tester':                        {"major_sn": 90, "major_code": "TS","subtypes": sub_tester},
    'Bare Cast Machined Tile':       {"major_sn": 20, "major_code": "BC","subtypes": sub_tester},
    'Bare Injection-Molded Tile':    {"major_sn": 21, "major_code": "BI","subtypes": sub_tester},
    'Wrapped Cast Machined Tile':    {"major_sn": 22, "major_code": "TC","subtypes": sub_tester},
    'Wrapped Injection-Molded Tile': {"major_sn": 23, "major_code": "TI","subtypes": sub_tester},
    'SiPM':                          {"major_sn": 24, "major_code": "SP","subtypes": sub_tester},
    'Tile PCB w/o Components':       {"major_sn": 25, "major_code": "TP","subtypes": sub_tester},
    'Tile PCB (TileBoard)':          {"major_sn": 26, "major_code": "TB","subtypes": sub_tester},
    'Tile Module':                   {"major_sn": 27, "major_code": "TM","subtypes": sub_tester},
    'Wingboard and Motherboard':     {"major_sn": 28, "major_code": "WM","subtypes": sub_tester},
    'TB Cable':                      {"major_sn": 29, "major_code": "CB","subtypes": sub_tile_4},

}    

MACs = {
    'UCSB': {'mac_code': "SB"}, 
    'CMU':  {'mac_code': "CM"}, 
    'IHEP': {'mac_code': "IH"},
    'NTU':  {'mac_code': "NT"},
    'TIFR': {'mac_code': "TI"},
    'TTU':  {'mac_code': "TT"},
}

def get_majortypes():
    return majortypes

def get_subtypes(key):
    return majortypes[key]["subtypes"] 

def get_macs():
    return MACs
