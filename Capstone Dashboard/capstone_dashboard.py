
# coding: utf-8

# In[3]:



import numpy as np
import pandas as pd
#import geoviews as gv   #explore and visualize geographical datasets
import holoviews as hv #GeoViews is built on the HoloViews library for building flexible visualizations of multidimensional data
#import geoviews.feature as gf #visualize diff types of features(ocean,land,coastline,borders etc)
import cartopy #designed for geospatial data processing in order to produce maps and other geospatial data analyses.

#from cartopy import crs as ccrs
from bokeh.tile_providers import STAMEN_TONER_LABELS#provide varities of tiles
#from bokeh.models import WMTSTileSource
#from bokeh.models.widgets import Panel, Tabs, Select
from bokeh.models.widgets import Select,Panel,Tabs

#import param, paramnb
from bokeh.layouts import layout
import json
from bokeh.io import show, output_notebook, output_file
from bokeh.models import (
    GeoJSONDataSource,
    HoverTool,
   # LinearColorMapper,
    CategoricalColorMapper,
    LogColorMapper
)
from bokeh.plotting import figure
from bokeh.palettes import Viridis9 as palette
from bokeh.io import curdoc


hv.notebook_extension('bokeh')


# ## Loading the data
# 
# Here we are loading data for all the years i:e from 2008 to 2016. 
data=pd.read_csv('Human_Traffic_data.csv', encoding= 'ISO-8859-1')


# Extracting the Required columns like "Destination_Country", "Origin_Country" their Logitude Latitude etc.
data=data[["Transit_Country","Years","Destination_Country", "Destination_Latitude","Destination_Longitude",
          "Flagged","Means","Notes","Origin_Country","Sector","Victim_Profile","trafficker","Type_Of_Trafficking",
          "Source_Latitude","Source_Longitude"]]


# Replacing Trafficker null values to 0 and removing commas(9,10 becomes 910)
# We need the show the trafficker infomation in the hover

data['trafficker'] = data['trafficker'].str.replace(',', '')
data['trafficker'] = data['trafficker'].str.replace(' ', '')
data.trafficker.fillna(0,inplace=True)


## Handling for type of trafficing


## Function to split the string like 1,2,3 will be 3 rows 

def change_column_order(df, col_name, index):
    cols = df.columns.tolist()
    cols.remove(col_name)
    cols.insert(index, col_name)
    return df[cols]

def split_df(dataframe, col_name, sep):
    orig_col_index = dataframe.columns.tolist().index(col_name)
    orig_index_name = dataframe.index.name
    orig_columns = dataframe.columns
    dataframe = dataframe.reset_index()  # we need a natural 0-based index for proper merge
    index_col_name = (set(dataframe.columns) - set(orig_columns)).pop()
    df_split = pd.DataFrame(
        pd.DataFrame(dataframe[col_name].str.split(sep).tolist())
        .stack().reset_index(level=1, drop=1), columns=[col_name])
    df = dataframe.drop(col_name, axis=1)
    df = pd.merge(df, df_split, left_index=True, right_index=True, how='inner')
    df = df.set_index(index_col_name)
    df.index.name = orig_index_name
    # merge adds the column to the last place, so we need to move it back
    return change_column_order(df, col_name, orig_col_index)

data['Type_Of_Trafficking']= data['Type_Of_Trafficking'].astype(str)
data = split_df(data, 'Type_Of_Trafficking', ',')


