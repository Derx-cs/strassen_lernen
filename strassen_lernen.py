import matplotlib.pyplot as plt
import matplotlib.patches as patches
import osmnx as ox
import shapely
import random as ran
import time
import geopandas as gpd

#Get the graph which corresponds to Greifswalds drive network
G = ox.graph_from_place('Greifswald, Germany', network_type='drive')

#if an entry in a list of data exists, return true and its index
def look_if_exists(dat,data):
    for i in range(len(data)):
        if(dat==data[i]):
            return (True,i)
        
    return (False, -1)

#list for the streetnames and line/position information
names=[]
lines=[]

#convert the graph to usable gdf format
gdf=ox.graph_to_gdfs(G, nodes=False).fillna('').iterrows()
#for every edge in this graph
for _, edge in gdf:
    #get the name and geometry
    name=edge["name"]
    geom=edge["geometry"]
    #check if we already have the street as an entry
    exists,index=look_if_exists(name,names)
    #if not, add the street as new and the corresponding lines
    if(not(exists)):
        names.append(name)
        lines.append([geom])
    else:
        #if it exists, just add the new part of the street to it
        lines[index].append(geom)

#activate interactive matplotlib to allow for updates during runtime
plt.ion()

#prepare the figure and get its axes
fig=plt.figure(figsize=(16,9))
fig.add_axes((0,0,1,1))
ax=fig.get_axes()[0]

#define a polygon for overwriting the text from the previous timestep (currently not used)
overwrite=shapely.Polygon([(13.339,54.104),(13.339,54.107),(13.379,54.107),(13.379,54.104)])
p=gpd.GeoSeries(overwrite)

#main loop
for i in range(100):
    #get a random list entry which we will display
    ind=ran.randint(0,len(names))
    print(names[ind])
    
    #print the street network in black (TODO: Find a way to rewrite just the text, makes a clear unnecessary and will allow us to only need to draw the network once)
    for j in range(0,len(lines)):
        for i in range(0,len(lines[j])):
            ax.plot(lines[j][i].xy[0],lines[j][i].xy[1],c="k")

    #highlight the selected street in red
    for i in range(0,len(lines[ind])):
        ax.plot(lines[ind][i].xy[0],lines[ind][i].xy[1],c="r")
    
    #print the name of the selected street
    ax.text(13.339, 54.105,names[ind] , c='k')
    
    #give the user 10 seconds to remember
    plt.pause(10)
    
    #change the selected street back to black (not needed currently)
    #for i in range(0,len(lines[ind])):
    #    ax.plot(lines[ind][i].xy[0],lines[ind][i].xy[1],c="k")

    #Try and patch the text area to allow for a new one
    #patch=patches.Rectangle((13.339,54.1059),0.04,0.000,color='b',linewidth=0.0015,alpha=1,fill=True)
    #ax.add_patch(patch)
    
    #having given up on the patching of the street names, just clear the whole figure and start anew
    ax.clear()