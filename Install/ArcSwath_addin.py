#ArcSwath
#NB 08/2014

import arcpy as ap
import pythonaddins
import math
import numpy as np
import os as os
import numpy.ma as ma
import csv
from subprocess import Popen, PIPE 

try:
    import matplotlib.pyplot as plt
    Matplotlibexists=True
except ImportError:
    print ("NO mathplotlib module found. Plot can only be NONE. CSV will be written.")
    Matplotlibexists=False

class ButtonClass9(object):
    """Implementation for SP3_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
        if Matplotlibexists == True:
            combobox_1.enabled=True
        
    def onClick(self):
        # Determining all variables from the combo/tool boxes.
        x5 = tool.x5
        y5 = tool.y5
        x6 = tool_1.x6
        y6 = tool_1.y6
        W = combobox_2.W
        if Matplotlibexists==True:
            plot = combobox_1.plot
            
        else:
            plot == 0
        
        if hasattr(combobox,'layer'):
            r_in_layer = combobox.layer
            print("r_in_layer.name: "+r_in_layer.name)
            
        if hasattr(combobox_4,'layer'):
            p_in_layer = combobox_4.layer
            print("p_in_layer.name: "+p_in_layer.name)
            
        if combobox_3.enabled:
            increment = combobox_3.increment
        if combobox_5.enabled:
            pointfeature = combobox_5.feature
        
        print("Starting process...")
        
        # Calculating geometry from the two selected points.
        
        # THIS WON'T WORK FOR A VERTICAL LINE
        deltax= x6-x5
        deltay= y6-y5
        lineslope=deltay/deltax
        
        lineangle = math.atan(lineslope)
        
        #Point 1
        x1 = x5 + math.cos(math.radians(90-math.degrees(lineangle)))*(float(W)/2.)
        y1 = y5 - math.sin(math.radians(90-math.degrees(lineangle)))*(float(W)/2.)
        #Point 2
        x2 = x6 + math.cos(math.radians(90-math.degrees(lineangle)))*(float(W)/2.)
        y2 = y6 - math.sin(math.radians(90-math.degrees(lineangle)))*(float(W)/2.)
        #Point3
        x3 = x6 - math.cos(math.radians(90-math.degrees(lineangle)))*(float(W)/2.)
        y3 = y6 + math.sin(math.radians(90-math.degrees(lineangle)))*(float(W)/2.)
        #Point4
        x4 = x5 - math.cos(math.radians(90-math.degrees(lineangle)))*(float(W)/2.)
        y4 = y5 + math.sin(math.radians(90-math.degrees(lineangle)))*(float(W)/2.)
        
        #Make a Polygon
        swathpoints = ap.Array()
        swathpoints.add(ap.Point(x1, y1))
        swathpoints.add(ap.Point(x2, y2))
        swathpoints.add(ap.Point(x3, y3))
        swathpoints.add(ap.Point(x4, y4))
        swathpoints.add(ap.Point(x1, y1))
        
        polygon = ap.Polygon(swathpoints)
        
        # Check to see if the user selected a raster layer. If not, set r_layertype to be empty.
        try:
            r_in_layer
        except NameError:
            r_layertype=""
        else:
            r_desc = ap.Describe(r_in_layer)
            r_layertype = r_desc.datasetType
   
        #print('r_layertype: ' +r_layertype)
        
        # Check to see if the user selected a point layer. If not, set p_layertype to be empty.
        try:
            p_in_layer
        except NameError:
            p_layertype=""
        else:
            p_desc = ap.Describe(p_in_layer)
            p_layertype = p_desc.datasetType
            
        #print ('point_layertype: '+p_layertype)
        
        
        if r_layertype == "RasterDataset":
            r_out_layer = r_in_layer.name[0:2] + "_swath"

            # Change to working directory
            workdir = r_in_layer.workspacePath
            ap.env.workspace = workdir
            os.chdir(workdir) 
        
            # Naming the output and checking that files with same name do not exist.
            swathnum=""
            for n in range(100):
                r_out_layer_name = r_out_layer
                if ap.Exists(r_out_layer_name):
                    swathnum=n+1
                    r_out_layer = r_in_layer.name[0:2] + "_swath" + str(swathnum)

                else:
                    break
            #This part is to deal with raster files
            
            # Clipping data from input by polygon to output
            ap.Clip_management(r_in_layer, "#", r_out_layer, polygon, "#", "ClippingGeometry")
            
            
            # set length to fit the swathprofile (constant increments)
            length= math.sqrt(((x6-x5)**2)+((y6-y5)**2))
            ninc = int(length/float(increment))
            if (np.mod(length,float(increment))>=1.0e-10):
                ninc=ninc+1
                increment=length/float(ninc)
                
            # Use new version of code to calculate LastValue
            
            # These arrays will be filled with data later on
            swathdist=np.zeros(ninc)
            swathmax=np.zeros(ninc)
            swathmean=np.zeros(ninc)
            swathmin=np.zeros(ninc)
            
            
            
            #Does not work for vertical or horital line.
            if lineslope*deltay>= 0.0 and deltax>= 0.0:
                increment = -increment            
            
            # Taking one step at a time (increment), creating arrays and finding the max, mean, min values.
            print("Calculating swath ranges...")
            for n in range(ninc):
                print("Processing row "+str(n+1)+" of "+str(ninc))
                #print n
                #PointA
                xA = x1-(n)*float(increment)*math.cos(lineangle)
                yA = y1-(n)*float(increment)*math.sin(lineangle)
                #PointB
                xB = x1-(n+1)*float(increment)*math.cos(lineangle)
                yB = y1-(n+1)*float(increment)*math.sin(lineangle)
                #PointC
                xC = x4-(n+1)*float(increment)*math.cos(lineangle)
                yC = y4-(n+1)*float(increment)*math.sin(lineangle)
                #PointD
                xD = x4-(n)*float(increment)*math.cos(lineangle)
                yD = y4-(n)*float(increment)*math.sin(lineangle)
            
                # Make the actual polygon
                clippoints = ap.Array()
                clippoints.add(ap.Point(xA, yA))
                clippoints.add(ap.Point(xB, yB))
                clippoints.add(ap.Point(xC, yC))
                clippoints.add(ap.Point(xD, yD))
                clippoints.add(ap.Point(xA, yA))
                swathpolygon = ap.Polygon(clippoints)
                
                ap.Delete_management("in_memory/swathclip")
                
                # The actual clipping

                ap.Clip_management(r_out_layer, "#", "in_memory/swathclip", swathpolygon, "#", "ClippingGeometry")
                
                #Find the NoDataValue, Use in mask(later)
                finddata = ap.Describe(r_in_layer)
                nodata = finddata.noDataValue
                
                # Convert the clipped area to Numpy Array
                swatharray = ma.MaskedArray(ap.RasterToNumPyArray("in_memory/swathclip"))
                swatharray.mask=(swatharray == nodata)#-32768)
                
                swathdist[n] = abs(increment) * n
                swathmax[n] = np.max(swatharray)
                swathmean[n] = np.mean(swatharray)
                swathmin[n] = np.min(swatharray)                

                
            # Write swath arrays to a CSV file
            swathprofile = r_in_layer.name[0:2] + "_rasterswath"+str(swathnum)+".csv"
            for n in range (100):
                if os.path.exists(swathprofile):
                    swathprofile = r_in_layer.name[0:2] + "_rasterswath"+str(swathnum)+"-"+str(n+1)+".csv"
                else:
                    break
            fileout = open(swathprofile, 'w')
            fileout.write('Point1: '+ ',' + str(x5) + ',' + str(y5) + ',' + 'Point2: '+ ',' + str(x6) + ',' + str(y6) +'\n')
            fileout.write('Distance [m], Max. Elevation [m], Mean Elevation [m], Min. Elevation [m]\n')
            for n in range(ninc):
                currentrow = '{0:.3f},{1:.3f},{2:.3f},{3:.3f}\n'.format(swathdist[n], swathmax[n], swathmean[n], swathmin[n])
                fileout.write(currentrow)
            fileout.close()
            
            
            # Test here for whether user wants to see the plot (comes from combobox in toolbar)
            # If yes call show_plot("swathplot.py")
            
            #if plot is wanted:
            if plot == 1 or plot == 3:
                fileout = open('C:\WorkSpace\plotdir.txt', 'w')
                fileout.write(r_in_layer.workspacePath+"\n")
                fileout.write(str(plot))
                fileout.close()
            
        if p_layertype == "FeatureClass":
            #This part is for pointdata/shapefiles
            p_out_layer = p_in_layer.name[0:2] + "_swath_pts"
            
            # Change to working directory
            workdir = p_in_layer.workspacePath
            ap.env.workspace = workdir
            os.chdir(workdir)
            
            # Naming the output and checking that files with same name do not exist.
            p_swathnum = ""
            for n in range(100):
                p_out_layer_name = p_out_layer+".shp"
                if ap.Exists(p_out_layer_name):
                    p_swathnum=n+1
                    p_out_layer = p_in_layer.name[0:2] + "_swath_pts" + str(p_swathnum)
                    #print(out_layer+" in loop")
                else:
                    break
            
            #Clip points which are inside the polygon
            ap.Clip_analysis(p_in_layer, polygon, p_out_layer)
            
            # Shorter term for lineslope
            k=lineslope
            
            #Works at least with shapefiles
            cutpointsfile = p_out_layer
            describe = ap.Describe(cutpointsfile)
            shapefieldname = describe.ShapeFieldName
            rows = ap.SearchCursor(cutpointsfile)
            
            pointarray = []
            print ("pointfeature: " + str(pointfeature))
            #Loop collects the values to csv-file.
            print("Finding points in swath area...")
            for row in rows:
                # Create the geometry object 'feat'
                feat = row.getValue(shapefieldname)
                pnt = feat.getPart()
                xp = pnt.X
                yp = pnt.Y
                # To change the data, check the name of the field from table
                data = row.getValue(pointfeature)
                xx = (xp +((k**2)*x5)+(yp*k)-(y5*k))/(k**2+1)
                yx = k*(xx-x5)+y5
                d = math.sqrt((xx-x5)**2+(yx-y5)**2)
                pointarray.append([d, data, xx, yx])
            
            # Write results into CSV file
            pointdatafile = p_in_layer.name[0:2] + "_pointswath"+str(p_swathnum)+".csv"
            for n in range(100):
                if os.path.exists(pointdatafile):
                    pointdatafile = p_in_layer.name[0:2] + "_pointswath"+str(p_swathnum)+"-"+str(n+1)+".csv"
                else:
                    break
            openpointdata = open(pointdatafile, 'w')
            openpointdata.write('Point1: '+ ',' + str(x5) + ',' + str(y5) + ',' + 'Point2: '+ ',' + str(x6) + ',' + str(y6) +'\n')
            openpointdata.write('Distance [m],' + str(pointfeature) + "," + 'X-coordinate, Y-coordinate\n')
            for n in pointarray:
                datarow = str(n[0])+","+str(n[1])+","+str(n[2])+","+str(n[3])+"\n"
                openpointdata.write(datarow)
            openpointdata.close()
            
            #Plotting pointdata
            if plot == 2 or plot == 3:
                pointout = open('C:\WorkSpace\plotpointdir.txt', 'w')
                pointout.write(p_in_layer.workspacePath+"\n")
                pointout.write(str(plot))
                pointout.close()
        
        # Plot the right way
        if plot == 2:
            fileout = open('C:\WorkSpace\plotdir.txt', 'w')
            fileout.write("\n"+str(plot))
            fileout.close()
        
        
        if plot == 1:
            pointout = open('C:\WorkSpace\plotpointdir.txt', 'w')
            pointout.write("\n"+str(plot))
            pointout.close()
                
        if plot != 0:

            show_plot("swathplot.py")
        
        
class ComboBoxClass5(object):
    """Implementation for SP3_addin.combobox (ComboBox)"""
    def __init__(self):
        self.editable = True
        self.enabled = True
        self.value = 'None'

    def onSelChange(self, selection):
        # When a new layer is selected diipa daapa
        if selection == 'None':
            del self.layer
            if 'Points' in combobox_1.items and Matplotlibexists:
                combobox_1.items=['None','Points']
            combobox_3.enabled = False
        else:
            self.layer = ap.mapping.ListLayers(self.mxd, selection)[0]
            combobox_3.enabled = True
            if Matplotlibexists:
                if 'Points' in combobox_1.items:
                    combobox_1.items=['None','Raster','Points','Raster+Points']
                else:
                    combobox_1.items=['None','Raster']
            
            # Error if not in UTM
            r_desc = ap.Describe(selection)
            r_spatialref = r_desc.spatialReference
            if "UTM" not in r_spatialref.name:
                print ('***ERROR***')
                print ('Input raster file is not in metric UTM coordinate system. Use UTM coordinate system.')
                button.enabled = False
  
            else:
                button.enabled = True

        ap.RefreshActiveView()
    def onEditChange(self, text):
        pass
    def onFocus(self, focused):
        #When the combo box has focus, update the combo box with the list of layer names.
        if focused:
            self.mxd = ap.mapping.MapDocument('current')
            layers = ap.mapping.ListLayers(self.mxd)
            self.items = ['None']
            for layer in layers:
                self.items.append(layer.name)
    def onEnter(self):
        pass
    def refresh(self):
        pass
        
class ComboBoxClass39(object):
    """Implementation for SP3_addin.combobox_4 (ComboBox)"""
    def __init__(self):
        self.editable = True
        self.enabled = True
        self.value = 'None'

    def onSelChange(self, selection):
        # When a new layer is selected

        #Different from the combobox 5 and has a "good" bug
        if selection == 'None':
            del self.layer
            if Matplotlibexists==True:
                if 'Raster' in combobox_1.items:
                    combobox_1.items=['None','Raster']
                else:
                    combobox_1.items=['None']
            combobox_5.enabled = False
        else:
            self.layer = ap.mapping.ListLayers(self.mxd, selection)[0]
            combobox_5.enabled = True
            if Matplotlibexists:
                if 'Raster' in combobox_1.items:
                    combobox_1.items=['None','Raster','Points','Raster+Points']
                else:
                    combobox_1.items=['None','Points']
            p_desc = ap.Describe(selection)
            p_spatialref = p_desc.spatialReference
            if "UTM" not in p_spatialref.name:
                print ('***ERROR***')
                print ('Input point file is not in metric UTM coordinate system. Use UTM coordinate system.')
                button.enabled = False

            else:
                button.enabled = True
        ap.RefreshActiveView()
    def onEditChange(self, text):
        pass
    def onFocus(self, focused):
        #When the combo box has focus, update the combo box with the list of layer names.
        if focused:
            self.mxd = ap.mapping.MapDocument('current')
            layers = ap.mapping.ListLayers(self.mxd)
            self.items = ['None']
            for layer in layers:
                self.items.append(layer.name)
    def onEnter(self):
        pass
    def refresh(self):
        pass
        
class ComboBoxClass3(object):
    """Implementation for SP_addin.combobox_5 (ComboBox)"""
    def __init__(self):
        self.editable = True
        self.enabled = False
    def onSelChange(self, selection):
        self.feature = selection
    def onEditChange(self, text):
        pass
    def onFocus(self, focused):
        # update combobox with point fieds
        pfields = ap.Describe(combobox_4.layer).fields
        self.items = []
        for f in pfields:
            self.items.append(f.baseName)
    def onEnter(self):
        pass
    def refresh(self):
        pass
  
class ComboBoxClass6(object):
    """Implementation for SP3_addin.combobox_1 (ComboBox)"""
    def __init__(self):
        self.editable = True
        self.enabled = False
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWW'
    def onSelChange(self, selection):
        if selection == "Raster":
            self.plot=1
        elif selection == "Points":
            self.plot=2
        elif selection == "Raster+Points":
            self.plot=3
        elif selection == "None":
            self.plot=0
    def onEditChange(self, text):
        pass
    def onFocus(self, focused):
        pass
    def onEnter(self):
        pass
    def refresh(self):
        pass

class ComboBoxClass7(object):
    """Implementation for SP3_addin.combobox_2 (ComboBox)"""
    def __init__(self):
        self.items = [1000, 5000, 10000, 20000]
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWW'
    def onSelChange(self, selection):
        self.W = selection
    def onEditChange(self, text):
        self.W = text
    def onFocus(self, focused):
        pass
    def onEnter(self):
        pass
    def refresh(self):
        pass

class ComboBoxClass8(object):
    """Implementation for SP3_addin.combobox_3 (ComboBox)"""
    def __init__(self):
        self.items = [180, 360, 720, 1080, 1440, 1800]
        self.editable = True
        self.enabled = False
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWW'
    def onSelChange(self, selection):
        self.increment = selection
    def onEditChange(self, text):
        self.increment = text
    def onFocus(self, focused):
        pass
    def onEnter(self):
        pass
    def refresh(self):
        pass

class ToolClass2(object):
    """Implementation for SP3_addin.tool (Tool)"""
    def __init__(self):
        self.enabled = True
        self.shape = "NONE" # Can set to "Line", "Circle" or "Rectangle" for interactive shape drawing and to activate the onLine/Polygon/Circle event sinks.
        self.cursor = 3 # Use crosshairs
        
    def onMouseDownMap(self, x, y, button, shift):
        self.x5 = x
        self.y5 = y
        print "Point 1: "+str(x)+","+str(y)
        
class ToolClass4(object):
    """Implementation for SP3_addin.tool_1 (Tool)"""
    def __init__(self):
        self.enabled = True
        self.shape = "NONE" # Can set to "Line", "Circle" or "Rectangle" for interactive shape drawing and to activate the onLine/Polygon/Circle event sinks.
        self.cursor = 3 # Use crosshairs
    def onMouseDownMap(self, x, y, button, shift):
        self.x6 = x
        self.y6 = y
        print "Point 2: "+str(x)+","+str(y)

def show_plot(file_name):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)  
    proc = Popen(file_path, shell=True, stdout=PIPE, bufsize=1)  
    stdoutdata, stderrdata = proc.communicate()  
    return stdoutdata  