data['Type_Of_Trafficking'] = data['Type_Of_Trafficking'].replace(['1.0','2.0','3.0','4.0','5.0','6.0','7.0','8.0','9.0','10.0','1','2','3','4','5','6','7','8','9','10','nan'], ['Sexual exploitation',
                                                                     'Sexual exploitation',
                                                                     'Forced labor',
                                                                     'Domestic servitude',
                                                                     'Child sex tourism',
                                                                     'Forced drug trafficking',
                                                                     'Forced begging',
                                                                     'Child soldiers',
                                                                     'Forced criminal activity',
                                                                     'Child sexual exploitation',
                                                                     'Forced marriage',
                                                                     'Sexual exploitation'
                                                                     'Forced labor',
                                                                     'Domestic servitude',
                                                                     'Child sex tourism',
                                                                     'Forced drug trafficking',
                                                                     'Forced begging',
                                                                     'Child soldiers',
                                                                     'Forced criminal activity',
                                                                     'Child sexual exploitation',
                                                                     'Forced marriage',''
                                                                     ])




# As a part of cleaning , lets change the Date format of Year to **Numeric.**

data.Years=data.Years.astype(int)

# Replacing all null values to zero and trafficker values to **Numeric** for some Validation purpose.
data.trafficker=pd.to_numeric(data.trafficker)

# Creating Interactive Paramets/Widgets to the graph

# As per the requirement we are handling the below functionalities.
# > </font color = green> Graph </font> showing human trafficing from source to destination for each particular year. 
# 
# > Hover tool on country to show a statistics on the trafficing distribution like the origin ountry, soure country the year etc.
# 
# > Showing the number of connections associated with eah country.
# 
# To show the number of connections for each country.

counts = data.groupby('Origin_Country')[['Destination_Country']].count().reset_index().rename(columns={'Destination_Country': 'Connections'})


# Joining the count data frame with Original dataframe which will allow us to show that column value "count" in the hover tool. 

## merge count with data.
data_df = pd.merge(data, counts, left_on='Origin_Country', right_on='Origin_Country', how='left')


# Dropping the source and destination longitude and latitude having Null values. 

data_df.dropna(subset = ['Destination_Latitude'], inplace = True)
data_df.dropna(subset = ['Destination_Longitude'], inplace = True)
data_df.dropna(subset = ['Source_Latitude'], inplace = True)
data_df.dropna(subset = ['Source_Longitude'], inplace = True)


# Traffic Points are the destination points. We will able to track those points using Longitude and Latitude. 
# 
# .Triffic Nodes have the Destination country name, Longitude and Latitude with the Hover information.
# 
# 
# Then Finally the graph connecting from source to destination point

#data_df_countries[data_df_countries['Country'] =='Australia']
#data_df_countries.columns
from bokeh.io import show, output_notebook
from bokeh.layouts import Column
from bokeh.models import (Plot, Range1d, GraphRenderer, ColumnDataSource, GlyphRenderer,
                          Circle, MultiLine, StaticLayoutProvider, HoverTool, LinearAxis,
                          DataTable, TableColumn, TapTool, BoxSelectTool, BoxZoomTool,
                          ResetTool, NodesAndLinkedEdges, GeoJSONDataSource, Patches,
                          WheelZoomTool, Arrow, OpenHead, NormalHead, VeeHead)
from bokeh.palettes import Set3_12

