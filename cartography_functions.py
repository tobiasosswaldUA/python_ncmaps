import cartopy.crs as ccrs
from math import floor
import matplotlib.pyplot as plt
import matplotlib
import geopandas as gp
import xarray as xr
import numpy as np
import pyproj as proj 

# Locations of shapefiles to plot features. Features can be downloaded with download_features.sh
shp = {
"rivers":"shp_features/ne_10m_rivers_lake_centerlines_scale_rank.shp",
"roads":"shp_features/ne_10m_roads.shp",
"bnational":"shp_features/ne_10m_admin_0_boundary_lines_land.shp",
"bregional":"shp_features/ne_10m_admin_1_states_provinces_lines.shp",
"coast":"shp_features/ne_10m_coastline.shp",
"cities":"shp_features/ne_10m_populated_places.shp",
"lakes":"shp_features/ne_10m_lakes.shp"
}

def make_map(x,y,z,crs_in,save_name,map_projection="original",colormap="jet",
    draw_scalebar=False,sb_length=10,draw_gridlines=False,draw_rivers=False,draw_roads=False,
    draw_bnational=False,draw_bregional=False,draw_coast=False,draw_cities=False,
    draw_lakes=False,shp=None, lw_fac=1.0):
    """
    create and save a map of a 2D variable.
    x,y: the geo coordinates in crs_in units. 2D arrays.
    z: the values of the variable being plotted
    crs_in: the proj string of the CRS of the input data
    save_name: the path w/ basename of the output file with extension. extension determines format
    map_projection: original (crs_in) or PlateCarree
    colormap: a matplotlib colormap name
    draw_*: boolean. Weather to draw a given element over the colormap of z.
        most are features like roads and borders etc...
        bnational and bregional are the national and regional boundaries.
        scalebar includes a north arrow.
    lw_fac: a factor for the line weights of the features
    sb_length: the length, in km of the scalebar
    shp: a dict with the file locations of the shapefiles for the features.
        This variable is part of this module. A bash script is available for
        downloading all the necessary files.
    """
    if map_projection == "original": # do not transform coordiantes
        ax_projection = "rectilinear"
        crs_features = crs_in
    elif map_projection == "PlateCarree": # transfrom coordinates if crs_in available
        ax_projection = ccrs.PlateCarree()
        crs_features = "EPSG:4326"
        if crs_in is None: 
            print(" Could not find CRS of data to plot. Assuming coordinates are"
                    " in lat lon (EPSG:4326). Will not transform.")
        else:
            print(" Transforming coordinates from %s to %s"%(crs_in,crs_features))
            trafo_in2map = proj.Transformer.from_crs(
                crs_in, crs_features, always_xy=True)
            x = x.flatten()
            y = y.flatten()
            x, y = trafo_in2map.transform(x, y)
            x = x.reshape(z.shape)
            y = y.reshape(z.shape)
            print(" Summary histograms of new coordinates:\nx:\n%s\ny:\n%s"%(
                np.histogram(x)[1],np.histogram(y)[1]))
    # make the plot
    ax = plt.axes(projection=ax_projection,aspect="equal")
    ax.set_xlim(left=np.min(x),right=np.max(x))
    ax.set_ylim(bottom=np.min(y),top=np.max(y))
    cont = ax.pcolormesh(x,y,z,cmap=colormap,rasterized=True) # rasterize to reduce image size
    # cartopy removes tick labels from axes, have to add them again
    if map_projection == "PlateCarree":
        ax.gridlines(crs=ax_projection,draw_labels=True,lw=0)
    # add the features requested
    if draw_rivers:     ax = add_feature(ax,shp["rivers"],crs_features,zorder=2,
        color="deepskyblue", width=0.7*lw_fac)
    if draw_roads:      ax = add_feature(ax,shp["roads"],crs_features,zorder=5,
        color="firebrick", width=0.7*lw_fac)
    if draw_bnational:  ax = add_feature(ax,shp["bnational"],crs_features,zorder=7,
        color="black",width=1.0*lw_fac)
    if draw_bregional:  ax = add_feature(ax,shp["bregional"],crs_features,zorder=6,
        color="black",width=0.7*lw_fac)
    if draw_coast:      ax = add_feature(ax,shp["coast"],crs_features,zorder=4,
        color="darkblue", width=1.0*lw_fac)
    if draw_cities:     ax = add_feature(ax,shp["cities"],crs_features,zorder=8,
        color="black",width=1.5*lw_fac)
    if draw_lakes:      ax = add_feature(ax,shp["lakes"],crs_features,zorder=3,
        color="deepskyblue", width=0.7*lw_fac)
    # add the scalebar if requested
    if draw_scalebar:
        if sb_length < 1:
        # display units in meters
            sb_length = sb_length * 1000
            sb_unit = "m"
            sb_munit = 1
        else:
        # in km
            sb_unit = "km"
            sb_munit = 1000
        # decide onto which projection to plot the scalebar
        if ax_projection == "rectilinear":
            print(" Scalebar: when using map_projection=original I don't assume anything about the map projection.")
            sb_proj = None
        else:
            sb_proj =  ax_projection
        # plot the scale bar and north arrow
        scale_bar(ax, sb_proj, sb_length, m_per_unit=sb_munit, units=sb_unit)
    # add the gridlines if requested
    if draw_gridlines:
        if map_projection == "original":
            # use matplotlib functions
            plt.grid(lw=0.6,color="k")
        else:
            # use cartopy functions
            ax.gridlines(crs=ax_projection,draw_labels=True,lw=0.6,color="k")    
    # save the figure
    plt.savefig(save_name)
    print("Saved plot to %s"%save_name) 
    return True

