print("loading modules")
import cartography_functions as cf
import os
import numpy as np
print("modules loaded")

#nc_fname = "/CESAM/GEMAC2/carlagama/CHIMERE_PACOPAR_FIRES/PACOPAR03/out.2021030100_24_PACOPAR03.nc"
#nc_fname = "/CESAM/GEMAC2/tobias/MOST_disperfire/CONdf_0000_20210301_01_PPM_coa.nc"
#nc_fname = "/CESAM/GEMAC2/tobias/FirEUrisk_emiFuture/futureFEMISSIONS_FireC_ssp126_ACCESS-CM2_BASE.nc"
#nc_fname = "/CESAM/GEMAC2/tobias/MOST_disperfire/EMIdf_0000_20210301_01_PPM_coa.nc"
#nc_fname = "/CESAM/GEMAC2/tobias/APIFLAME_data/sweden_2014/EMISSIONS/FIRE_EMISS_SE05/AB_FRP_MODIS/SE05_gridded/AB_FRP_veg_grid_201408_SE05_forplot_nc4.nc" 
#nc_fname = "/CESAM/GEMAC2/tobias/FirEUrisk_sweden/chimere_v2020r1_ERA5/OUT_sweden/SE05_API/data_SE05_SE05_API/total_column_CO/FEMISSIONS.2014073100_24_SE05_API.nc" 
nc_fname = "/CESAM/GEMAC2/tobias/FirEUrisk_emiFuture/futureFEMISSIONS_FireC_ssp126_ACCESS-CM2_SPITFIRE.nc"
#nc_fname = __RUN__ 

nc_xvar = "lon"
#nc_xvar = "UTMx"

nc_yvar = "lat"
#nc_yvar = "UTMy"

#nc_var = "NO2"
nc_var = "CO"
#nc_var = "Conc"
#nc_var = "EMI"
#nc_var = "EMIstart"
#nc_var = "PM10"
#nc_var = "AB_MCD64"
#nc_var = "PM25"

nc_crs = "CRS"

nc_tdim = "Time"
#nc_tdim = None
#nc_tdim = "Times" 
#nc_tdim = "TIME" 

nc_ntime = 1215
#nc_ntime = __RUN__
#nc_ntime = None
#nc_ntime = __TIM__
#nc_ntime = int(nc_ntime)

#nc_btdim = "bottom_top"
nc_btdim = None 

#nc_nlevel = 5
nc_nlevel = 0 

map_projection = "PlateCarree"
#map_projection = "original"

#cblabel = r"Emission start [s]"
#cblabel = r"%s emission 2070-2100 [$g/m^2$]"%nc_var
#cblabel = r"Daily CO emission [$g m^{-2}$]"
#cblabel = r"Daily CO emission [$g m^{-2}$]"
#cblabel = "Concentration of "+nc_var+r" [$\mu g\; m^{-3}$]"
#cblabel = "Concentration of "+"PM2.5"+r" [$\mu g\; m^{-3}$]"
cblabel = r"Change in Carbon Emissions [$\%$]"

vmin = -300
#vmin = None
#vmax = 4000
vmax = 300
#vmax = None
#colormap = "autumn_r"
#colormap = "plasma_r"
colormap = "RdBu_r"

title = None
#title = nc_fname[-25:-21]+"-"+nc_fname[-21:-19]+"-"+nc_fname[-19:-17]
#title = title +"  %0.2i:00"%nc_ntime

## DON'T TOUCH THIS (or do)

if nc_tdim == None: nc_ntime = None
if nc_btdim == None: nc_nlevel = None
savename = os.path.basename(nc_fname)[:-3]
savename = "%s_%s_%s_%s.png"%(savename,nc_ntime,nc_nlevel,nc_var)

print("Reading dataset")
x, y, z, crs_data = cf.read_netcdf_2D(nc_fname,nc_xvar,nc_yvar,nc_var,nc_tdim=nc_tdim,
    nc_ntime=nc_ntime,nc_btdim=nc_btdim,nc_nlevel=nc_nlevel)

print("Manipulating data")
z = z*100.
z = z[0] # there's a bug here when btdim is none (check z.shape is same as x.shape)
z[z>9.e+36] = None
#z = (28.0101/6.022E23)*(60*60*24)*10E4 * z # molecules CO to g CO, molar mass of CO is 28.0101, 6.02.. is avogadro

print("Plotting")
ax = cf.make_map(x,y,z,crs_data,savename,map_projection=map_projection,draw_gridlines=True,draw_coast=True,
    draw_rivers=False,draw_roads=False,draw_bnational=True,draw_bregional=False,draw_cities=False,
    draw_lakes=False,draw_ocean=True,shp=cf.shp,draw_scalebar=False,sb_length=50,sb_loc=0.1,colormap=colormap,
    vmin=vmin,vmax=vmax,title=title)

print("Making Colorbar")
cb_savename = "%s_colorbar.pdf"%savename[:-4]
cf.make_colorbar(ax,cb_savename,label=cblabel)