def source_connection(inputyear):
    data_df_year = data_df[data_df.Years == inputyear].reset_index(drop=True)
    data_df_year.index.name = "index"
    connections_df_year = data_df_year[['Origin_Country','Destination_Country']]
    connections_df_year = connections_df_year.rename(columns={"Origin_Country": "start", 
                                                    "Destination_Country": "end"})
    ## two df 
    data_df_year_src = data_df_year[['Origin_Country','Source_Latitude','Source_Longitude']]
    data_df_year_dest= data_df_year[['Destination_Country','Destination_Latitude','Destination_Longitude']]

    ## rename
    data_df_year_src = data_df_year_src.rename(columns={"Origin_Country": "Country", "Source_Latitude": "Latitude", "Source_Longitude":"Longitude"})
    data_df_year_dest = data_df_year_dest.rename(columns={"Destination_Country": "Country", "Destination_Latitude": "Latitude", "Destination_Longitude":"Longitude"})

    ## merge
    data_df_countries_year = data_df_year_src.append(data_df_year_dest)

    #data_df_countries.drop_duplicates(subset=None, keep='first', inplace=True)
    data_df_countries_year.dropna(inplace=True)
    
    unique_country = set(data_df_countries_year.Country)
    #unique_country.update(data_df.Origin_Country)
    dict_country_to_id = {c:i for (i,c) in enumerate(unique_country)}
    dict_country_to_id
    data_df_countries_year['country_id'] = data_df_countries_year.apply(lambda r: dict_country_to_id[r.Country] , axis = 1)
    
    #data_df_countries_year.insert(1, 'country_id', range(1, 1 + len(data_df_countries_year)))
    #data_df_countries_year.set_index('country_id', drop=True, append=False, inplace=False, verify_integrity=False)
    connections_df_year.fillna(0,inplace = True)
    connections_df_year.drop_duplicates(subset=None, keep='first', inplace=True)

    #minimum value for each country 
    y = data_df_countries_year.sort_values("country_id").groupby("Country", as_index=False).first()
    for cnty in connections_df_year['start'].unique():
        if (type(cnty)  == str):
            t = y.loc[y["Country"] == cnty ,'country_id']
            connections_df_year.loc[connections_df_year['start'] == cnty ,'start'] =int(t.values)

    for cnty in connections_df_year['end'].unique():
        if (type(cnty)  == str):
            t = y.loc[y["Country"] == cnty ,'country_id']
            connections_df_year.loc[connections_df_year['end'] == cnty ,'end'] = int(t.values)
            
    return connections_df_year, data_df_countries_year

# Lets Run the above function to get the nodes and connection infomation for all the years (from 2008 to 2016)

connections_df_2008, data_df_countries_2008 = source_connection(2008)
connections_df_2009, data_df_countries_2009 = source_connection(2009)
connections_df_2010, data_df_countries_2010 = source_connection(2010)
connections_df_2011, data_df_countries_2011 = source_connection(2011)
connections_df_2012, data_df_countries_2012 = source_connection(2012)
connections_df_2013, data_df_countries_2013 = source_connection(2013)
connections_df_2014, data_df_countries_2014 = source_connection(2014)
connections_df_2015, data_df_countries_2015 = source_connection(2015)
connections_df_2016, data_df_countries_2016 = source_connection(2016)

#geo_projection = ccrs.Geostationary(central_longitude=data_df_countries.Longitude)

#######################   Tier Information  ####################################################

## Plot for Tier Information . We have tier information of country from 2008 to 2016.
#step1 : Load the data for all countries 
tier_df = pd.read_excel("TIP Tier Rankings.xlsx")

# Loading data for list of longitude and latitude for the countries from world.geojson. 
with open(r'world.geojson', 'r') as f:
    geoSource_data = json.load(f)


# Step2:Adding tier field to the property of the feature attribute in world.json.The function "tier_info"
# takes the input as year and returns a new jeojson having addition attribute "Tier". 

def tier_info(year):
    country_t = tier_df[tier_df.Year == year]
    
    with open(r'world.geojson', 'r') as f:
        geoSource_data = json.load(f)

    for i in geoSource_data["features"]:
        country = str(i["properties"]["name"] )
        if country in country_t['Country'].unique():
            tier_info =  country_t[country_t["Country"] == country ]['Tier Ranking']
            i["properties"]["Tier"] = str(tier_info.values[0])
        else: 
            i["properties"]["Tier"] = 'No Tier Infomation'
            
    return geoSource_data

# Step3: Call the above function for all the years and dump the respective file into a new geojson file.

geoSource_data_2008 = tier_info(2008)
with open("geoSource_final_2008.geojson", 'w') as json_file:
        json.dump(geoSource_data_2008, json_file)
        
geoSource_data_2009 = tier_info(2009)
with open("geoSource_final_2009.geojson", 'w') as json_file:
        json.dump(geoSource_data_2009, json_file)
        
