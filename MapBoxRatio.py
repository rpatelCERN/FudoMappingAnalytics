import pandas as pd
import plotly.express as px
from GetListOfRestaurants import RestoFinder
from PolygonGrids import ScanPolygon
import csv
import googlemaps
import gmaps
import sys
API_KEY ='YOUR_API_KEY'
gm = googlemaps.Client(key=API_KEY)
gmaps.configure(api_key=API_KEY) # Your Google API key
#geocode_result = gm.geocode('Geneve Switzerland')[0]
center_lat=46.2043907#geocode_result['geometry']['location']['lat']
center_lng=6.1431577#geocode_result['geometry']['location']['lng']
print('center=',center_lat,center_lng)
GridPoints=ScanPolygon("%s" %sys.argv[1])
gridx=GridPoints[0]
gridy=GridPoints[1]


def DensitySoverB(dffood, df):
    densityMap=pd.DataFrame(columns=['latitude','longitude','density','hits'])
    for index, row in dffood.iterrows():#step through all grid points
        restodensity=row['hits']
        officedensity=0;
        for index2, row2, in df.iterrows():#check for office buildings
            dx=row['latitude']-row2['latitude']
            dy=row['longitude']-row2['longitude']
            if(abs(dx)>0.002581 or abs(dy)>0.0025):continue
            officedensity=officedensity+1
        #if(officedensity<1):continue #nothing matches
        #if(restodensity<1):restodensity=1;
        if(restodensity>0):densityMap=densityMap.append({'latitude':row['latitude'],'longitude':row['longitude'],'density':float(officedensity)/restodensity,'hits':row['hits'] },ignore_index=True)
        else:densityMap=densityMap.append({'latitude':row['latitude'],'longitude':row['longitude'],'density':float(officedensity),'hits':row['hits'] },ignore_index=True)
        #if restodensity>0:print(float(officedensity)/restodensity,officedensity,restodensity)
        #else:print(officedensity,restodensity)

        #if(row['hits']<1):continue
        #print(index,row)
    #print(densityMap.dtypes)
    return densityMap

def ScanGMaps(fname,gridx,gridy):
    with open(fname, mode='w') as restaurants_file:
        fieldnames = ['latitude','longitude','hits']
        writer = csv.DictWriter(restaurants_file, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(len(gridx)):
                testpoint=[gridy[i], gridx[i]] #lat, long so reverse y,x
                #print(testpoint[1], testpoint[0])
                RestoFinder(testpoint[0], testpoint[1],API_KEY,writer)
ScanGMaps("restaurants_file.csv",gridx,gridy)
#import matplotlib.pyplot as plt

#fig=plt.figure()
#ax=fig.add_axes([0,0,1,1])
#gridx,gridy=ScanPolygon("/Users/rishipatel/Downloads/features.geojson");
#ax.scatter(gridx, gridy)
#plt.show()


px.set_mapbox_access_token("Mapbox_API_TOKEN")

df = pd.read_csv('restaurants_file.csv')
dfoffice = pd.read_csv('data/output-2015.csv')

densityMap=DensitySoverB(df,dfoffice)
densityMap.to_csv(r'DensityMap.csv', index = True)
#locationsFood=densityMap['latitude','longitude']
officeoverRestodensity=densityMap['density']
ghits=df['hits']
all_rows=[densityMap['latitude'],densityMap['longitude'],ghits,officeoverRestodensity]

AllinfoDF=pd.DataFrame(all_rows,columns=['latitude','longitude','hits','density'])


import plotly.express as px
fig = px.density_mapbox(df, lat='latitude', lon='longitude', z='hits', radius=20,
                        center=dict(lat=center_lat, lon=center_lng), zoom=10,
                        mapbox_style="stamen-terrain")
fig.show()
fig2 = px.scatter_mapbox(df, lat="latitude", lon="longitude",     color="hits", size="hits",
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=20, zoom=10)
fig2.show()

fig3 = px.scatter_mapbox(densityMap, lat="latitude", lon="longitude",     color="density", size="density",
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=20, zoom=10)
fig3.show()
