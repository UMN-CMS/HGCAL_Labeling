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

sub_baseplate = {}
mat_list = ["", "W", "P", "C"]
den_list = ["", "L", "H"]
cut_list = ["", "T", "B", "L", "R", "F"]

mat_name = ["", "WCu", "PCB", "Carbon Fiber"]
den_name = ["", "LD", "HD"]
cut_name = ["Full", "Top", "Bottom", "Left", "Right", "Five"]

for mat in range(1,4):
    for den in range(1,3):
        for cut in range(0,6):

            sub_sn = str(mat) + str(den) + str(cut)
            sub_code = mat_list[mat] + den_list[den] + cut_list[cut]
            name = "{} {} {}".format(den_name[den], cut_name[cut], mat_name[mat])

            sub_baseplate["BA{}".format(sub_code)] = {"sub_sn": sub_sn, "sub_code": sub_code, "name": name}

sub_ldhexaboard = {
    "XLF01":         {"sub_sn": "001", "sub_code": "F01", "name": "Full V2", "lower":00000},
    "XLF02":         {"sub_sn": "002", "sub_code": "F02", "name": "Full NSH", "lower":00500},
    "XLF03":         {"sub_sn": "003", "sub_code": "F03", "name": "Full V3", "lower":01000},
    "XLF10":         {"sub_sn": "010", "sub_code": "F10", "name": "Full Production", "lower":10000},

    "XLT03":         {"sub_sn": "103", "sub_code": "T03", "name": "Half Top V3", "lower":05000},
    "XLT10":         {"sub_sn": "110", "sub_code": "T10", "name": "Half Top Production", "lower":50000},
    "XLB03":         {"sub_sn": "203", "sub_code": "B03", "name": "Half Bottom V3", "lower":05500},
    "XLB10":         {"sub_sn": "210", "sub_code": "B10", "name": "Half Bottom Production", "lower":55000},

    "XLL03":         {"sub_sn": "303", "sub_code": "L03", "name": "Semi Left V3", "lower":06000},
    "XLL10":         {"sub_sn": "310", "sub_code": "L10", "name": "Semi Left Production", "lower":60000},
    "XLR03":         {"sub_sn": "403", "sub_code": "R03", "name": "Semi Right V3", "lower":06500},
    "XLR10":         {"sub_sn": "410", "sub_code": "R10", "name": "Semi Right Production", "lower":65000},

    "XL503":         {"sub_sn": "503", "sub_code": "503", "name": "Five V3", "lower":07000},
    "XL510":         {"sub_sn": "510", "sub_code": "510", "name": "Five Production", "lower":70000},
}

