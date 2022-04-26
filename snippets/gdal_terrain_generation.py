from osgeo import gdal, gdal_array
filepath = '/Users/odinndagur/Blender/2022/islandsdem-modular-heightmap/data/temp/IslandsDEMv1.0_2x2m_zmasl_isn2016_57_x_4_y_4.tif'
filepath = '/Users/odinndagur/Blender/2022/islandsdem-modular-heightmap/data/raw/IslandsDEMv1.0_2x2m_zmasl_isn2016_57.tif' # testa með heilu 25k * 25k tif

filepath = '/Users/odinndagur/Blender/2022/islandsdem-modular-heightmap/data/temp/IslandsDEMv1.0_2x2m_zmasl_isn2016_57_x_3_y_5.tif'

rasterArray = gdal_array.LoadFile(filepath)
raster = gdal.Open(filepath)
band = raster.GetRasterBand(1)

import numpy as np
print(gdal.GetDataTypeName(band.DataType))
# Get nodata value from the GDAL band object
nodata = band.GetNoDataValue()

#Create a masked array for making calculations without nodata values
rasterArray = np.ma.masked_equal(rasterArray, nodata)
type(rasterArray)

# Check again array
min = rasterArray.min()
max = rasterArray.max()
print(min,max)

from math import sqrt
import bpy

import pandas as pd
import os
df = pd.DataFrame(rasterArray)

heights = df.iloc[:,1:].values


def generate_terrain_mesh(row,col):
    w = 251
    h = 251
    scale = 1
    plane_name = 'x{x}y{y}_plane_width{w}_height{h}_scale{scale}'.format(x=col,y=row,w=w,h=h,scale=scale)
    xmin = col * (w-1)
    ymin = row * (h-1)
    edges = []
    faces = []
    
    if(row == 9):
        xmin -= 1
    if(col == 9):
        ymin -= 1
    vertices = [((x-xmin)*scale,(y-ymin)*scale,heights[x][y]*scale) for x in range(xmin,xmin+w) for y in range(ymin,ymin+h)]
    #print(len(heights),len(heights[2500]))

    # make triangle faces
    vertexIndex = 0
    sz = int(sqrt(len(vertices)))
    for y in range(sz):
        for x in range(sz):
            if (x < sz - 1) and (y < sz - 1):
                # faces.append((vertexIndex,vertexIndex+width+1,vertexIndex+width)) #unity mode
                # faces.append((vertexIndex + width + 1, vertexIndex, vertexIndex+1)) #unity mode
                faces.append((vertexIndex+sz,vertexIndex+sz+1,vertexIndex)) #blender mode
                faces.append((vertexIndex+1, vertexIndex,vertexIndex + sz + 1)) #blender mode
            vertexIndex+=1


    new_mesh = bpy.data.meshes.new(plane_name)
    new_mesh.from_pydata(vertices, edges, faces)
    new_mesh.update()
    # make object from mesh
    new_object = bpy.data.objects.new(plane_name, new_mesh)
    # make collection
    IslandsDEM_collection = bpy.data.collections.get('IslandsDEM')
    if not IslandsDEM_collection:
        IslandsDEM_collection = bpy.data.collections.new('IslandsDEM')
        bpy.context.scene.collection.children.link(IslandsDEM_collection)
    IslandsDEM_collection.objects.link(new_object)
    new_object.select_set(True)
    new_object.location = (col*w*scale - scale*col,row*h*scale - scale*row,0)
    #bpy.ops.view3d.view_selected(use_all_regions=False)
    
for i in range(3,6):
    for j in range(6,9):
        generate_terrain_mesh(i,j)