#!/bin/bash

# This will download the necessary features for cartography_functions.py. The features can then be plotted
# onto the maps before saving them using add_feature. Features include borders, roads, rivers, etc...

# List of URLs
urls=(
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_physical/ne_10m_coastline.cpg"
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_physical/ne_10m_coastline.dbf"
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_physical/ne_10m_coastline.prj"
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_physical/ne_10m_coastline.shp"
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_physical/ne_10m_coastline.shx"
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_cultural/ne_10m_admin_0_boundary_lines_land.cpg"
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_cultural/ne_10m_admin_0_boundary_lines_land.dbf"
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_cultural/ne_10m_admin_0_boundary_lines_land.prj"
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_cultural/ne_10m_admin_0_boundary_lines_land.shp"
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_cultural/ne_10m_admin_0_boundary_lines_land.shx"
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_cultural/ne_10m_admin_1_states_provinces_lines.cpg"
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_cultural/ne_10m_admin_1_states_provinces_lines.dbf"
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_cultural/ne_10m_admin_1_states_provinces_lines.prj"
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_cultural/ne_10m_admin_1_states_provinces_lines.shp"
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_cultural/ne_10m_admin_1_states_provinces_lines.shx"
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_cultural/ne_10m_populated_places.cpg"
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_cultural/ne_10m_populated_places.dbf"
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_cultural/ne_10m_populated_places.prj"
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_cultural/ne_10m_populated_places.shp"
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_cultural/ne_10m_populated_places.shx"
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_physical/ne_10m_rivers_lake_centerlines_scale_rank.cpg"
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_physical/ne_10m_rivers_lake_centerlines_scale_rank.dbf"
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_physical/ne_10m_rivers_lake_centerlines_scale_rank.prj"
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_physical/ne_10m_rivers_lake_centerlines_scale_rank.shp"
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_physical/ne_10m_rivers_lake_centerlines_scale_rank.shx"
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_physical/ne_10m_lakes.cpg"
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_physical/ne_10m_lakes.dbf"
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_physical/ne_10m_lakes.prj"
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_physical/ne_10m_lakes.shp"
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_physical/ne_10m_lakes.shx"
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_cultural/ne_10m_roads.cpg"
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_cultural/ne_10m_roads.dbf"
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_cultural/ne_10m_roads.prj"
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_cultural/ne_10m_roads.shp"
"https://github.com/nvkelso/natural-earth-vector/raw/master/10m_cultural/ne_10m_roads.shx"
)

# Loop through each URL in the list and download the file
for url in "${urls[@]}"; do
    # Extract filename from the URL
    filename=$(basename "$url")
    # Use wget to download the file
    wget "$url" -O "$filename"
    echo "Downloaded $filename"
done

echo "All files downloaded successfully to the current directory."


