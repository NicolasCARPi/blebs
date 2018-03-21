#!/usr/bin/env python
"""
    Read an excel file with all the tracks and produce a plot of the tracks
"""
import pandas as pd
import matplotlib.pyplot as plt

# config
EXCEL_FILE = 'tracks.xlsx'
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

i = 0
# plot all on same figure
fig, ax = plt.subplots(1, 1)
for k in groups.keys():
    groups[k].plot('x', 'y', ax=ax, legend=False)
    i += 1
    if (i % 100 == 0):
        print("Processed {} tracks".format(i))
    #if (i) > 4000:
    #    print("Stopping")
    #    break


plt.show()
