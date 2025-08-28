import matplotlib.pyplot as plt
import matplotlib.patches as patches
import osmnx as ox
import shapely
import random as ran
import time
import geopandas as gpd

G = ox.graph_from_place('Greifswald, Germany', network_type='drive')

def look_if_exists(dat,data):
    for i in range(len(data)):
        if(dat==data[i]):
            return (True,i)
        
    return (False, -1)


names=[]
lines=[]

merged_lines=[]

gdf=ox.graph_to_gdfs(G, nodes=False).fillna('').iterrows()
for _, edge in gdf:
    name=edge["name"]
    geom=edge["geometry"]
    exists,index=look_if_exists(name,names)
    if(not(exists)):
        names.append(name)
        lines.append([geom])
    else:
        lines[index].append(geom)
plt.ion()
fig=plt.figure(figsize=(16,9))
fig.add_axes((0,0,1,1))
ax=fig.get_axes()[0]
overwrite=shapely.Polygon([(13.339,54.104),(13.339,54.107),(13.379,54.107),(13.379,54.104)])
p=gpd.GeoSeries(overwrite)
for i in range(100):
    ind=ran.randint(0,len(names))
    print(names[ind])

    for j in range(0,len(lines)):
        for i in range(0,len(lines[j])):
            ax.plot(lines[j][i].xy[0],lines[j][i].xy[1],c="k")

    for i in range(0,len(lines[ind])):
        ax.plot(lines[ind][i].xy[0],lines[ind][i].xy[1],c="r")
    ax.text(13.339, 54.105,names[ind] , c='k')
    plt.pause(10)
    for i in range(0,len(lines[ind])):
        ax.plot(lines[ind][i].xy[0],lines[ind][i].xy[1],c="k")
    #patch=patches.Rectangle((13.339,54.1059),0.04,0.000,color='b',linewidth=0.0015,alpha=1,fill=True)
    #ax.add_patch(patch)
    ax.clear()