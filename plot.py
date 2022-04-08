"""Load CSV and draw diagram."""

import argparse
import numpy as np
from dateutil import parser
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

argParser = argparse.ArgumentParser(description='Plot CSV file')
argParser.add_argument('csvPath', metavar='CSV_PATH', type=str,
                       help='Path to the CSV file')
argParser.add_argument('outputPath', metavar='IMAGE_PATH', type=str,
                       help='Output path for image')
argParser.add_argument('--title', dest='title', type=str, default=None,
                       help='title for the graph')

args = argParser.parse_args()

x = np.array([])
y = np.array([])

path = args.csvPath
outPath = args.outputPath
title = args.title
with open(path) as f:
    line = f.readline()
    time, value = line.split(', ')
    value = float(value)

    startTime = parser.parse(time)
    x = np.append(x, 0)
    y = np.append(y, value)

    while line:
        line = f.readline()
        if line != "":
            time, value = line.split(', ')
            time = parser.parse(time)
            diff = round((time - startTime).total_seconds(), 2)
            value = float(value)

            x = np.append(x, diff)
            y = np.append(y, value)

yhat = savgol_filter(y, 333, 1)

plt.grid(axis='x', color='0.95')
plt.grid(axis='y', color='0.95')
plt.plot(x, yhat)
plt.xlim(xmin=0)
plt.ylim(ymin=y.min())
plt.xlabel("Seconds")
plt.ylabel("Volt")

if title:
    plt.title(title)

plt.savefig(outPath)
