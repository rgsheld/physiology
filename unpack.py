#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 14:37:38 2017

@author: Richard
Unpack a axon abf file into a numpy array of sweeps (i.e. *signal*)
and an array of times (i.e. *times*) in seconds.
"""
import numpy as np
from neo import io


def Unpack(file):

    read = io.AxonIO(filename=file)
    bl = read.read_block(cascade=True, lazy=False)

    signal = np.empty([len(bl.segments[0].analogsignals[0]),
                      len(bl.segments)])
    for i in range(0, len(bl.segments)):
        sweep = bl.segments[i].analogsignals[0]
        sweep = np.squeeze(sweep)
        signal[:, i] = sweep

    for i, asig in enumerate(bl.segments[0].analogsignals):
        times = asig.times.rescale('s').magnitude

    return signal, times