def add_feature(ax,shp_file,crs="EPSG:4326",zorder=0.5,color="gray",width=1.5):
    """
    add a feature to the map from a shapefile.
    ax: the axis object on which to add the feature
    shp_file: the path to the shape file of the feature to be plotted
    crs: the coordinate reference system of the map in ax (map is assumed lat lon if crs is not defined)
    zorder: motplotlib zorder of the feature. low zorder features are plotted below high zorder ones.
    color: the color used for plotting the feautre
    width: the width of the line or size of the points (e.g cities) with which to plot the features.
    """
    feature = gp.read_file(shp_file)
    feature.to_crs(crs=crs,inplace=True)
    feature.plot(color=color,ax=ax,linewidth=width,markersize=width,zorder=zorder)
    print(" added feature %s"%shp_file)
    return ax

def read_netcdf_2D(nc_fname,nc_xvar,nc_yvar,nc_var,nc_tdim=None,nc_ntime=0,
    nc_btdim=None,nc_nlevel=0,nc_crsdim="CRS"):
    """
    extract coordinates, coordinate reference system proj string and values of a
    netcdf variable. time dimension and bottom_top are assumed non existent unless
    specified. If specified extract var at nc_ntime and nc_nlevel
    nc_fname: the netcdf file name
    nc_xvar, nc_yvar: are the names of the netcdf variables of x, y coordinates
    nc_var: the name of the variable we want to extract
    nc_tdim: the name of the netcdf dimension time
    nc_ntime: the time step (int) from which to extract the values of nc_var to plot
    nc_btdim: name of nc bottom_top dimension
    nc_nlevel: the height (int) at which to extract var
    nc_crsdim: name of nc global attribute containing proj string of netcdf coordinate ref system
    """
    # read the necessary variables and dims from netcdf file    
    data = xr.open_dataset(nc_fname)
    x = data[nc_xvar]
    y = data[nc_yvar]
    z = data[nc_var]
    if nc_crsdim in data.attrs:
        crs = str(data.attrs[nc_crsdim])
    else:
        crs = None
    # check consistency of inputs with dimesnion of z
    if (z.ndim == 4 and (nc_tdim == None or nc_btdim == None)):
        print(__file__ + ": nc_btdim or nc_tdim are not defined. array dimension may be awkward.")
    elif (z.ndim == 3 and (nc_tdim == None and nc_btdim == None)):
        print(__file__ + ": nc_btdim and nc_tdim are not defined. array dimension may be awkward.")
    elif (z.ndim == 2 and (nc_tdim != None or nc_btdim != None)):
        print(__file__ + ": nc_btdim or nc_tdim are defined,but nc array is 2D??")
    # subsample z
    if nc_tdim != None:
        z = z.isel({nc_tdim:nc_ntime})
    if nc_btdim != None:
        z = z.isel({nc_btdim:nc_nlevel})
    data.close()
    # convert data format of outputs
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    # return the x, y, z 2D arrays and the crs string if it was found (None otherwise)
    print(" Summary histograms of netcdf data:\n    x:\n    %s\n    "
                "y:\n   %s\n    variable:   \n %s\n    CRS:\n  %s"%(
       np.histogram(x)[1],np.histogram(y)[1],np.histogram(z)[1],crs))
    return x,y,z,crs
    

