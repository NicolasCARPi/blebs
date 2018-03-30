#!/usr/bin/env python
"""
    Read a file (Excel or CSV) with all the tracks and produce a plot of the tracks
"""
# to select the directory
from tkinter.filedialog import askopenfilename
import os.path
import pandas as pd
import matplotlib.pyplot as plt

# config
# the input file with all the tracks
#INPUT_FILE = 'tracks.xlsx'
#INPUT_FILE = 'dmso-flat-pos1.csv'
# mininum number of timepoints a track must have to be plotted
MIN_TIMEPOINTS = 30
# maximum number of tracks to plot
MAX_TRACKS = 9999999999999999
# end config

INPUT_FILE = askopenfilename()
print(INPUT_FILE)

print("Reading file")
ext = os.path.splitext(INPUT_FILE)[1]
print("Found extension", ext)
if (ext == '.csv'):
    df = pd.read_csv(INPUT_FILE)
    # for csv file
    COLUMNS_TO_DROP = ['Slice', 'Distance', 'Velocity', 'Pixel Value']
    GROUP_KEY = 'Track'
    X = 'X'
    Y = 'Y'
elif (ext == '.xlsx'):
    xl = pd.ExcelFile(INPUT_FILE)
    # for excel file
    COLUMNS_TO_DROP = ['type', 'classname', 'version', 'z', 'linklist']
    GROUP_KEY = 'id'
    X = 'x'
    Y = 'y'
    print("Parsing first sheet")
    df = xl.parse('Sheet1')
else:
    print("Extension not supported")
    raise SystemExit

print("Removing useless columns")
df = df.drop(columns=COLUMNS_TO_DROP)
print("Grouping tracks")
dfg = df.groupby([GROUP_KEY])
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
        groups[k].plot(X, Y, ax=ax, legend=False)
        plotted += 1

    i += 1
    if (i % 100 == 0):
        print("Processed {} tracks".format(i))
    if (plotted) > MAX_TRACKS:
        print("Reached maximum number of tracks to plot ({})".format(MAX_TRACKS))
        break

plt.show()
