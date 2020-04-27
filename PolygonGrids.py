from shapely import geometry
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import geojson


from matplotlib import path
import matplotlib.pyplot as plt
import numpy as np
def ScanPolygon(fname):
    Polygons=[]
    GridPoints=[]
    with open(fname) as json_file:
        json_data = geojson.load(json_file)
        for i in range(0,4):
            coordlist = json_data.features[i]['geometry']['coordinates'][0]
            #print(json_data.features[i]['properties']['Commune'])
            commune=json_data.features[i]['properties']['Commune']
            pointList = []
            for p in coordlist:pointList.append(Point(p[0],p[1]))
            poly = geometry.Polygon(pointList)
            Polygons.append(poly)

    xv,yv = np.meshgrid(np.linspace(6.019343820934978,6.238756882209202,85),np.linspace(46.158198093616335, 46.25326344729717,55))#### Coding a box around Geneva to search for points in the polygon
    gridx=[]
    gridy=[]
    for x in xv[0]:
        for y in yv:
            #print(x,y[0])
            gridpoint=Point(x,y[0])
            for poly in Polygons:
                if poly.contains(gridpoint):
                    #print("Found")
                    gridx.append(x)
                    gridy.append(y[0])

    return gridx,gridy

#fig=plt.figure()
#ax=fig.add_axes([0,0,1,1])
#gridx,gridy=ScanPolygon("/Users/rishipatel/Downloads/features.geojson");
#ax.scatter(gridx, gridy)
#plt.show()
