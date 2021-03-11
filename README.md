Weed Prescription Map using Arcpy using Python

This script imports Arcpy, and Rasterio packages in Python to create a weed prescription map. A feature to calculate Excess Green and 4 different VIs, namely, NDSVI, NDRE, SAVI, and OSAVI canalso be calculated using the script. The script accepts either a multispectral imagery or an RGB imagery. Based on band count, it calculates the required indices. After indices calcualtion, it also performs image sharpening and thresholding thereby converting the whole image into a binary image. After that it converts objects within the image to polygons and perfroms weed identification and craetes a weed map based on Fishnet Grid technique.

Prerequisites: 
1. Imagery should be provided by the user. Either it should be RGB imagery or Multispectral. Several Indices can be 
# calculated and exported in local drive bsaed on the imagery type provided
# 2. Shapefile (a polygon line drawn over the crops) should be provided by the user.
# Limitation of this algorithm: Weeds won't get detected or identified if they are present in-between crop rows
# Original workflow in ArcGIS was developed by Dr. J. Paulo Flores (Assistant Prof. at NDSU)
# Automation using Python scripting was developed by Nitin Rai (PhD Student)
# Agricultural Engineering, Precision Agriculture
# North Dakota State University, USA
