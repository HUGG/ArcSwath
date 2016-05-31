# ArcSwath
An efficient swath profile analysis tool for ArcGIS 10.2 and later.

## Installation

1. Download the ArcSwath files
2. Double click on makeaddin.py
3. Double click on ArcSwath.esriaddin -> click Install Add-In
4. Create to your C: drive a folder named WorkSpace (This is done for the plotting)

## Preparing your data

- UTM coordinates are required for the geometrical calculation that are used in the code.
- Pixel Type should be signed integer. Conversion can be executed with Int tool in spatial analyst.
- For some data (SRTM): you may want to convert near sea level values according to the following link: [convert near sea level values] ( http://mappingcenter.esri.com/index.cfm?fa=ask.answers&q=1686.).
- Follow the noData value - should be defined to something.

## Using ArcSwath
![ArcSwath toolbar] (Images/ArcSwathtoolbar.JPG) <br/>
*ArcSwath toolbar*
* 1. Select input raster. The list is same as your Table of Contents. Use only raster files.
* 2. Select input point file. The list is same as your Table of Contents. Use point data.
* 3. In point feature you can select the data from Attribute Table.
* 4. Select what data you want to plot with matplotlib library. The tool will check if you have matplotlib. Also a csv file will be written.
* 5. Select the starting and end point by clicking the map.*
* 6. How wide your swath profile will be (in meters). Type in or select from the drop-down list.
* 7. The increment sets how often (in meters) minimum, mean and maximum values are calculated along profile lenght.
* 8. Click and your swath profile will be extracted.

## How does ArcSwath work?

After you click Calculate: <br/>
1. The script calculates 4 points for a rectangle according to the two points (Point 1 and 2) you clicked and the width you defined. Then it creates a polygon of the points.
2. The code checks that your input raster is really a raster layer and the same for the input point data.
3. The code names and defines working directory for the raster layer.
4. The polygon is used to exract raster layer. Then smaller boxes according to increment are extracted inside the previously extracted raster layer. Minimum, mean and maximum values are the added to arrays and written into a csv file.
5. Then the plotting for raster file is defined.
6. First for the point files naming and working directory is defined.
7. The points are clipped inside the polygon which was created in the end of step 1.
8. Then the points are calculated to fit a line going trough the points 1 and 2. For each point the distance to the point 1 is calculated and the dataa is written to a csv file.
9. Plotting for points is defined.
10. The entire plotting is then defined.

