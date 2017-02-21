#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 16:24:33 2017

@author: Richard
"""

import xlsxwriter

workbook = xlsxwriter.Workbook('PPR test.xlsx')
worksheet = workbook.add_worksheet()
row = 0
col = 0
files = []
for filename in os.listdir('/Volumes/Neurobio/KaeserLab/MEMBERS/Richard/DATA/Physiology Data/CPN eIPSC'):
    if filename.endswith(".abf"): 
        files.append(filename)

files.sort()
for j in range(len(files)):
    prot = ev.Protocol(files[j])
    if len(prot.stim) == 1 or len(prot.stim) == 50:
        # head = filename + " " + str(prot.ISI)
        # worksheet.write(row, col, head)
        # col += 2
        # row = 0
        pass
    else:
        head = str(files[j]) + " " + str(prot.ISI)
        worksheet.write(row, col, head)
        col += 1
        worksheet.write(row, col, prot.norm[1])
        #row += 1
        #for i in range(len(prot.amp)):
            #worksheet.write(row, col, prot.amp[i])
            #row += 1
        col = 0
        row += 2
        #worksheet.write(row, col, 'normalized')
        #row += 1
        #for i in range(len(prot.norm)):
          #  worksheet.write(row, col, prot.norm[i])
           # row += 1
       # col = col - 1
       #worksheet.write(row, col, 'decay tau')
       #col += 1
       #worksheet.write(row, col, prot.decay_time)
       #col += 2
       #row = 0
workbook.close()