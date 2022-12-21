# Author: Jacob Dawson
#
# All that we're doing in this file is taking the logs in toBeProcessed and
# adding any unique stations (who have called CQ--that's important!) to the
# big file named fullLog.txt

import os

fullLog = 'fullLog.txt'
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
        station = tokenizedLines[7]
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
                log.write(newLine+'\n')