sub_hdhexaboard = {
    "XHF03":         {"sub_sn": "003", "sub_code": "F03", "name": "Full V3", "lower":07500},
    "XHF10":         {"sub_sn": "010", "sub_code": "F10", "name": "Full Production", "lower":75000},

    "XHT03":         {"sub_sn": "103", "sub_code": "T03", "name": "Top (Half Minus) V3", "lower":8500},
    "XHT10":         {"sub_sn": "110", "sub_code": "T10", "name": "Top (Half Minus) Production", "lower":85000},
    "XHB03":         {"sub_sn": "203", "sub_code": "B03", "name": "Bottom (Chop Two) V3", "lower":8800},
    "XHB10":         {"sub_sn": "210", "sub_code": "B10", "name": "Bottom (Chop Two) Production", "lower":88000},

    "XHL03":         {"sub_sn": "303", "sub_code": "L03", "name": "Left V3", "lower":9100},
    "XHL10":         {"sub_sn": "310", "sub_code": "L10", "name": "Left Production", "lower":91000},
    "XHR03":         {"sub_sn": "403", "sub_code": "R03", "name": "Right V3", "lower":9400},
    "XHR10":         {"sub_sn": "410", "sub_code": "R10", "name": "Right Production", "lower":94000},
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
    "EngV1":        {"sub_sn": "0000", "sub_code": "0000", "name": "V1"},
    "EngV2":        {"sub_sn": "0100", "sub_code": "0100", "name": "V2"},
    "EngV2b":       {"sub_sn": "0200", "sub_code": "0200", "name": "V2b"},
    "EngV3":        {"sub_sn": "0300", "sub_code": "0300", "name": "V3 East"},
    "EngV3W":       {"sub_sn": "0310", "sub_code": "0310", "name": "V3 West"},
    "EngEQ":        {"sub_sn": "0400", "sub_code": "0QE0", "name": "Qualification East"},
    "EngWQ":        {"sub_sn": "0410", "sub_code": "0QW0", "name": "Qualification West"},
    "EngDmy":       {"sub_sn": "0310", "sub_code": "0900", "name": "Mechanical Dummy East"},
    "Eng E":        {"sub_sn": "1000", "sub_code": "10E0", "name": "East"},
    "Eng EB":       {"sub_sn": "1001", "sub_code": "10EB", "name": "East Bare"},
    "Eng W":        {"sub_sn": "1010", "sub_code": "10W0", "name": "West"},
    "Eng WB":       {"sub_sn": "1011", "sub_code": "10WB", "name": "West Bare"},
}
sub_hdengine = {
    "HDEF3":        {"sub_sn": "0300", "sub_code": "03F0", "name": "V3 Full"},
    "HDE FQ":        {"sub_sn": "0400", "sub_code": "0QF0", "name": "Qualification Full"},
    "HDE HQ":        {"sub_sn": "0410", "sub_code": "0QH0", "name": "Qualification Half"},
    "HDE F":        {"sub_sn": "1000", "sub_code": "10F0", "name": "Full"},
    "HDE FB":        {"sub_sn": "1001", "sub_code": "10FB", "name": "Full Bare"},
    "HDE H":        {"sub_sn": "1010", "sub_code": "10H0", "name": "Half"},
    "HDE HB":        {"sub_sn": "1011", "sub_code": "10HB", "name": "Half Bare"},
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
    "West 1 Debug": {"sub_sn": "10Z1", "sub_code": "10Z1"},
    "West 1F+1P A":  {"sub_sn": "11A1", "sub_code": "11A1"}
}
sub_hdwagon = {
    "Prototype A":        {"sub_sn": "3010", "sub_code": "30A0"},
    "Prototype C":        {"sub_sn": "3030", "sub_code": "30C0"},
    "Straight 3 HDEF":       {"sub_sn": "3011", "sub_code": "30A1"},
    "Straight 3 HDEH":       {"sub_sn": "3021", "sub_code": "30B1"},
    "Triangle 3 LT 1":       {"sub_sn": "3031", "sub_code": "30C1"},
    "Triangle 3 LT 2":       {"sub_sn": "3032", "sub_code": "30C2"},
    "Straight 3 Small": {"sub_sn": "", "sub_code": "130C"},
    "Straight 3.5":     {"sub_sn": "3111", "sub_code": "31A1"},
    "J-Shaped 3.5":     {"sub_sn": "3121", "sub_code": "31B1"},
    "Straight 2":       {"sub_sn": "2011", "sub_code": "20A1"},
    "Straight 2.5 HDEF":     {"sub_sn": "2111", "sub_code": "21A1"},
    "Straight 2.5 HDEH":     {"sub_sn": "2121", "sub_code": "21B1"}
}
sub_econ = {
    "Full, ECON-T COB Proto":  {"sub_sn": "1111", "sub_code": "1F11"},
    "Full, ECON-T Proto":      {"sub_sn": "1112", "sub_code": "1F12"},
    "Full, ECON-D COB Proto":  {"sub_sn": "1121", "sub_code": "1F21"},
    "Full Proto":              {"sub_sn": "1122", "sub_code": "1F22"},
    "Dummy":                   {"sub_sn": "1190", "sub_code": "1F90"},
    "Partial Semi-Right, T+D": {"sub_sn": "1230", "sub_code": "1RT0"},
    "Full ECON-T+D":           {"sub_sn": "2100", "sub_code": "2F00"},
    "Partial Semi-Right, T+D": {"sub_sn": "2230", "sub_code": "2RT0"},
    "Partial Semi-Right, T+D": {"sub_sn": "2340", "sub_code": "2LB0"},
    "Partial Semi-Right, T+D": {"sub_sn": "2540", "sub_code": "25R0"},
    "Partial Semi-Right, T+D": {"sub_sn": "2550", "sub_code": "25L0"},
}
sub_dcdc = {
    "TST1":         {"sub_sn": "9001", "sub_code": "TST1"}
}
sub_zipper = {
    "Semi/Half Straight":   {"sub_sn": "1100", "sub_code": "AR00"},
    "Five Right":           {"sub_sn": "2100", "sub_code": "BR00"},
    "Five Left":            {"sub_sn": "3100", "sub_code": "CR00"},
    "Five Right Snake":     {"sub_sn": "2200", "sub_code": "BS00"},
    "Semi/Half LPGBT":      {"sub_sn": "1300", "sub_code": "AL00"}
}
sub_tester = {
    "TBT":          {"sub_sn": "0001", "sub_code": "0001", "name": "Tileboard Tester"},
    "TBT2":         {"sub_sn": "0002", "sub_code": "0002", "name": "Tileboard Tester V2"},
    "HXCTR1":       {"sub_sn": "0011", "sub_code": "0011", "name": "Hexacontroller"},
    "HXCTR2":       {"sub_sn": "0011", "sub_code": "0011", "name": "Hexacontroller2"},
    "ZCU102":       {"sub_sn": "0021", "sub_code": "0021", "name": "ZCU"},
    "WagT":         {"sub_sn": "0031", "sub_code": "0031", "name": "Wagon Tester"},
    "WagWhl":       {"sub_sn": "0032", "sub_code": "0032", "name": "Wagon Wheel"},
    "WagAdE":       {"sub_sn": "0033", "sub_code": "0033", "name": "Wagon Adapter East"},
    "WagAdW":       {"sub_sn": "0034", "sub_code": "0034", "name": "Wagon Adapter West"},
    "EngT":         {"sub_sn": "0400", "sub_code": "0400", "name": "Engine Tester"},
    "EngLIE":       {"sub_sn": "0410", "sub_code": "0410", "name": "Engine Tester LD Interposer East"},
    "EngLIW":       {"sub_sn": "0420", "sub_code": "0420", "name": "Engine Tester LD Interposer West"},
    "EngHI":        {"sub_sn": "0430", "sub_code": "0430", "name": "Engine Tester HD Interposer"}
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
    'Baseplates':                    {"major_sn": 1, "major_code": "BA","subtypes": sub_baseplate},
    'LD Sensors':                    {"major_sn": 2, "major_code": "SL","subtypes": None},
    'HD Sensors':                    {"major_sn": 3, "major_code": "SH","subtypes": None},
    'LD Protomodules':               {"major_sn": 4, "major_code": "PL","subtypes": None},
    'HD Protomodules':               {"major_sn": 5, "major_code": "PH","subtypes": None},
    'LD Hexaboard':                  {"major_sn": 6, "major_code": "XL","subtypes": sub_ldhexaboard},
    'HD Hexaboard':                  {"major_sn": 7, "major_code": "XH","subtypes": sub_hdhexaboard},
    'LD Module':                     {"major_sn": 8,  "major_code": "ML","subtypes": sub_ldmodule},
    'HD Module':                     {"major_sn": 9,  "major_code": "MH","subtypes": sub_hdmodule},
    "LD Engine":                     {"major_sn": 10, "major_code": "EL", "subtypes": sub_ldengine},
    "HD Engine":                     {"major_sn": 11, "major_code": "EH", "subtypes": sub_hdengine},
    "LD Wagon East":                 {"major_sn": 12, "major_code": "WE", "subtypes": sub_ldwagoneast},
    "LD Wagon West":                 {"major_sn": 13, "major_code": "WW", "subtypes": sub_ldwagonwest},
    "HD Wagon":                      {"major_sn": 14, "major_code": "WH", "subtypes": sub_hdwagon},
    "Concentrator Mezzanine":        {"major_sn": 15, "major_code": "CM", "subtypes": sub_econ},
    "DCDC Board":                    {"major_sn": 16, "major_code": "DC", "subtypes": sub_dcdc},
    "Zipper Board":                  {"major_sn": 17, "major_code": "ZP", "subtypes": sub_zipper},
    'Tester':                        {"major_sn": 90, "major_code": "TS","subtypes": sub_tester},
    'Bare Cast Machined Tile':       {"major_sn": 20, "major_code": "BC","subtypes": None},
    'Bare Injection-Molded Tile':    {"major_sn": 21, "major_code": "BI","subtypes": None},
    'Wrapped Cast Machined Tile':    {"major_sn": 22, "major_code": "TC","subtypes": None},
    'Wrapped Injection-Molded Tile': {"major_sn": 23, "major_code": "TI","subtypes": None},
    'SiPM':                          {"major_sn": 24, "major_code": "SP","subtypes": None},
    'Tile PCB w/o Components':       {"major_sn": 25, "major_code": "TP","subtypes": None},
    'Tile PCB (TileBoard)':          {"major_sn": 26, "major_code": "TB","subtypes": None},
    'Tile Module':                   {"major_sn": 27, "major_code": "TM","subtypes": None},
    'Wingboard and Motherboard':     {"major_sn": 28, "major_code": "WM","subtypes": None},
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
