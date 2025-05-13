from bokeh.models import LogColorMapper
from bokeh.palettes import Viridis6 as palette
from bokeh.plotting import figure, show
from bokeh.sampledata.unemployment import data as unemployment
from bokeh.sampledata.us_counties import data as counties
from bokeh.layouts import column
from streamlit_bokeh import streamlit_bokeh
import streamlit as st
import geopandas as gpd
from bokeh.models import (ColumnDataSource, HoverTool, CustomJS, TapTool, Select, SetValue)
from misc.gkzList import *

def createMap():
    gkz_List = gkzList['gkz']
    #gkz_List.extend([''] * 233)
    gdf = gpd.read_file('koralm2025.json') # read geojson file
    gdf = gdf.explode(ignore_index=True) # make multipolygon to separate polygons
    gdf = gdf.drop(index=179) # delete exclave hitzendorf
        
    # extract coordinates from gdf
    gdf['x'] = gdf.apply(lambda row: list(row.geometry.exterior.coords.xy[0]), axis=1)
    gdf['y'] = gdf.apply(lambda row: list(row.geometry.exterior.coords.xy[1]), axis=1)

    # prep data
    lenGDF = len(gdf)
    source = ColumnDataSource(data=dict(
            x=gdf['x'].tolist(),
            y=gdf['y'].tolist(),
            gemeinde=gdf['Gemeindename'].tolist(), 
            gkz=gdf['Gemeindenummer'].tolist(),
            line_color=['black'] * lenGDF,
            line_width=[0.5] * lenGDF,
            fill_color=['#CC79A7' if gkz in gkz_List 
                        else "#FFB81C" if gkz.startswith('2') 
                        else "#5B8C5A" for gkz in gdf['Gemeindenummer']],
            flag=[1 if gkz in gkz_List else 0 for gkz in gdf['Gemeindenummer']]  
        ))

        
    # Create a Bokeh figure OG!!!
    p = figure(
            title="",
            tools="",
            x_axis_location=None, 
            y_axis_location=None,
            tooltips=[("", "@gemeinde")],
            width=1572//2,  #og width=1572//2,
            height=966//2,  #og height=966//2,
            aspect_scale=0.68,
            match_aspect=True
        )

    p.grid.grid_line_color = None
        
    # Add patches to the figure
    patches = p.patches(
            'x', 
            'y', 
            source=source,
            fill_alpha=1,
            line_color='line_color', 
            line_width='line_width',
            fill_color='fill_color'
        )
        
        
    # Add hover tool
    hover = HoverTool()
    hover.tooltips = [("", "@gemeinde")]
    hover.renderers = [patches]
    p.add_tools(hover)

    p.toolbar.logo = None
    p.toolbar_location = None

    pp = column(p, sizing_mode="stretch_width")
    return pp