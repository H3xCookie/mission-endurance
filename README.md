# mission-endurance
Very nice

## Software architecture description

### Preliminary data gathering from OLAF

Get information of each field which is subsidized by the EU, preferably as a shapefile. Get metadata, such as supposed crop type, approximate time of planting etc. Superimpose the shapefiles on the satellite image (shouldn't be too hard). Perform stat analysis on the pixels of the field. They should be similar, in case they are not, probably we shot the image during harvesting. Otherwise we analyse the image for whether it has been harvested or not (ML model #1). If it has been harvested, run the before-harvest photos against a model which tries to determine the crop type (ML model #2).
