#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This script creates a weed map using several ArcGIS tools and a bit of Image Processing. 
# It is based on the concept of Fishnet Grid and Thresholding technique. 
# Prerequisites before using this algorithm/script:
# 1. Imagery should be provided by the user. Either it should be RGB imagery or Multispectral. Several Indices can be 
# calculated and exported in local drive bsaed on the imagery type provided
# 2. Shapefile (a polygon line drawn over the crop rows) should be provided by the user.
# Limitation of this algorithm: Weeds won't get detected or identified if they are present in-between crop rows
# Original workflow in ArcGIS was developed by Dr. J. Paulo Flores (Assistant Prof. at NDSU)
# Automation using Python scripting was developed by Nitin Rai (PhD Student)
# Agricultural Engineering, Precision Agriculture
# North Dakota State University, USA
#################### Script starts here ########################################################################
################################################################################################################

# Importing packages
import numpy as np
import arcpy # from ArcGIS 
import os
import sys
from arcpy.ia import * # Image Analyst
from arcpy.sa import * # Spatial Analyst
from arcpy import env 
from arcpy.sa import Raster, Float
import rasterio # Working with Raster Dataset
import gdal # Geospatial Data Abstraction Library
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import copy
# Reading the imagery (can be .jpg or .png too) from the local HD
RGB_imagery = r"E:/Nitin.Rai/ForPythonScripting/Sunf_AOI_Lab7_2021.tif"
raster = rasterio.open(RGB_imagery)
bands = [Raster(os.path.join(RGB_imagery, b))
         for b in arcpy.ListRasters()]
# counting number of bands within the loaded raster file
arcpy.env.workspace = RGB_imagery
band_count = raster.count
print(band_count)
# User can list all the raster files present within the working directory and print it
#raster_list = arcpy.ListRasters("*")
#print (raster_list)
# Extra information about the raster data loaded
#raster.width
#raster.height
#raster.meta
# Extracting bands from the loaded raster data 
# Setting up the working directory
# print(band_count)
# Another way to open raster file
# Excess = r'C:\Users\nitin.rai\Desktop\ArcGIS Pro\PAG654LABS\Lab7\Lab_Practice\Sunf_ExGr_AOI_Lab7.tif'
# raster_dataset = gdal.Open(Excess)
# env.outputCoordinateSystem = arcpy.SpatialReference("WGS_1984_UTM_Zone_14N")
#################### Additional features in this script/algorithm #############################
###############################################################################################
# Here the operation is dependent on band count. If the band count is equal to 5 then the script assumes it's a 5-band imagery
# and starts calculating all the indices. More indices can be added to the workflow. Whereas, if the band count is greater than
# 5, then an error message is displayed asking user to enter an imagery which is either 3-band or 5-band.
# If the band count is equal equal to 3 or 4, then Excess Green is automatically calculated and stored to the HDD.
# As in array function, the index starts from 0 onwards.
# # For a multispectral imagery (RedEdge MicaSense), 0  = Blue band, 1 = green, 2 = red, 3 = RedEdge, 4 = NIR
if band_count > 5:
    print("Input Imagery should be 3-band RGB Imagery or 5-band Multispectral Imagery")
elif band_count == 5:
    path = os.path.dirname(imagery)
    base1 = os.path.basename(imagery)
    base = os.path.splitext(base1)[0]
    ndvi_filename = base + "_NDVI.tif"
    ndre_filename = base + "_NDRE.tif"
    savi_filename = base + "_SAVI.tif"
    osavi_filename = base + "_OSAVI.tif"
    arcpy.env.workspace = imagery
    ndvi = (Float(bands[4]) - bands[2]) / (Float(bands[4]) + bands[2]) 
    ndvi.save(ndvi_filename)
    print ("NDVI successfully calculated")
    ndre = (Float(bands[4]) - bands[3]) / (Float(bands[4]) + bands[3]) 
    ndre.save(ndre_filename)
    print ("NDRE successfully calculated")
    savi = 1.5 * ((Float(bands[4]) - bands[2]) / (Float(bands[4]) + bands[2] + 0.5))
    savi.save(savi_filename)
    print ("SAVI successfully calculated")
    osavi = 1.16 * ((Float(bands[4]) - bands[2]) / (Float(bands[4]) + bands[2] + 0.16))
    osavi.save(osavi_filename)
    print ("OSAVI successfully calculated")
else:
    path = os.path.dirname(RGB_imagery)
    base1 = os.path.basename(RGB_imagery)
    base = os.path.splitext(base1)[0]
    ExGreen_filename = base + "_ExcessGreen.tif"
    total_bands = (Float(bands[0] + bands[1] + bands[2]))
    red_band = (Float(bands[2]) / total_bands)
    green_band = (Float(bands[1]) / total_bands)
    blue_band = (Float(bands[0]) / total_bands)
    ExGreen = (2 * green_band - red_band - blue_band)
    ExGreen.save(ExGreen_filename)
    arcpy.env.workspace = path
    print ("You have successfully exported the Excess Green.tif file")
    arcpy.BuildPyramids_management(ExGreen_filename, "", "NONE", "BILINEAR","", "", "")
    print ("Excess Green pyramids successfully calculated")
    # Sharpening the image so the objects (crops & weeds) details are highlighted
