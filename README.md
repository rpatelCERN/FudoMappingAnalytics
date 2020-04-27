# FudoMappingAnalytics

This code is a short analytics excercise in reading tables in python with pandas, geocoding (converting addresses to longitude/latitude), and making a heat map to look at potential areas of interest for a catering and food delivery business. 

## Geocode Addresses

In order to complete this step, I use the google maps api. Instructions on getting an API key are here: https://developers.google.com/maps/documentation/javascript/get-api-key

The API token then gives you access to google maps within the python script below: 


```	
python python_batch_geocoding.py FILENAME 
```

Replace this line with the API token you are given: 
```  
API_KEY ='YOUR_API_KEY'
```    

The above code takes as input a .csv file (can be generated in EXCEL) with a list of addresses and outputs a csv file with the addresses and  the longitude and latitude added for each address in a folder 'data/output.csv'. This allows the addresses to be plotted as points on a map. 

## Create list of Search points

We search different sections of the city of Geneva, Switzerland using polygons for sections of tow in mapbox. A meshgrid is used to create a large array in a box around the city and then the shapely python library is used to check to see fi the points lie within the polygons. This is done within the functions of PolygonGrids.py. The search grid can be plotted in this code. 

The polygons are read into the code above as GeoJson Files where each point is listed in lat/long. 

The search grid points are then used to call the function GetListOfRestaurants.py within the same grid spacing as defined by the mesh grid (NOTE: this is hard coded so far to be 0.2km)

## Searching locations and Creating a  Heat Map

The main executable code: 

'''
python MapBoxRatio.py FILENAME_GeoJSON
'''
It requires both a google api token and a mapbox API token, which can be acquired here: https://docs.mapbox.com/help/how-mapbox-works/access-tokens/

Takes the polygons that cover the search regions you want on your map and does a gmap search for restaurants within the provided radius. The number of hits is stored as an integer between 0, 20. Nearby addresses (from the geocoding script) are matched within a 0.25km box region. Matched addresses/ number of hits is stored as the main observable for the map plots. All the output information is stored in DensityMap.csv. 

The columns in the generated csv file are used to make mapbox plots for the scan of the restaurants and the ratio. These plots will be output in your webbrowser as html files. 



