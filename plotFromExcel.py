#!/usr/bin/env python
"""
    Read an excel file with all the tracks and produce a plot of the tracks
"""
import pandas as pd
import matplotlib.pyplot as plt

# config
# the input file with all the tracks
EXCEL_FILE = 'tracks.xlsx'
# mininum number of timepoints a track must have to be plotted
MIN_TIMEPOINTS = 40
# maximum number of tracks to plot
MAX_TRACKS = 9999999999999999
# end config

print("Reading file")
xl = pd.ExcelFile(EXCEL_FILE)
print("Parsing first sheet")
df = xl.parse('Sheet1')
print("Removing useless columns")
df = df.drop(columns=['type', 'classname', 'version', 'z', 'linklist'])
print("Grouping by id")
dfg = df.groupby(['id'])
# get a dict where the key is the id and the value is the dataframe
groups = dict(list(dfg))
print("Found {} tracks".format(len(groups)))

i = 1
plotted = 0

# plot all on same figure
fig, ax = plt.subplots(1, 1)
for k in groups.keys():
    # only plot big tracks
    if len(groups[k]) > MIN_TIMEPOINTS:
        groups[k].plot('x', 'y', ax=ax, legend=False)
        plotted += 1

    i += 1
    if (i % 100 == 0):
        print("Processed {} tracks".format(i))
    if (plotted) > MAX_TRACKS:
        print("Reached maximum number of tracks to plot ({})".format(MAX_TRACKS))
        break

plt.show()