sharpen_ExGreen = arcpy.ia.Convolution(ExGreen, 20)
sharpen_ExGreen.save(r'E:/Nitin.Rai/ForPythonScripting/ExGreen_Sharpened.tif')
print("You have successfully sharpened the Excess Green.tif file!")
# Converting the above sharpened image into binary image, thresholding technique is applied here 
# converting the imagery into 0 and 1.
binary_raster = arcpy.ia.Threshold(sharpen_ExGreen)
binary_raster.save(r"E:/Nitin.Rai/ForPythonScripting/ThresholdSharpen.tif")
print("You have successfully perfromed Imagery Thresholding!")
# reclassify the raster
# reclassField = "Value"
# remap = RemapValue([[0, 1], [1, 2], ["NODATA", "NODATA"]])
# outReclassify = Reclassify(RGB_imagery, reclassField, remap, "NODATA")
# outReclassify.save(r"D:\Datasets\ReclassifiesImagery.tif")
# Converting Raster to Polygon (a shapefile is generated for the whole raster file)
# objects within the raster file is 1s while all the rest is 0s
arcpy.env.workspace = 'E:/Nitin.Rai/ForPythonScripting'
inRaster = "ThresholdSharpen.tif"
outPolygons = r"E:/Nitin.Rai/ForPythonScripting/RasterToPolygonConvert.shp"
field = "VALUE"
arcpy.RasterToPolygon_conversion(inRaster, outPolygons, "NO_SIMPLIFY", field)
print("You have successfully converted Raster to Polygon!")
# Selecting all the 1s so that we can export a shapefile for all the objects labeled 1s within the imagery
arcpy.env.workspace = r'E:/Nitin.Rai/DatasetForPythonScripting'
polygonAttached = "RasterToPolygonConvert.shp"
selectedAttributes = arcpy.SelectLayerByAttribute_management(polygonAttached, "NEW_SELECTION", '"gridcode" > 0')
arcpy.CopyFeatures_management(selectedAttributes, 'Attributes_SelectedGridOne')
# At this step, user provides a line shpaefile denoting crop rows.
arcpy.env.workspace = r'E:/Nitin.Rai/DatasetForPythonScripting'
cropsline = "PAG_Sunf_rows.shp"
rowsBuffered = r'E:/Nitin.Rai/DatasetForPythonScripting/ROI_Buffered3Inches'
# Specifying buffer of 3 inches using the line shapefile provided by the user
distanceField = "3 Inches"
sideType = "FULL"
endType = "FLAT"
dissolve = "NONE"
# Finally storing the buffer shapefile in Buffered_CropsLine
Buffered_CropsLine = arcpy.Buffer_analysis(cropsline, rowsBuffered, distanceField, sideType, endType, dissolve)
# # Erasing all the required crop rows
# arcpy.Erase_analysis(outPolygons, 
#                      r'D:\PAG654\Lab7\PAG454_AOI_RowsBuffered.shp', 
#                      r'D:\PAG654\Lab7\ErasedOutputAlgo')
# Erase the polygon layer with the buffered layer
# Setting the workspace in every step
arcpy.env.workspace = r'E:/Nitin.Rai/DatasetForPythonScripting'
# Reading the shapefile which has ll the 1s (basically crops and weeds)
polygon = "Attributes_SelectedGridOne.shp"
# Using Buffer shapefile as an erase feature
eraseFeature = "ROI_Buffered3Inches.shp"
# Saving it for further application
ErasedLayer = r'E:/Nitin.Rai/DatasetForPythonScripting/ErasedPolygonLayerFinal.shp'
arcpy.Erase_analysis(polygon, eraseFeature, ErasedLayer)
# Creating a Fishnet Tool
env.workspace = r'E:\Nitin.Rai\DatasetForPythonScripting'
# This step is very important. It will create a Fishnet with the same coordinate and projected information. We can specify this
# at the beginning of this script too so that all the created shapefiles are of same coordinate and projected information 
# env.outputCoordinateSystem = arcpy.SpatialReference("WGS_1984_UTM_Zone_14N")
# Setting up all the parameters required to create a Fishnet tool. At this step, origin coordinates, y axis coordinates, 
# and opposite corner options are all provided by the user 
outFeatureClass = "fishnet_10x10.shp"
origin_coordinate = '491218.69307 5263121.21232'
yAxisCoordinate = '491218.69307 5263125.21232'
CellWidth = '0.3'
CellHeight = '0.3'
numRows = '0'
numCols = '0'
oppositeCorner = '491229.23675 5263129.25616'
labels = "NO_LABELS"
templateExtent = '#'
geometryType = 'POLYGON'
arcpy.CreateFishnet_management(outFeatureClass, origin_coordinate, yAxisCoordinate, CellWidth, 
                               CellHeight, numRows, numCols, oppositeCorner,
                               labels, templateExtent, geometryType)
# add a field to the created fishnet table
arcpy.env.workspace = r'E:/Nitin.Rai/DatasetForPythonScripting'
inFeatures = "fishnet_10x10.shp"
addfield = "Rate"
fieldPrecision = 5
AddedField = arcpy.AddField_management(inFeatures, addfield, "SHORT", fieldPrecision, field_is_nullable="NULLABLE")
arcpy.CopyFeatures_management(AddedField, 'AddedFieldtotheFishnet')
# Select layer by location
arcpy.env.workspace = r'E:\Nitin.Rai\DatasetForPythonScripting'
LocationSelection = arcpy.SelectLayerByLocation_management(ErasedLayer, 'INTERSECT', outFeatureClass)
arcpy.CopyFeatures_management(LocationSelection, 'IntersectFishnetwithErasedLayer')

