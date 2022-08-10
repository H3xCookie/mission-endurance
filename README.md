# mission-endurance
Very nice

## 1. Preliminary data gathering from OLAF

Get information of each field which is subsidized by the EU, preferably as a shapefile. Get metadata, such as supposed crop type, approximate time of planting etc. 

## 2. Take pictures of the fields

Point the satellite to the given fields and take pictures before, during and after harvest time for each given field. For testing use SENTINEL data (same resolution). Output should be image with metadata for sat position, so we can later convert to a geocentric coordinate system. 

## 3. Get training data for models
Pls Shelly make it work pls

### Recognising if a field is planted with crops or already harvested

Need an index of (image, shapefile, crop status), train the model on individual pixels inside the shapefile (only color information).

### Identifying the crop type of the unharvested fields

Same info as top section, but with crop type instead of crop/no_crop. 

## 4. Image analysis

Run the images with shapefiles against ML models 1 and 2 to determine what crop is there on every field, or if it is harvested. If anything unusual is reported, contact ground with relevant images, as well as the analysis performed in space. 


