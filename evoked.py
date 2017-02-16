# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 17:26:30 2016

@author: rgshe

import a trace as an abf file using the neo module and plot
it in a new figure window.
"""

from neo import io
import numpy as np
from itertools import groupby
from operator import itemgetter


def unpack(trace):
    """reads an abf file and outputs the data as a numpy
    array as well as the time points in seconds.
    ----------------------------------------------------
    Usage:
        import evoked as ev
        signal, times = ev.unpack('trace')
    """

    read = io.AxonIO(filename=trace)
    bl = read.read_block(cascade=True, lazy=False)

    signal = np.empty([len(bl.segments[0].analogsignals[0]), len(bl.segments)])
    for i in range(0, len(bl.segments)):
        sweep = bl.segments[i].analogsignals[0]
        sweep = np.squeeze(sweep)
        signal[:, i] = sweep

    for i, asig in enumerate(bl.segments[0].analogsignals):
        times = asig.times.rescale('s').magnitude

    return signal, times


def average(signal):
    "baseline_mean = []"

    for i in range(0, len(signal[1])):
        sweep = signal[:, i]
        sweep = np.squeeze(sweep)
        dy = np.diff(sweep)

        j = 0
        baseline = []
        while(abs(dy[j]) < 200):
            baseline.append(sweep[j])
            j = j + 1

        signal[:, i] = signal[:, i] - np.mean(baseline)

    sweep_average = np.mean(signal, 1)
    return sweep_average


def artifacts(sweep_average):
    
    """there's somethign off with the way i'm identifying artifacts
    it's too sensitive to the variable shape and amplitude of the facts.
    I think a better way may be to search for the sign inversion"""

    ddy = np.diff(np.diff(sweep_average))
    fact_index = np.where(abs(ddy[1500:]) > 300)  # index protocol sensitive
    index_list = fact_index[0] + 1500
    events = []
    event_n = np.array(index_list[0])
    for i in range(1, (len(index_list))):
        if (index_list[i] - index_list[i-1] < 5) and (i < len(index_list)):
            event_n = np.append(event_n, index_list[i])
        else:
            event_n = np.append(event_n, np.array((max(event_n)+3)))
            events.append(event_n)
            event_n = np.array(index_list[i])

    return events


def amplitude(average, events):

    if len(events) == 1:
        amplitude = min(average[max(events[0]):])
        return amplitude

    else:
        amplitude = np.empty(len(events))
        norm_amp = np.empty(len(events))
        for i in range(0, len(events)):
            base = np.argmax(average[max(events[i]):(max(events[i])+15)]) \
																+ max(events[i])
            if (i <= (len(events) - 2)) and (len(events) > 2):
                amplitude[i] = min(average[base:min(events[i+1])]) \
                               - average[base]
                norm_amp[i] = amplitude[i] / amplitude[0]
            else:
                amplitude[i] = min(average[base:]) - average[base]
            norm_amp[i] = amplitude[i] / amplitude[0]

    return amplitude, norm_amp

    """there's something off with running this in KO conditions"""
