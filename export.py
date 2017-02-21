#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 16:24:33 2017

@author: Richard
"""

import xlsxwriter

workbook = xlsxwriter.Workbook('python test 2.xlsx')
worksheet = workbook.add_worksheet()
row = 0
col = 0
for filename in os.listdir('/Volumes/Neurobio/KaeserLab/MEMBERS/Richard/DATA/Physiology Data/CPN eIPSC/python test'):
    if filename.endswith(".abf"): 
        prot = ev.Protocol(filename)
        if len(prot.stim) > 1:
            head = filename + " " + str(prot.ISI)
            worksheet.write(row, col, head)
            col += 2
            row = 0
        else:
            head = filename + " " + 'single'
            worksheet.write(row, col, head)
            row += 1
            worksheet.write(row, col, 'amplitude')
            col += 1
            worksheet.write(row, col, prot.amp)
            row += 1
            col = col - 1
            worksheet.write(row, col, 'rise time')
            col += 1
            worksheet.write(row, col, prot.rise_time)
            row += 1
            col = col - 1
            worksheet.write(row, col, 'decay tau')
            col += 1
            worksheet.write(row, col, prot.decay_time)
            col += 2
            row = 0
            
workbook.close()