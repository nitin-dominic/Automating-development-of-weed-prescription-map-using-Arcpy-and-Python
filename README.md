# Weed Prescription Map using Arcpy and Python

This algorithm imports Arcpy, and Rasterio packages in Python to create a weed prescription map. A feature to calculate Excess Green and 4 different VIs, namely, Normalised Difference Vegetation Index (NDVI), Normalized Difference Red Edge Index (NDRE), Soil Adjusted Vegetation Index (SAVI), and Optimized Soil Adjusted Vegetation Index (OSAVI) can also be calculated and exported to local drive using this script. The script accepts either a multispectral imagery or an RGB imagery. Based on band count, it calculates the required indices. After indices calcualtion, it also performs image sharpening and thresholding thereby converting the whole image into a binary image. After that it converts objects within the image to polygons and perfroms weed identification while creating a weed map using Fishnet Grid technique.

# Prerequisites: 
1. RGB or a multispectral imagery should be provided by the user.
2. Specify an directory with an empty folder before this scripts starts exporting all the indices (output images) or processed images.

3. Shapefile (a polygon line drawn over the crops) should be provided by the user.

# Limitation of this algorithm: 
1. Weeds won't get detected or identified if they are present in-between crop rows.

# Credits:
1. Original workflow in ArcGIS Pro was developed by Dr. J. Paulo Flores (Assistant Prof. at NDSU)
2. Automation using Python scripting was developed by Nitin Rai (PhD Student)

# Codes were developed at the Department of Agricultural and Biosystems Engineering at North Dakota State University, USA

# Final image output looks somewhat like this based on location of weeds on the imagery:

Legends:

a. Red square: Weeds (Targets)
b. Green Square: Either crops or soil (Non-targets) 
![weed](https://user-images.githubusercontent.com/68175121/110733196-27cd5d80-81eb-11eb-859b-ba662f105a59.jpg)