geoSource_data_2010 = tier_info(2010)
with open("geoSource_final_2010.geojson", 'w') as json_file:
        json.dump(geoSource_data_2010, json_file)
        
geoSource_data_2011 = tier_info(2011)
with open("geoSource_final_2011.geojson", 'w') as json_file:
        json.dump(geoSource_data_2011, json_file)
        
geoSource_data_2012 = tier_info(2012)
with open("geoSource_final_2012.geojson", 'w') as json_file:
        json.dump(geoSource_data_2012, json_file)
        
geoSource_data_2013 = tier_info(2013)
with open("geoSource_final_2013.geojson", 'w') as json_file:
        json.dump(geoSource_data_2013, json_file)

geoSource_data_2014 = tier_info(2014)
with open("geoSource_final_2014.geojson", 'w') as json_file:
        json.dump(geoSource_data_2014, json_file)  

geoSource_data_2015 = tier_info(2015)
with open("geoSource_final_2015.geojson", 'w') as json_file:
        json.dump(geoSource_data_2015, json_file)
        
geoSource_data_2016 = tier_info(2016)
with open("geoSource_final_2016.geojson", 'w') as json_file:
        json.dump(geoSource_data_2016, json_file)

# Step 4: reading back the new updated json data.

with open(r'geoSource_final_2008.geojson', 'r') as f:
    geoSource_new_2008 = GeoJSONDataSource(geojson=f.read())

with open(r'geoSource_final_2009.geojson', 'r') as f:
    geoSource_new_2009 = GeoJSONDataSource(geojson=f.read())
    
with open(r'geoSource_final_2010.geojson', 'r') as f:
    geoSource_new_2010 = GeoJSONDataSource(geojson=f.read())

with open(r'geoSource_final_2011.geojson', 'r') as f:
    geoSource_new_2011 = GeoJSONDataSource(geojson=f.read())
    
with open(r'geoSource_final_2012.geojson', 'r') as f:
    geoSource_new_2012 = GeoJSONDataSource(geojson=f.read())

with open(r'geoSource_final_2013.geojson', 'r') as f:
    geoSource_new_2013 = GeoJSONDataSource(geojson=f.read())
    
with open(r'geoSource_final_2014.geojson', 'r') as f:
    geoSource_new_2014 = GeoJSONDataSource(geojson=f.read())

with open(r'geoSource_final_2015.geojson', 'r') as f:
    geoSource_new_2015 = GeoJSONDataSource(geojson=f.read())
    
with open(r'geoSource_final_2016.geojson', 'r') as f:
    geoSource_new_2016 = GeoJSONDataSource(geojson=f.read())
    
TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

# Now.. time to plot the final figure 
p = figure(title="Tier Infomation for Countries", 
          tools=TOOLS, 
          x_axis_location=None, 
          y_axis_location=None, 
          width=800, 
          height=700)
p.grid.grid_line_color = None

palette.reverse()
#mapper1 = LinearColorMapper(palette=palette, low=0, high=262000)
mapper2 = CategoricalColorMapper(palette=["#4ca64c","yellow","orange","#ff3232","white"], 
                                 factors=["1", "2","2W","3",'No Tier Infomation'])

hover1 = HoverTool( tooltips=[("Country","@name"), ("Tier", "@Tier")] )
p.add_tools(hover1)
    
# Function to plot tier infomation graph. Here we need to only pass the updated data for a particular year

def tier_graph(geoSource_new):
    p.patches('xs', 'ys', fill_alpha=1,  #fill_color='red', , 'transform': mapper1
              fill_color={'field': 'Tier','transform': mapper2},
              line_color='Red', line_width=0.5, source=geoSource_new, legend='Tier')
    show(p)

##### Plottt graph 
with open('world.geojson', 'r') as f:
            geo_source = f.read()
geoSource_data = GeoJSONDataSource(geojson=geo_source)

