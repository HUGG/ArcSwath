# Swathplot.py
# Plots swath profile data from arcmap tool.
# NB 08/2014

import matplotlib.pyplot as plt
import glob
import numpy as np
import os

def main():
    # Finding correct rasterfile
    filein = open('C:\WorkSpace\plotdir.txt', 'r')
    plotinfo = filein.read().splitlines()
    mydir = plotinfo[0]
    plottype = int(plotinfo[1])
    filein.close()
    #print (mydir)
    #print (plottype)
    
    # Finding correct shapefile
    pointin = open('C:\WorkSpace\plotpointdir.txt', 'r')
    pointinfo = pointin.read().splitlines()
    mypointdir = pointinfo[0]
    pointplottype = int(pointinfo[1])
    pointin.close()
    
    #mydir = combobox.layer.workspacePath
    #mydir = "C:\GIS\ArcGIS\grids\Bolivia"
    
    #Plotting raster data
    if plottype == 1 or plottype == 3:
        os.chdir(mydir)
        # Finding the latest raster file that have been worked on.
        myraster = filter(os.path.isfile, glob.glob(mydir + "\*rasterswath*.csv"))
        myraster.sort(key=lambda x: os.path.getmtime(x))
        
        #print("My raster:")
        #print(myraster)
        #print("My directory:")
        #print(mydir)
        
        # Open file
        reader = open(myraster[-1],"r")
        # Read header line
        headerline = reader.readline()
        headerline = reader.readline()
        # Read all lines using readlines()
        contents = reader.readlines()
        # Make arrays for each variable
        swathdist = np.zeros(len(contents))
        swathmax = np.zeros(len(contents))
        swathmean = np.zeros(len(contents))
        swathmin = np.zeros(len(contents))
        
        linecount = 0
        # Loop over all lines in readlines, split line by ",", store each variable in splitline list in right spot in array
        for line in contents:
            splitline = line.split(',')
            swathdist[linecount] = splitline[0]
            swathmax[linecount] = splitline[1]
            swathmean[linecount] = splitline[2]
            swathmin[linecount] = splitline[3]
            linecount = linecount + 1
        
        #plot the array
        #plt.plot(swatharray)
        # x = width * listnumber
        # y = altitude(max, min, mean)
        #plt.scatter((width * 5), np.min(swalist[5]), color="blue", label='line1', linewidth=2)
        #plt.scatter((width * 6), np.min(swalist[6]), color="red", label='line1', linewidth=2)
        #plt.scatter((width * 7), np.min(swalist[7]), color="yellow", label='line1', linewidth=2)
        #plt.scatter((width * 8), np.min(swalist[8]), color="purple", label='line1', linewidth=2)
        #swathdist=np.zeros(len(swalist))
        #swathmax=np.zeros(len(swalist))
        #swathmean=np.zeros(len(swalist))
        ##swathmin=np.zeros(len(swalist))
        #for n in range(0, int(LastValue)):
            #plt.scatter(width * n, np.max(swalist[n]), color="blue")
            #plt.scatter(width * n, np.mean(swalist[n]), color="green")
            #plt.scatter(width * n, np.min(swalist[n]), color="red")
            #swathdist[n] = width * n
            #swathmax[n] = np.max(swalist[n])
            #swathmean[n] = np.mean(swalist[n])
            #swathmin[n] = np.min(swalist[n])
            
        # Convert swathdist to km
        swathdist=swathdist/1000.0
        
        fig, ax1 = plt.subplots()
        ax1.plot(swathdist, swathmax, "r", label="Maximum")
        ax1.plot(swathdist, swathmean, "k", linewidth=2, label="Mean")
        ax1.plot(swathdist, swathmin, "b", label="Minimum")
        ax1.fill_between(swathdist, swathmax, swathmin, color='grey', alpha=0.25 )
        
        ax1.set_xlabel("Distance along profile (km)")
        ax1.set_ylabel("Elevation (m)")
        
        # ax2 = ax1.twinx()
        # t = np.arange(0.01, 10.0, 0.01)
        # s = np.sin(2*np.pi*t)
        # ax2.plot(t, s, 'r.')
        # ax2.set_label('exp')
        
        # plt.plot(swathdist, swathmax, "r", label="Maximum")
        # plt.plot(swathdist, swathmean, "k", linewidth=2, label="Mean")
        # plt.plot(swathdist, swathmin, "b", label="Minimum")
        # plt.fill_between(swathdist, swathmin, "b", label="Minimum")
        
        # plt.xlabel("Distance along profile (km)")
        # plt.ylabel("Elevation (m)")
    
    # Plotting shapefile data
    if pointplottype == 2 or pointplottype == 3:
        os.chdir = (mypointdir)
        # Find the latest shapefile that have been worked on.
        mypoints = filter(os.path.isfile, glob.glob(mypointdir + "\*pointswath*.csv"))
        mypoints.sort(key=lambda x: os.path.getmtime(x))
        
        
        #SPLIT IN TWO CASES: RASTER+POINT AND JUST POINTS
        #print("My poits:")
        #print(mypoints)
        # Open file
        reader = open(mypoints[-1],"r")
        # Read header line
        headerline = reader.readline()
        headerline = reader.readline()

        splitheaderline = headerline.split(',')
        pointfeatheader = splitheaderline[1]
        print (pointfeatheader)
        # splitheaderline2 = line.split(',')
        # disthead[headerline2] = splitheaderline2[0]
        # pointfeathead[headerline2] = splitheaderline2[1]
        # print (pointfeathead)
        #xhead = splitheaderline2[2]
        #yhead = splitheaderline2[3]
        
        # Read all lines using readlines()
        contents = reader.readlines()
        # Make array for each variable
        distance = np.zeros(len(contents))
        variable = np.zeros(len(contents))
        xcoord = np.zeros(len(contents))
        ycoord = np.zeros(len(contents))
        
        linecount = 0
        # Loop over all lines in readlines, split line by ",", store each variable in splitline list in right spot in array
        for line in contents:
            splitline = line.split(',')
            distance[linecount] = splitline[0]
            variable[linecount] = splitline[1]
            xcoord[linecount] = splitline[2]
            ycoord[linecount] = splitline[3]
            linecount = linecount + 1
        # Convert distance from m to km
        distance = distance/1000.0
        # Only points
        if pointplottype == 2:
            
            plt.plot(distance, variable, "ro")
            plt.xlabel("Distance along profile (km)")
            plt.ylabel(pointfeatheader)
            # ax1 = plt.subplots()
            # ax1.plot(distance, )
            # ax2 = plt.twinx()
            # ax2.plot(erorate, "rs")
        
            #plt.plot(distance, erorate, "rs")
            #plt.twinx()
        # If plottinf both raster and shapefile.
        if pointplottype == 3:
            ax2 = ax1.twinx()
            #t = np.arange(0.01, 10.0, 0.01)
            #s = np.sin(2*np.pi*t)
            ax2.plot(distance, variable, 'ro')
            ax2.set_ylabel(pointfeatheader)
            #plt.y2label("Erosionrate (mm/a)")
            
            #ax2 = ax1.twinx()
            # plt.plot.twinx(distance,erorate, "rs")
            #plt.twinx.ylabel("Erosionrate (mm/a)", color='r')
        
    plt.legend()
    plt.grid()
    
        #plt.show()
    #plt.imshow(swatharray)
    #plt.gray()
    plt.show()
        
main()
