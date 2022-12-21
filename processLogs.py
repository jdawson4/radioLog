# Author: Jacob Dawson
#
# All that we're doing in this file is taking the logs in toBeProcessed and
# adding any unique stations (who have called CQ--that's important!) to the
# big file named fullLog.txt

import os
import sys
import pandas as pd
import plotly.express as pl

fullLog = 'fullLog.txt'

def locator_to_latlong(locator):
    # Found this in a python repo called "pyhamtools"
    locator = locator.upper()
    if len(locator) == 5 or len(locator) < 4:
        raise ValueError
    if ord(locator[0]) > ord('R') or ord(locator[0]) < ord('A'):
        raise ValueError
    if ord(locator[1]) > ord('R') or ord(locator[1]) < ord('A'):
        print(locator)
        raise ValueError
    if ord(locator[2]) > ord('9') or ord(locator[2]) < ord('0'):
        raise ValueError
    if ord(locator[3]) > ord('9') or ord(locator[3]) < ord('0'):
        raise ValueError
    if len(locator) == 6:
        if ord(locator[4]) > ord('X') or ord(locator[4]) < ord('A'):
            raise ValueError
        if ord (locator[5]) > ord('X') or ord(locator[5]) < ord('A'):
            raise ValueError
    longitude = (ord(locator[0]) - ord('A')) * 20 - 180
    latitude = (ord(locator[1]) - ord('A')) * 10 - 90
    longitude += (ord(locator[2]) - ord('0')) * 2
    latitude += (ord(locator[3]) - ord('0'))
    if len(locator) == 6:
        longitude += ((ord(locator[4])) - ord('A')) * (2 / 24)
        latitude += ((ord(locator[5])) - ord('A')) * (1 / 24)
        # move to center of subsquare
        longitude += 1 / 24
        latitude += 0.5 / 24
    else:
        # move to center of square
        longitude += 1;
        latitude += 0.5;
    return latitude, longitude


def plot():
    uniqueGridLocations = []
    with open(fullLog) as file:
        lines = file.readlines()[1:]
        for line in lines:
            tokenizedLines = line.split()
            # check for weirdness: we should have exactly 10 tokens
            if len(tokenizedLines) != 10:
                continue
            if tokenizedLines[3] != 'FT8':
                continue
            gridLocation = tokenizedLines[9]
            if gridLocation not in uniqueGridLocations:
                if len(gridLocation) == 4:
                    uniqueGridLocations.append(gridLocation)
    # uniqueGridLocations is now a list of *all* unique grid locations.
    # we simply want to convert those to latlongs now:
    df = pd.DataFrame([{'lat': x, 'lon': y} for x,y in [locator_to_latlong(pos) for pos in uniqueGridLocations]])
    #print(df)

    # and show the plot:
    plot = pl.scatter_geo(df, lat="lat", lon="lon")
    plot.show()

def record():
    directory = 'toBeProcessed'

    if not os.path.isfile('fullLog.txt'):
        with open(fullLog, 'a') as log:
            log.write('All Recorded FT8 CQs:\n')

    # first we need to figure out which stations we've already logged
    uniqueStations = []
    with open(fullLog) as file:
        lines = file.readlines()[1:]
        for line in lines:
            tokenizedLines = line.split()
            if tokenizedLines[3]!='FT8':
                continue
            station = tokenizedLines[8]
            if station not in uniqueStations:
                uniqueStations.append(station)

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            print('Processing', f)
            with open(f) as file:
                lines = file.readlines()
            for line in lines:
                #print(line, end='')
                tokenizedLines = line.split()
                #print(tokenizedLines)

                # check for weirdness: we should have exactly 10 tokens
                if len(tokenizedLines) != 10:
                    continue

                # note: we only want FT8 signals:
                if tokenizedLines[3]!='FT8':
                    continue
                # we also want to ignore things that aren't CQs, because only CQ
                # calls will contain location information:
                if tokenizedLines[7]!='CQ':
                    continue
                station = tokenizedLines[8]
                # we also want to ignore stations we've already logged:
                if station in uniqueStations:
                    continue
                else:
                    uniqueStations.append(station)
                
                # now we only have unique FT8 CQ calls.
                # we'll append these to our fullLog.txt
                with open(fullLog, 'a') as log:
                    newLine = ""
                    for t in tokenizedLines:
                        newLine += t + " "
                    log.write(newLine[:-1]+'\n')

if __name__=="__main__":
    record()

    # include a "t" somewhere in your first command line arg in order to
    # see a plot of heard cq's!
    if len(sys.argv) > 1:
        if ('t' in sys.argv[1].lower()):
            pass # we want to plot things on a map in this case!
            print("Plotting points")
            plot()
