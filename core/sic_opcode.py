import core.sic_map
from string import ascii_letters

INSTRUCTIONS_MAP = core.sic_map.sic_instructions_map 
SIC_RESULT = []
FUNC_MP = {}

register_mp = {"A": "0", "X": "1", "L": "2", "B": "3",
                   "S": "4", "T": "5", "F": "6", "PC": "8", "SW": "9"}

class SIC_Line:
    def __init__(self) -> None:
        self.location = ""
        self.first = ""
        self.second = ""
        self.third = ""
        self.obj_code = ""
        
def get_byte(line):
    mode = line.third[:2]
    data = line.third[2:-1]
    objCode = ""
    if (mode == "C'"):
        for i in data:
            objCode += (hex(ord(i))[2:].upper()).zfill(2)
    elif (mode == "X'"):
        objCode += data
    return objCode

def get_word(line):
    if (int(line.third) >= 0):
        objCode = hex(int(line.third))[2:].upper().zfill(6)
    else:
        full_hex = int("1000000", 16)
        objCode = hex(full_hex + int(line.third))[2:].upper().zfill(6)
    return objCode

def get_1byte(line):
    return INSTRUCTIONS_MAP["instrucetion"][line.second][0]
    
def get_2byte(line):
    objCode = ""
    tmp = line.third.split(",")
    if len(tmp) == 1:
        objCode += INSTRUCTIONS_MAP["instrucetion"][line.second][0]
        objCode += register_mp[line.third]
    else:
        objCode += INSTRUCTIONS_MAP["instrucetion"][line.second][0]
        objCode += register_mp[tmp[0]]
        objCode += register_mp[tmp[1]]        
    return objCode.ljust(4, "0")

