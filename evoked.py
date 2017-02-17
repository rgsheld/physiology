# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 17:26:30 2016

@author: rgshe

import a trace as an abf file using the neo module and plot
it in a new figure window.
"""

from neo import io
import numpy as np


class Protocol(object):

    def __init__(self, trace):

        read = io.AxonIO(filename=trace)
        bl = read.read_block(cascade=True, lazy=False)

        self.signal = np.empty([len(bl.segments[0].analogsignals[0]), \
																											len(bl.segments)])
        for i in range(0, len(bl.segments)):
            sweep = bl.segments[i].analogsignals[0]
            sweep = np.squeeze(sweep)
            self.signal[:, i] = sweep

        for i, asig in enumerate(bl.segments[0].analogsignals):
            self.times = asig.times.rescale('s').magnitude

        self.avg = self.average(self.signal)
        self.stim = self.artifacts(self.avg, self.times)
        if len(self.stim) > 1:
            self.ISI = (min(self.stim[1]) - min(self.stim[0])) * self.times[1]
            self.amp, self.norm = self.amplitude(self.avg, self.stim)
        else:
            self.amp = self.amplitude(self.avg, self.stim)

    def average(self, signal):
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

    def artifacts(self, sweep_average, times):

        """this is working fairly well but there is still an issue
				with the last artifact not being fully covered"""

        ddy = np.diff(np.diff(sweep_average)/times[1])/times[1]
        fact_index = np.where(abs(ddy[1500:]) > 3000000000)  # index protocol sensitive
        index_list = fact_index[0] + 1500
        events = []
        event_n = np.array(index_list[0])
        for i in range(1, (len(index_list))):
            if (index_list[i] - index_list[i-1] < 5):
                event_n = np.append(event_n, index_list[i])
            else:
                event_n = np.append(event_n, np.array((max(event_n)+3)))
                events.append(event_n)
                event_n = np.array(index_list[i])

        event_n = np.append(event_n, np.array((max(event_n)+3)))
        events.append(event_n)

        return events

    def amplitude(self, average, events):

        if len(events) == 1:
            amplitude = min(average[max(events[0]):])
            return amplitude

        else:
            amplitude = np.empty(len(events))
            norm_amp = np.empty(len(events))
            for i in range(0, len(events)):
                base = min(events[i])
                if (i <= (len(events) - 2)) and (len(events) > 2):
                    amplitude[i] = min(average[base:min(events[i+1])]) \
                                   - average[base]
                    norm_amp[i] = amplitude[i] / amplitude[0]
                else:
                    amplitude[i] = min(average[base:]) - average[base]
                norm_amp[i] = amplitude[i] / amplitude[0]

        return amplitude, norm_amp
