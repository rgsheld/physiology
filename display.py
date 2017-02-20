#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 16:30:58 2017

@author: Richard
Blank stimulus artifacts and plot the trace
"""

import numpy as np
import matplotlib.pyplot as plt
from copy import copy


def blank(trace, facts):

    blanked = copy(trace)
    for i in range(0, len(facts)):
        p1 = min(facts[i]) - 1
        p2 = max(facts[i]) + 1
        p1V = blanked[p1]
        p2V = blanked[p2]
        points = np.linspace(p1, p2, num=(p2-p1), dtype=int)
        blank = np.interp(points, [p1, p2], [p1V, p2V])
        blanked[range(p1, p2)] = blank

    plt.plot(blanked)

    return blanked