## prior node ifo
node_glyph = Circle( size=8,  fill_color=Set3_12[3])
node_nonselection = Circle( fill_color=Set3_12[3], line_dash='dashed', fill_alpha=0.2, line_alpha=0.1)
node_selection = Circle(fill_color=Set3_12[10], fill_alpha=0.8, line_alpha=0.3,line_width=10, line_color='green')
## prior edge information 
edge_glyph = MultiLine(line_alpha=0.05) #line_dash='dashed')
edge_hover = MultiLine(line_alpha=0.6, line_color="Blue", line_dash="4 4")
edge_selection = MultiLine(line_alpha=1, line_width=3 , line_color= "Red", line_dash='dashed')
edge_nonselection = MultiLine(line_width=0.02 , line_color= "grey")

## Plot for adding filter and making the graph 

def plot_data(data_df,connections,year,geoSource_new):
    
    data_df_countries = data_df #.drop_duplicates(subset=None, keep='first', inplace=True)
    connections_df = connections

    node_source = ColumnDataSource(data_df_countries[["country_id","Country", "Longitude", "Latitude"]])
    edge_source = ColumnDataSource(connections_df[["start", "end"]])

    node_renderer = GlyphRenderer(data_source=node_source, 
                                  glyph=node_glyph,
                                  selection_glyph=node_selection, 
                                  nonselection_glyph=node_nonselection)

    ## Create edge_renderer
    edge_renderer = GlyphRenderer(data_source=edge_source, glyph=edge_glyph,
                                  hover_glyph=edge_hover, selection_glyph=edge_selection, 
                                  nonselection_glyph=edge_nonselection
                                 )
    ## Create layout_provider
    graph_layout = dict(zip(data_df_countries.country_id.astype(str), 
                            zip(data_df_countries.Longitude, data_df_countries.Latitude)))
    layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

    ## Create graph renderer
    graph = GraphRenderer(edge_renderer=edge_renderer, 
                          node_renderer=node_renderer, 
                          layout_provider=layout_provider, 
                          inspection_policy=NodesAndLinkedEdges(),
                          selection_policy=NodesAndLinkedEdges())

    plot = Plot(x_range=Range1d(-150, 150), y_range=Range1d(15, 75), plot_width=800, plot_height=600, background_fill_color=Set3_12[4],background_fill_alpha=0.2)

    plot.title.text = "Human Trafficing Visualization for "+ str(year)

    # plot.add_glyph( geoSource_data, Patches(xs='xs', ys='ys', line_color='grey'
    #                      , line_width=.5, fill_color=Set3_12[6], fill_alpha=0.25))

    plot.add_glyph(geoSource_new, Patches(xs='xs', ys='ys', line_color='grey'
                        , line_width=.2,  fill_color={'field': 'Tier','transform': mapper2}, fill_alpha=0.25))


    plot.renderers.append(graph)
    plot.add_layout(LinearAxis(axis_label="Latitude"), "below")
    plot.add_layout(LinearAxis(axis_label="Longitude"), "left")

    hover = HoverTool(show_arrow=True,# tooltips=  # [("Country Involved: ", "@Country")],
                      tooltips="""
                                <div>
                                    <div>
                                        <span style="font-size: 15px;">Country Information </span>
                                        <span style="font-size: 12px; color: #696;">@Destination_Country </span>
                                    </div>
                                </div>
                                """, 
                      renderers=[graph])
    hover_no_tooltips = HoverTool(tooltips=None, renderers=[graph])
    box_zoom = BoxZoomTool()

    plot.add_tools(hover, hover_no_tooltips, box_zoom, TapTool(), BoxSelectTool(), ResetTool(), WheelZoomTool())
    plot.toolbar.active_inspect = [hover, hover_no_tooltips]
    plot.toolbar.active_drag = box_zoom
    plot.outline_line_color = "navy"
    plot.outline_line_alpha = 0.3
    plot.outline_line_width = 3
    plot.add_tile(STAMEN_TONER_LABELS)
    
    return plot

