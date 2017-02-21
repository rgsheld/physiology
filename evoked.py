# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 17:26:30 2016

@author: rgshe

import a trace as an abf file using the neo module and plot
it in a new figure window.
"""

import numpy as np
from physiology.unpack import Unpack
from copy import copy


class Protocol(object):

    def __init__(self, trace):

        self.signal, self.times = Unpack(trace)
        self.avg = self.average(self.signal)
        self.stim = self.artifacts(self.avg, self.times)
        if len(self.stim) > 1:
            self.ISI = (min(self.stim[1]) - min(self.stim[0])) * self.times[1]
            self.amp, self.norm = self.amplitude(self.avg, self.stim)
        else:
            self.amp = self.amplitude(self.avg, self.stim)
            self.rise_idx, self.rise_time, self.decay_idx, self.decay_time = \
                self.kinetics(self.avg, self.stim, self.times)

    def average(self, signal):

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

        ddy = np.diff(np.diff(sweep_average)/times[1])/times[1]
        fact_index = np.where(abs(ddy[1500:]) > 2500)  # index protocol sensitive
        index_list = fact_index[0] + 1500
        if len(index_list) < 1:
            raise RuntimeError("No stimulus artifacts detected. Check file")
        events = []
        event_n = np.array(index_list[0])
        for i in range(1, (len(index_list))):
            if (index_list[i] - index_list[i-1] < 5):
                event_n = np.append(event_n, index_list[i])
            elif (np.size(event_n) < 2):
                event_n = np.array(index_list[i+1])
            else:
                event_n = np.append(event_n, np.array((max(event_n)+3)))
                events.append(event_n)
                event_n = np.array(index_list[i])

        if np.size(event_n) > 2:
            event_n = np.append(event_n, np.array((max(event_n)+3)))
            events.append(event_n)

        j = 0
        for i in range(0, len(events)):
            if (np.size(events[j]) < 5):
                del events[j]
            else:
                j += 1

        j = 1
        if len(events) > 1:
            for i in range(1, len(events)):
                if ((min(events[j]) - min(events[j-1])) * times[1]) < 5:
                    del events[j]
                else:
                    j += 1

        return events

    def amplitude(self, average, events):

        if len(events) == 1:
            amplitude = min(average[max(events[0]):])
            return amplitude

        else:
            amplitude = np.empty(len(events))
            norm_amp = np.empty(len(events))
            for i in range(0, len(events)):
                base = min(events[i]) - 1
                if (i <= (len(events) - 2)) and (len(events) > 2):
                    amplitude[i] = min(average[(base+15):min(events[i+1])]) \
                                   - average[base]
                    norm_amp[i] = amplitude[i] / amplitude[0]
                else:
                    amplitude[i] = min(average[(base+15):]) - average[base]
                norm_amp[i] = amplitude[i] / amplitude[0]
                """
                there's a problem with PPR. Maybe the base +15 fix
                """

        return amplitude, norm_amp

    def kinetics(self, avg, events, times):

        if len(events) > 1:
            return
        else:
            base = np.argmax(avg[max(events[0]):max(events[0])+10]) \
                    + max(events[0])
            peak = np.argmin(avg[base:]) + base
            amplitude = min(avg[base:])
            twenty = 0.2 * amplitude
            eighty = 0.8 * amplitude
            decay = 0.37 * amplitude

            rise_events = np.where(np.logical_and(avg[base:peak] < twenty,
                                           avg[base:peak] > eighty))
            rise_idx = rise_events[0] + base
            if len(rise_idx) >= 1:
                rise_time = (max(rise_idx) - min(rise_idx)) * times[1]
            else:
                rise_time = 'Rise time start not found'

            decay_events = np.where(np.logical_and(avg[peak:] > amplitude,
                                                   avg[peak:] < decay))
            decay_idx = decay_events[0] + peak
            decay_time = float((max(decay_idx) - min(decay_idx))) * times[1]

        return rise_idx, rise_time, decay_idx, decay_time
