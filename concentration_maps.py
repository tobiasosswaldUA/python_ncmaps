print("loading modules")
import cartography_functions as cf
import os
import numpy as np
print("modules loaded")

#nc_fname = "/CESAM/GEMAC2/carlagama/CHIMERE_PACOPAR_FIRES/PACOPAR03/out.2021030100_24_PACOPAR03.nc"
nc_fname = "/CESAM/GEMAC2/tobias/MOST_disperfire/CONdf_0000_20210301_01_PPM_coa.nc"
#nc_fname = "/CESAM/GEMAC2/tobias/FirEUrisk_emiFuture/futureFEMISSIONS_FireC_ssp126_ACCESS-CM2_BASE.nc"
#nc_fname = "/CESAM/GEMAC2/tobias/MOST_disperfire/EMIdf_0000_20210301_01_PPM_coa.nc"

#nc_xvar = "lon"
nc_xvar = "UTMx"

#nc_yvar = "lat"
nc_yvar = "UTMy"

#nc_var = "NO2"
nc_var = "Conc"
#nc_var = "EMI"
#nc_var = "PM10"

nc_crs = "CRS"
nc_tdim = "Time"
#nc_tdim = None 
nc_ntime = 0
nc_btdim = "bottom_top"
nc_nlevel = 5
#nc_nlevel = 0 

#map_projection = "PlateCarree"
map_projection = "original"

cblabel = r"PM10 $g m^{-2}$"

## DON'T TOUCH THIS (or do)

if nc_tdim == None: nc_ntime = None
if nc_btdim == None: nc_nlevel = None
savename = os.path.basename(nc_fname)[:-3]
savename = "%s_%s_%s_%s.pdf"%(savename,nc_ntime,nc_nlevel,nc_var)

print("Reading dataset")
x, y, z, crs_data = cf.read_netcdf_2D(nc_fname,nc_xvar,nc_yvar,nc_var,nc_tdim=nc_tdim,
    nc_ntime=nc_ntime,nc_btdim=nc_btdim,nc_nlevel=nc_nlevel)

print("Plotting")
ax = cf.make_map(x,y,z,crs_data,savename,map_projection=map_projection,draw_gridlines=False,draw_coast=False,
    draw_rivers=False,draw_roads=False,draw_bnational=False,draw_bregional=False,draw_cities=False,
    draw_lakes=False,shp=cf.shp,draw_scalebar=True,sb_length=0.1,colormap="plasma_r")

print("Making Colorbar")
cb_savename = "%s_colorbar.pdf"%savename[:-4]
cf.make_colorbar(ax,cb_savename,label=cblabel)