data_df.insert(1, 'country_id', range(1, 1 + len(data_df)))
plot2008 = plot_data(data_df_countries_2008,connections_df_2008,2008,geoSource_new_2008)
plot2009 = plot_data(data_df_countries_2009,connections_df_2009,2009,geoSource_new_2009)
plot2010 = plot_data(data_df_countries_2010,connections_df_2010,2010,geoSource_new_2010)
plot2011 = plot_data(data_df_countries_2011,connections_df_2011,2011,geoSource_new_2011)
plot2012 = plot_data(data_df_countries_2012,connections_df_2012,2012,geoSource_new_2012)
plot2013 = plot_data(data_df_countries_2013,connections_df_2013,2013,geoSource_new_2013)
plot2014 = plot_data(data_df_countries_2014,connections_df_2014,2014,geoSource_new_2014)
plot2015 = plot_data(data_df_countries_2015,connections_df_2015,2015,geoSource_new_2015)
plot2016 = plot_data(data_df_countries_2016,connections_df_2016,2016,geoSource_new_2016)


def update_plot(attr,old,new):
    if (select.value == "2008"):
        print("2008")
        curdoc().clear()
        curdoc().add_root(tabs)
       # curdoc().add_root(myLayout1)
       # curdoc().add_root(toggle_layout) 
        curdoc().add_root(plot2008)
    if (select.value == "2009"):
        print("2009")
        curdoc().clear()
        curdoc().add_root(tabs)
        #curdoc().add_root(myLayout1)
       # curdoc().add_root(toggle_layout)
        curdoc().add_root(plot2009)
    if (select.value == "2010"):
        print("2010")
        curdoc().clear()
        curdoc().add_root(tabs)
        #curdoc().add_root(myLayout1)
       # curdoc().add_root(toggle_layout)
        curdoc().add_root(plot2010)
    if (select.value == "2011"):
        print("2011")
        curdoc().clear()
        curdoc().add_root(tabs)
        #curdoc().add_root(myLayout1)
        curdoc().add_root(plot2011)
    if (select.value == "2012"):
        curdoc().clear()
        curdoc().add_root(tabs)
        #curdoc().add_root(myLayout1)
       #curdoc().add_root(toggle_layout)
        curdoc().add_root(plot2012)
    if (select.value == "2013"):
        print("2013")
        curdoc().clear()
        curdoc().add_root(tabs)
        #curdoc().add_root(myLayout1)
        #curdoc().add_root(toggle_layout)
        curdoc().add_root(plot2013)
    if (select.value == "2014"):
        print("fig4")
        curdoc().clear()
        curdoc().add_root(tabs)
        #curdoc().add_root(myLayout1)
        #curdoc().add_root(toggle_layout)
        curdoc().add_root(plot2014)
    if (select.value == "2015"):
        print("2015")
        curdoc().clear()
        curdoc().add_root(tabs)
        #curdoc().add_root(myLayout1)
        #curdoc().add_root(toggle_layout)
        curdoc().add_root(plot2015)
    if (select.value == "2016"):
        print("fig4")
        plot2016 = plot_data(data_df_countries_2016,connections_df_2016,2016,geoSource_new_2016)
        curdoc().clear()
        curdoc().add_root(tabs)
       # curdoc().add_root(myLayout1)
       # curdoc().add_root(toggle_layout)
        curdoc().add_root(plot2016)

#  create select widget
select = Select(title="Please Select Year:", value="fig4", options=[("2008","2008"), 
                                                               ("2009","2009"), 
                                                               ("2010","2010"), 
                                                               ("2011","2011"),
                                                               ("2012","2012"),
                                                               ("2013","2013"),
                                                               ("2014","2014"),
                                                               ("2015","2015"),
                                                               ("2016","2016"),
                                                              ])
select.on_change("value",update_plot)
#curdoc().clear()
myLayout1 = layout([[select]])
# add the select width
#curdoc().add_root(layout([[button]]))   # add the select width
#show(plot2009)