def get_opcode(lines: list, get_FUNC_MP: dict) -> list:
    global FUNC_MP 
    FUNC_MP = get_FUNC_MP
    for curr_line, line in enumerate(lines):
        if line.second in INSTRUCTIONS_MAP["pseudo"]:
            if line.second == "START": 
                SIC_RESULT.append(line)
                continue
            if line.second == "END":
                SIC_RESULT.append(line)
                continue
            if line.second == "BASE":
                SIC_RESULT.append(line)
                continue
            if line.second == "BYTE":
                line.obj_code = get_byte(line)
                SIC_RESULT.append(line)
                continue
            if line.second == "WORD":
                line.obj_code = get_word(line)
                SIC_RESULT.append(line)
                continue
            if line.second == "RESB":
                SIC_RESULT.append(line)
                continue
            if line.second == "RESW":
                SIC_RESULT.append(line)
                continue
        elif line.second in INSTRUCTIONS_MAP["instrucetion"] and INSTRUCTIONS_MAP["instrucetion"][line.second][1] == "1":
            line.obj_code = get_1byte(line)
            SIC_RESULT.append(line)
            continue
        elif line.second in INSTRUCTIONS_MAP["instrucetion"] and INSTRUCTIONS_MAP["instrucetion"][line.second][1] == "2":
            line.obj_code = get_2byte(line)
            SIC_RESULT.append(line)
            continue
        elif line.second.replace("+","") in INSTRUCTIONS_MAP["instrucetion"] and INSTRUCTIONS_MAP["instrucetion"][line.second.replace("+","")][1] == "3":
            if line.second == "RSUB":
                line.obj_code = "4F0000"
                SIC_RESULT.append(line)
                continue
            elif "+" == line.second[0]:        
                if ",X" in line.third:
                    tmp_op = int(INSTRUCTIONS_MAP["instrucetion"][line.second.replace("+","")][0], 16)
                    tmp_op += 3
                    line.obj_code += hex(tmp_op)[2:].upper().zfill(2)
                    line.obj_code += "9"
                    try:   
                        line.obj_code += hex(FUNC_MP[line.third.split(",")[0]])[2:].upper().zfill(5)
                    except:
                        line.obj_code += hex(int(line.third.split(",")[0]))[2:].upper().zfill(5)
                    SIC_RESULT.append(line)
                    continue
                elif "@" == line.third[0]:
                    tmp_op = int(INSTRUCTIONS_MAP["instrucetion"][line.second.replace("+","")][0], 16)
                    tmp_op += 2
                    line.obj_code += hex(tmp_op)[2:].upper().zfill(2)
                    line.obj_code += "1"
                    try:
                        
                        line.obj_code += hex(FUNC_MP[line.third.replace("@","")])[2:].upper().zfill(5)
                    except:
                        line.obj_code += hex(int(line.third.replace("@","")))[2:].upper().zfill(5)
                    SIC_RESULT.append(line)
                    continue
                elif "#" == line.third[0]:
                    tmp_op = int(INSTRUCTIONS_MAP["instrucetion"][line.second.replace("+","")][0], 16)
                    tmp_op += 1
                    line.obj_code += hex(tmp_op)[2:].upper().zfill(2)
                    line.obj_code += "1"
                    try:
                        line.obj_code += hex(FUNC_MP[line.third.replace("#","")])[2:].upper().zfill(5)
                    except:   
                        line.obj_code += hex(int(line.third.replace("#","")))[2:].upper().zfill(5)
                    SIC_RESULT.append(line)
                    continue
                else:
                    tmp_op = int(INSTRUCTIONS_MAP["instrucetion"][line.second.replace("+","")][0], 16)
                    tmp_op += 3
                    line.obj_code += hex(tmp_op)[2:].upper().zfill(2)
                    line.obj_code += "1"
                    try:
                        line.obj_code += hex(FUNC_MP[line.third])[2:].upper().zfill(5)
                    except:   
                        line.obj_code += hex(int(line.third))[2:].upper().zfill(5)
                    SIC_RESULT.append(line)
                    continue
            else:
                mode = "m"
                try:
                    if int(line.third.split(",")[0].replace("@", "").replace("#", "")) < 4096:
                        mode = "c"                           
                except:
                    pass
                if mode == "c":
                    if ",X" in line.third:
                        tmp_op = int(INSTRUCTIONS_MAP["instrucetion"][line.second][0], 16)
                        tmp_op += 3
                        line.obj_code += hex(tmp_op)[2:].upper().zfill(2)
                        line.obj_code += "8"
                        line.obj_code += hex(int(line.third.split(",")[0]))[2:].upper().zfill(3)
                        SIC_RESULT.append(line)
                        continue
                    elif "@" == line.third[0]:
                        tmp_op = int(INSTRUCTIONS_MAP["instrucetion"][line.second][0], 16)
                        tmp_op += 2
                        line.obj_code += hex(tmp_op)[2:].upper().zfill(2)
                        line.obj_code += "0"
                        line.obj_code += hex(int(line.third.replace("@","")))[2:].upper().zfill(3)
                        SIC_RESULT.append(line)
                        continue
                    elif "#" == line.third[0]:
                        tmp_op = int(INSTRUCTIONS_MAP["instrucetion"][line.second][0], 16)
                        tmp_op += 1
                        line.obj_code += hex(tmp_op)[2:].upper().zfill(2)
                        line.obj_code += "0"   
                        line.obj_code += hex(int(line.third.replace("#","")))[2:].upper().zfill(3)
                        SIC_RESULT.append(line)
                        continue
                    else:
                        tmp_op = int(INSTRUCTIONS_MAP["instrucetion"][line.second][0], 16)
                        tmp_op += 3
                        line.obj_code += hex(tmp_op)[2:].upper().zfill(2)
                        line.obj_code += "0"
                        line.obj_code += hex(int(line.third))[2:].upper().zfill(3)
                        SIC_RESULT.append(line)
                        continue
                else:
                    m_mode = "pc"
                    tmp_cnt = 1
                    while(lines[curr_line + tmp_cnt].location == ""):
                        tmp_cnt += 1
                    diff = FUNC_MP[line.third.split(",")[0].replace("@", "").replace("#", "")] - lines[curr_line + tmp_cnt].location
                    if diff > 2047 or diff < -2048:
                        m_mode = "b"
                    
                    if m_mode == "b":
                        if ",X" in line.third:
                            tmp_op = int(INSTRUCTIONS_MAP["instrucetion"][line.second][0], 16)
                            tmp_op += 3
                            line.obj_code += hex(tmp_op)[2:].upper().zfill(2)
                            line.obj_code += "C"
                            disp = FUNC_MP[line.third.split(",")[0]] - FUNC_MP["BASE"]
                            line.obj_code += hex(disp)[2:].upper().zfill(3)
                            SIC_RESULT.append(line)
                            continue
                        elif "@" == line.third[0]:
                            tmp_op = int(INSTRUCTIONS_MAP["instrucetion"][line.second][0], 16)
                            tmp_op += 2
                            line.obj_code += hex(tmp_op)[2:].upper().zfill(2)
                            line.obj_code += "4"
                            disp = FUNC_MP[line.third.replace("@","")] - FUNC_MP["BASE"]
                            line.obj_code += hex(disp)[2:].upper().zfill(3)
                            SIC_RESULT.append(line)
                            continue
                        elif "#" == line.third[0]:
                            tmp_op = int(INSTRUCTIONS_MAP["instrucetion"][line.second][0], 16)
                            tmp_op += 1
                            line.obj_code += hex(tmp_op)[2:].upper().zfill(2)
                            line.obj_code += "4"
                            disp = FUNC_MP[line.third.replace("#","")] - FUNC_MP["BASE"]
                            line.obj_code += hex(disp)[2:].upper().zfill(3)
                            SIC_RESULT.append(line)
                            continue
                        else:
                            tmp_op = int(INSTRUCTIONS_MAP["instrucetion"][line.second][0], 16)
                            tmp_op += 3
                            line.obj_code += hex(tmp_op)[2:].upper().zfill(2)
                            line.obj_code += "4"
                            disp = FUNC_MP[line.third.replace("#","")] - FUNC_MP["BASE"]
                            line.obj_code += hex(disp)[2:].upper().zfill(3)
                            SIC_RESULT.append(line)
                            continue
                    else:
                        if ",X" in line.third:
                            tmp_op = int(INSTRUCTIONS_MAP["instrucetion"][line.second][0], 16)
                            tmp_op += 3
                            line.obj_code += hex(tmp_op)[2:].upper().zfill(2)
                            line.obj_code += "A"
                            disp = FUNC_MP[line.third.split(",")[0]] - lines[curr_line + tmp_cnt].location
                            if disp < 0:
                                line.obj_code += hex(int("FFF", 16) + (disp + 1))[2:].upper().zfill(3)
                            else:
                                line.obj_code += hex(disp)[2:].upper().zfill(3)
                            SIC_RESULT.append(line)
                            continue
                        elif "@" == line.third[0]:
                            tmp_op = int(INSTRUCTIONS_MAP["instrucetion"][line.second][0], 16)
                            tmp_op += 2
                            line.obj_code += hex(tmp_op)[2:].upper().zfill(2)
                            line.obj_code += "2"
                            disp = FUNC_MP[line.third.replace("@","")] - lines[curr_line + tmp_cnt].location
                            if disp < 0:
                                line.obj_code += hex(int("FFF", 16) + (disp + 1))[2:].upper().zfill(3)
                            else:
                                line.obj_code += hex(disp)[2:].upper().zfill(3)
                            SIC_RESULT.append(line)
                            continue
                        elif "#" == line.third[0]:
                            tmp_op = int(INSTRUCTIONS_MAP["instrucetion"][line.second][0], 16)
                            tmp_op += 1
                            line.obj_code += hex(tmp_op)[2:].upper().zfill(2)
                            line.obj_code += "2"
                            disp = FUNC_MP[line.third.replace("#","")] - lines[curr_line + tmp_cnt].location
                            if disp < 0:
                                line.obj_code += hex(int("FFF", 16) + (disp + 1))[2:].upper().zfill(3)
                            else:
                                line.obj_code += hex(disp)[2:].upper().zfill(3)
                            SIC_RESULT.append(line)
                            continue
                        else:
                            tmp_op = int(INSTRUCTIONS_MAP["instrucetion"][line.second][0], 16)
                            tmp_op += 3
                            line.obj_code += hex(tmp_op)[2:].upper().zfill(2)
                            line.obj_code += "2"
                            disp = FUNC_MP[line.third.replace("#","")] - lines[curr_line + tmp_cnt].location
                            if disp < 0:
                                line.obj_code += hex(int("FFF", 16) + (disp + 1))[2:].upper().zfill(3)
                            else:
                                line.obj_code += hex(disp)[2:].upper().zfill(3)
                            SIC_RESULT.append(line)
                            continue
                    
                    
                
    return SIC_RESULT     


    
    
    
    