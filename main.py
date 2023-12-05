#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Author: TU

import argparse
import core.sic_map
import core.sic_preprocess
import core.sic_location
import core.sic_opcode

FUNC_MP = {}

class SIC_Line:
    def __init__(self) -> None:
        self.location = ""
        self.first = ""
        self.second = ""
        self.third = ""
        self.obj_code = ""
         
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source", required=True, help="Input the file name you want to assemble here")
    parser.add_argument("-o", "--ouput", required=True, help="The file to store the assembly result")

    args = parser.parse_args()
    
    sic_source = core.sic_preprocess.preprocess(args.source)
    sic_lined, FUNC_MP  = core.sic_location.get_location(sic_source)
    sic_lined = core.sic_opcode.get_opcode(sic_lined, FUNC_MP)
    
    curr_line_cnt = 5
    for i in sic_lined:
        if i == sic_lined[-1]: 
            print(f"{curr_line_cnt:<10} {'':<10} {i.first:<10} {i.second:<10} {i.third:<10}")
            continue
        if i.location != "":
            print(f"{curr_line_cnt:<10} {hex(i.location)[2:].upper().zfill(4):<10} {i.first:<10} {i.second:<10} {i.third:<10} {i.obj_code:<7}")
        else:
            print(f"{curr_line_cnt:<10} {'':<10} {i.first:<10} {i.second:<10} {i.third:<10} {i.obj_code:<10}")
            
        curr_line_cnt += 5
        
    curr_line_cnt = 5
    with open(args.ouput, "w") as f:
        for i in sic_lined:
            if i == sic_lined[-1]: 
                f.write(f"{curr_line_cnt:<10} {'':<10} {i.first:<10} {i.second:<10} {i.third:<10}\n")
                continue
            if i.location != "":
                f.write(f"{curr_line_cnt:<10} {hex(i.location)[2:].upper().zfill(4):<10} {i.first:<10} {i.second:<10} {i.third:<10} {i.obj_code:<7}\n")
            else:
                f.write(f"{curr_line_cnt:<10} {'':<10} {i.first:<10} {i.second:<10} {i.third:<10} {i.obj_code:<10}\n")
                
            curr_line_cnt += 5