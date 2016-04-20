#Swathpointplot.py
#This hopefully will plot point data
#NB 11/14

import matplotlib.pyplot as plt
import glob
import numpy as np
import os

def main():
    filein = open('C:\WorkSpace\plotdir.txt', 'r')
    mydir = filein.read()
    filein.close()
    print (mydir)
    #mydir = combobox.layer.workspacePath
    #mydir = "C:\GIS\ArcGIS\grids\Bolivia"
    os.chdir(mydir)
    myfiles = filter(os.path.isfile, glob.glob(mydir + "\*.csv"))
    myfiles.sort(key=lambda x: os.path.getmtime(x))
    
    # Open file
    reader = open(myfiles[-1],"r")
    # Read header line
    headerline = reader.readline()
    # Read all lines using readlines()
    contents = reader.readlines()
    # Make array for each variable
    distance = np.zeros(len(contents))
    erorate = np.zeros(len(contents))
    xcoord = np.zeros(len(contents))
    ycoord = np.zeros(len(contents))
    
    linecount = 0
    # Loop over all lines in readlines, split line by ",", store each variable in splitline list in right spot in array
    for line in contents:
        splitline = line.split(',')
        distance[linecount] = splitline[0]
        erorate[linecount] = splitline[1]
        xcoord[linecount] = splitline[2]
        ycoord[linecount] = splitline[3]
        linecount = linecount + 1
    
    # Convert distance from m to km
    distance = distance/1000.0
    
    ax1 = plt.subplots()
    ax1.plot()
    ax2 = plt.twinx()
    ax2.plot(erorate, "rs")
    
    #plt.plot(distance, erorate, "rs")
    #plt.twinx()
    plt.show()
    
main()