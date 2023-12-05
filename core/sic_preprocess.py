import core.sic_map

INSTRUCTIONS_MAP = core.sic_map.sic_instructions_map 
TMP_MP = []
RES_MP = []

def preprocess(filepath: str)->list: 
    TMP_MP = []
    RES_MP = []
    with open(filepath, "r") as f:
        for i in f.read().split("\n"):
            i = i.split(".")[0]
            if len(i) == 0: continue
            for j in i.split(" "):
                if j == "": continue
                else: TMP_MP.append(j) 
            
    curr = 1
    buffer = []
    buffer.append(TMP_MP[0])
    
    while(curr < len(TMP_MP)):
        mode = ""
        if TMP_MP[curr] == "+":
            try:
                TMP_MP[curr + 1] = "+" + TMP_MP[curr + 1]
                curr += 1
                continue
            except: pass
            
        elif TMP_MP[curr][0] == "+": 
            mode = "+"
            TMP_MP[curr] = TMP_MP[curr][1:]
            
        if (TMP_MP[curr] in INSTRUCTIONS_MAP["instrucetion"]) or (TMP_MP[curr] in INSTRUCTIONS_MAP["pseudo"]):
            buffer.append(mode + TMP_MP[curr])
            if TMP_MP[curr] in INSTRUCTIONS_MAP["instrucetion"] and INSTRUCTIONS_MAP["instrucetion"][TMP_MP[curr]][1] == "1":
                curr += 1 
            elif TMP_MP[curr] == "RSUB":
                curr += 1
            else: 
                buffer.append(TMP_MP[curr + 1])
                curr += 2
            try:
                if TMP_MP[curr - 1][-1] == "," or TMP_MP[curr - 1] == "@" or TMP_MP[curr - 1] == "#":
                    buffer[-1] += TMP_MP[curr]
                    curr += 1
                elif TMP_MP[curr] == ",":
                    buffer[-1] += TMP_MP[curr] + TMP_MP[curr + 1]
                    curr += 2
                elif TMP_MP[curr][0] == ",":
                    buffer[-1] += TMP_MP[curr]
                    curr += 1
                    
            except: pass
            RES_MP.append(buffer)
            buffer = []
            #print(mp)
        else: 
            buffer.append(TMP_MP[curr])
            curr += 1
    return RES_MP
            
