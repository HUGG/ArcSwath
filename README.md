# ArcSwath
An efficient swath profile analysis tool for ArcGIS 10.2 and later.

## Installation
### The easy way (try this first)

1. Download the [`ArcSwath Add-In`](ArcSwath-git.esriaddin).
2. Double click on the `ArcSwath-git.esriaddin` file after it downloads and click **Install Add-In**.
3. Create a directory `C:\WorkSpace` if it does not already exist. This is needed for plotting to work.

### The slightly harder way (if the easy way doesn't work)
1. Download all of the ArcSwath files by clicking on the **Clone or download** button on the top right and then **Download ZIP**.
2. Unzip the files and double click on the `makeaddin.py` file.
3. Double click on the `ArcSwath-git.esriaddin` file and click **Install Add-In**.
4. Create a directory `C:\WorkSpace` if it does not already exist. This is needed for plotting to work.

## Preparing your data
There are a few data requirements needed for the ArcSwath tool to work properly. To ensure proper functioning of the tool, please make sure your data meet the following criteria:

- Point and raster data should be projected in UTM coordinates. This is required for the geometrical calculations that are used in the code.
- The **Pixel Type** for raster files should be signed integer. Conversion can be done using the **Int** tool in Spatial Analyst.
- For [SRTM data](http://www.cgiar-csi.org/data/srtm-90m-digital-elevation-database-v4-1) you may want to [process the data to adjust near sea level values](http://mappingcenter.esri.com/index.cfm?fa=ask.answers&q=1686).
- The noData value for raster data must be defined. If undefined, a value can be set in **ArcCatalog**.

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
1. The script calculates 4 points for a rectangle according to the two points (Point 1 and 2) you clicked and the width you defined. Then it creates a polygon of the points. <br/>
2. The code checks that your input raster is really a raster layer and the same for the input point data. <br/>
3. The code names and defines working directory for the raster layer. <br/>
4. The polygon is used to exract raster layer. Then smaller boxes according to increment are extracted inside the previously extracted raster layer. Minimum, mean and maximum values are the added to arrays and written into a csv file. <br/>
5. Then the plotting for raster file is defined. <br/>
6. First for the point files naming and working directory is defined. <br/>
7. The points are clipped inside the polygon which was created in the end of step 1. <br/>
8. Then the points are calculated to fit a line going trough the points 1 and 2. For each point the distance to the point 1 is calculated and the dataa is written to a csv file. <br/>
9. Plotting for points is defined. <br/>
10. The entire plotting is then defined. <br/>

