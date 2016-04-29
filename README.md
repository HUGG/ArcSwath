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