def utm_from_lon(lon):
    """
    utm_from_lon - UTM zone for a longitude
    Not right for some polar regions (Norway, Svalbard, Antartica)
    :param float lon: longitude
    :return: UTM zone number
    :rtype: int
    """
    return floor( ( lon + 180 ) / 6) + 1

def scale_bar(ax, proj, length, location=(0.5, 0.05), linewidth=3,
              units='km', m_per_unit=1000):
    """
    http://stackoverflow.com/a/35705477/1072212 (modified)
    ax is the axes to draw the scalebar on.
    proj is the projection the axes are in
    location is center of the scalebar in axis coordinates ie. 0.5 is the middle of the plot
    length is the length of the scalebar in km.
    linewidth is the thickness of the scalebar.
    units is the name of the unit being displayed
    m_per_unit is the number of meters in a unit
    """
    if proj is not None:
        # find lat/lon center to find best UTM zone
        x0, x1, y0, y1 = ax.get_extent(proj.as_geodetic())
        # Projection in metres
        utm = ccrs.UTM(utm_from_lon((x0+x1)/2))
        trans_arg = {"transform":utm}
        # Get the extent of the plotted area in coordinates in metres
        x0, x1, y0, y1 = ax.get_extent(utm)
    else:
        print(" Could not obtain crs for scalebar, assuming axes are in meters")
        x0,x1 = ax.get_xlim()
        y0,y1 = ax.get_ylim()
        utm = None
        trans_arg = {} 
    # Turn the specified scalebar location into coordinates in metres
    sbcx, sbcy = x0 + (x1 - x0) * location[0], y0 + (y1 - y0) * location[1]
    # Generate the x coordinate for the ends of the scalebar
    bar_xs = [sbcx - length * m_per_unit/2, sbcx + length * m_per_unit/2]
    print(" Plotting scalebar at:")
    print("     x0,x1,y0,y1",x0,x1,y0,y1)
    print("     sbcx, sbcy",sbcx, sbcy)
    print("     bar_xs",bar_xs)
    # Plot the scalebar 
    ax.plot(bar_xs, [sbcy, sbcy], color='k',
        linewidth=linewidth, **trans_arg)
    # Add text under scalebar
    ax.annotate("\n"+str(int(length)) + ' ' + units, size=linewidth*3,
            xy=(sbcx, sbcy), xytext=(0., -1.5*linewidth*3), textcoords='offset points', 
            horizontalalignment='center', verticalalignment='bottom', **trans_arg)
    # Plot the N arrow
    left = x0+(x1-x0)*0.05
    t1 = ax.text(left, sbcy, u'\u25B2\nN', horizontalalignment='center', 
        verticalalignment='bottom', **trans_arg)