def tier_graph1(geoSource_new, year):
    
    
    
    p = figure(title="Tier Infomation for the Year :"+str(year), 
          tools=TOOLS, 
          x_axis_location=None, 
          y_axis_location=None, 
          width=800, 
          height=700)
    p.grid.grid_line_color = None

    palette.reverse()
    mapper2 = CategoricalColorMapper(palette=["#4ca64c","yellow","orange","#ff3232","white"], 
                                     factors=["1", "2","2W","3",'No Tier Infomation'])
    label=["1", "2","2W","3",'No Tier Infomation']

    for factor, color in zip(mapper2.factors, mapper2.palette):
        p.circle(x=[], y=[], size = 5, fill_color=color, legend=factor)

    hover1 = HoverTool( tooltips=[("Country","@name"), ("Tier", "@Tier")] )
    p.add_tools(hover1)
    p.legend.border_line_width = 3
    p.legend.border_line_color = "navy"
    p.legend.border_line_alpha = 0.2
    p.legend.location = "center_left"
    p.patches('xs', 'ys', fill_alpha=1,  #fill_color='red', , 'transform': mapper1
              fill_color={'field': 'Tier','transform': mapper2},
              line_color='Red', line_width=0.5, source=geoSource_new)
    #p.title.text = "Tier Information for:" + str(year)
    p.legend.location = "center_left"
    return p

with open('world.geojson', 'r') as f:
            geo_source = f.read()
        
geoSource_data = GeoJSONDataSource(geojson=geo_source)


plot2008_tier = tier_graph1(geoSource_new_2008, 2008)
plot2009_tier = tier_graph1(geoSource_new_2009, 2009)
plot2010_tier = tier_graph1(geoSource_new_2010, 2010)
plot2011_tier = tier_graph1(geoSource_new_2011, 2011)
plot2012_tier = tier_graph1(geoSource_new_2012, 2012)
plot2013_tier = tier_graph1(geoSource_new_2013, 2013)
plot2014_tier = tier_graph1(geoSource_new_2014, 2014)
plot2015_tier = tier_graph1(geoSource_new_2015, 2015)
plot2016_tier = tier_graph1(geoSource_new_2016, 2016)

def plot_year(year):
    curdoc().clear()
    curdoc().add_root(tabs)
    #curdoc().add_root(myLayout2)
    curdoc().add_root(year)

def update_plot1(attr,old,new):
    if (select1.value == "2008"):
        print("2008")
        plot_year(plot2008_tier)
    if (select1.value == "2009"):
        print("2009")
        plot_year(plot2009_tier)
    if (select1.value == "2010"):
        plot_year(plot2010_tier)
    if (select1.value == "2011"):
        plot_year(plot2011_tier)
    if (select1.value == "2012"):
        plot_year(plot2012_tier)
    if (select1.value == "2013"):
        plot_year(plot2013_tier)
    if (select1.value == "2014"):
        plot_year(plot2014_tier)
    if (select1.value == "2015"):
        plot_year(plot2015_tier)
    if (select1.value == "2016"):
        plot_year(plot2016_tier)
        
select1 = Select(title="Please Select Year:", value="fig4", options=[("2008","2008"), 
                                                               ("2009","2009"), 
                                                               ("2010","2010"), 
                                                               ("2011","2011"),
                                                               ("2012","2012"),
                                                               ("2013","2013"),
                                                               ("2014","2014"),
                                                               ("2015","2015"),
                                                               ("2016","2016"),
                                                              ])        
select1.on_change("value",update_plot1)
curdoc().clear()
myLayout2 = layout([[select1]])
tab1 = Panel(child=myLayout1,title="Trafficking countries information")
tab2 = Panel(child=myLayout2,title="Tier information")
tabs = Tabs(tabs=[ tab1, tab2 ])
curdoc().add_root(tabs)
#curdoc().add_root(plot2008_tier)
curdoc().add_root(plot2008)


