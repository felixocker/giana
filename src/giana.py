#!/usr/bin/env python3
"""analyze coding habits via commits - plot results"""

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
import sys
import time

from datetime import datetime, timezone

class Giana():
    """analyze commit history and plot results"""

    def __init__(self, repo=None, day=7, night=19):
        """initalize with info what is considered day and night"""
        self.repo = repo
        self.day = day
        self.night = night
        self.day_night_dist = [None]*2
        self.commits_by_hour = np.zeros((7, 24), dtype=int)
        self.barchart = None
        self.heatmap = None
        with open("giana.log", "r") as file:
            self.data = file.readlines()
        self.data = [time.strptime(x.strip()[:-6]) for x in self.data]

    def analyze_binary(self):
        """distinguish commit times by day and night"""
        by_day = [0] * 7
        by_night = [0] * 7
        for x in self.data:
            if self.night > x.tm_hour > self.day:
                by_day[x.tm_wday] += 1
            else:
                by_night[x.tm_wday] += 1
        self.day_night_dist = [by_day, by_night]

    def plot_barchart(self):
        """plot chart for day/ night distribution by day"""
        labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        width = 0.35
        fig, ax = plt.subplots()
        ax.bar(labels, self.day_night_dist[1], width, label=self.label_barchart('night', self.night, self.day), color='midnightblue')
        ax.bar(labels, self.day_night_dist[0], width, bottom=self.day_night_dist[1], label=self.label_barchart('day', self.day, self.night), color='lightsteelblue')
        ax.set_ylabel('Commits')
        ax.set_title(f'Commits by day and time for { self.repo }')
        ax.legend()
        self.barchart = ax.get_figure()
        plt.show()

    @staticmethod
    def label_barchart(text, start, end):
        return text+' ('+str(start)+' - '+str(end)+')'

    def analyze_by_hour(self):
        """count number of commits by day and hour"""
        for x in self.data:
            self.commits_by_hour[x.tm_wday][x.tm_hour] += 1
        self.commits_by_hour = self.commits_by_hour.transpose()

    def plot_heatmap(self):
        """plot and show heatmap for commits by day and hour"""
        x_axis_labels=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        y_axis_labels=[datetime.fromtimestamp(d, tz=timezone.utc).strftime('%H:%M') for d in range(0, 60*60*24, 60*60)]
        ax = sns.heatmap(self.commits_by_hour, xticklabels=x_axis_labels, yticklabels=y_axis_labels, linewidth=4, cmap="Blues")
        ax.set_title(f'Commits by day and time for { self.repo }')
        ax.set(xlabel = "Day", ylabel = "Time")
        self.heatmap = ax.get_figure()
        plt.show()

    def save(self):
        """save current plot as file"""
        self.barchart.savefig(self.repo + "-barchart.png")
        self.heatmap.savefig(self.repo + "-heatmap.png")

if __name__ == "__main__":
    giana = Giana(sys.argv[1].split("/")[-1])
    giana.analyze_binary()
    giana.plot_barchart()
    giana.analyze_by_hour()
    giana.plot_heatmap()
    giana.save()

