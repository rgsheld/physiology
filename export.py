#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 16:24:33 2017

@author: Richard
"""

import xlsxwriter

workbook = xlsxwriter.Workbook('train test.xlsx')
worksheet = workbook.add_worksheet()
row = 0
col = 0
for filename in os.listdir('/Volumes/Neurobio/KaeserLab/MEMBERS/Richard/DATA/Physiology Data/CPN eIPSC'):
    if filename.endswith(".abf"): 
        prot = ev.Protocol(filename)
        if len(prot.stim) < 50:
            # head = filename + " " + str(prot.ISI)
            # worksheet.write(row, col, head)
            # col += 2
            # row = 0
            pass
        else:
            head = filename + " " + 'train'
            worksheet.write(row, col, head)
            row += 2
            worksheet.write(row, col, 'amplitude')
            row += 1
            for i in range(len(prot.amp)):
                worksheet.write(row, col, prot.amp[i])
                row += 1
            col += 1
            row = 2
            worksheet.write(row, col, 'normalized')
            row += 1
            for i in range(len(prot.norm)):
                worksheet.write(row, col, prot.norm[i])
                row += 1
           # col = col - 1
            #worksheet.write(row, col, 'decay tau')
            #col += 1
            #worksheet.write(row, col, prot.decay_time)
            col += 2
            row = 0
            
workbook.close()