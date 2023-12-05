import core.sic_map

START_ADDR = 0
SIC_RESULT = []
FUNC_MP = {}

INSTRUCTIONS_MAP = core.sic_map.sic_instructions_map  = core.sic_map.sic_instructions_map 
 
class StartException(Exception):
    def __init__(self, message):
        super().__init__(message)

class SIC_Line:
    def __init__(self) -> None:
        self.location = ""
        self.first = ""
        self.second = ""
        self.third = ""
        self.obj_code = ""

def get_location(lines: list) -> list:
    base_addr = ""
    
    if lines[0][-2] != "START":
        error_message = "START Not Found!!"
        raise StartException(error_message)
    try:
        START_ADDR = int(lines[0][2], 16)
    except:
        error_message = "START Address Error!!"
        raise StartException(error_message)
    
    print("SIC_START_ADDRESS_IS: " + str(START_ADDR))
    last_location = START_ADDR
    for line in lines:
        curr_line_sic_obj = SIC_Line()
        curr_line_sic_obj.location = last_location
        if len(line) == 1:
            curr_line_sic_obj.second = line[0]
            if line[0] == "RSUB":
                last_location += 3
            else:
                last_location += 1
        else:
            curr_line_sic_obj.second = line[-2]
            curr_line_sic_obj.third = line[-1]
            if line[-2] in INSTRUCTIONS_MAP["pseudo"]:
                if line[-2] == "START":
                    last_location += 0
                elif line[-2] == "BYTE":
                    if line[-1][0].upper() == "C":
                        last_location += len(line[-1].replace(" ", "")) - 3
                    elif line[-1][0].upper() == "X":
                        last_location += (len(line[-1]) - 3) // 2
                elif line[-2] == "WORD":
                    last_location += 3
                elif line[-2] == "RESB":
                    last_location += int(line[-1])
                elif line[-2] == "RESW":
                    last_location += int(line[-1]) * 3
                elif line[-2] == "END":
                    last_location += 0
                elif line[-2] == "BASE":
                    last_location += 0
                    base_addr = line[-1]
                    curr_line_sic_obj.location = ""
                    
            elif line[-2][0] == "+":
                last_location += 4
            elif line[-2] in INSTRUCTIONS_MAP["instrucetion"]:
                last_location += int(INSTRUCTIONS_MAP["instrucetion"][line[-2]][1])
            else:
                error_message = f"Instruction not found!! -> {line[-2]}"
                raise StartException(error_message)
            
            if len(line) == 3:
                curr_line_sic_obj.first = line[-3]
                FUNC_MP[line[-3]] = curr_line_sic_obj.location
        SIC_RESULT.append(curr_line_sic_obj)
    FUNC_MP["BASE"] = FUNC_MP[base_addr]
    return [SIC_RESULT, FUNC_MP]