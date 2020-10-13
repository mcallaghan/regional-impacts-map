import shapely
import shapely.vectorized
import re
from itertools import product, combinations

from pycountry_convert import  country_alpha2_to_continent_code, country_alpha3_to_country_alpha2
import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy.crs as ccrs
import cartopy
import geopy
import geopy.distance
import xarray as xr
import seaborn as sns
import geopandas
from scipy.spatial import distance
import cartopy.io.shapereader as shpreader
import numpy as np
import pandas as pd
import time

def match_shp_da(shpfile, ndf, shpfile_name, shp_ndf_df):

    shp_ndf = []

    degrees = abs(ndf.LAT.unique()[1] - ndf.LAT.unique()[0])

    yv, xv = np.meshgrid(ndf.LAT.unique(), ndf.LON.unique())
    xv[xv>180] -= 360

    for i, place in shpfile.iterrows():

        inplace = shapely.vectorized.contains(place.geometry,xv,yv)

        idx = np.argwhere(inplace==True)
        ndots = idx.size/2

        n_attributable_trend = 0
        notna_cells = 0

        if ndots==0:
            c = np.array(place.geometry.centroid)
            lon = c[0]//degrees*degrees+degrees*0.5
            if lon < 0:
                lon+=360
            lat = c[1]//degrees*degrees+degrees*0.5
            da_df = ndf[(ndf['LON']==lon) & (ndf['LAT']==lat)]
            da_cat = da_df['da_cat']
            if da_cat.shape[0]==0:
                print(c)
                print(degrees)
                print(lat, lon)
            shpfile.loc[i, 'gridcells'] = 1
            if abs(da_cat.values[0]) > 1:
                n_attributable_trend +=1
            if not np.isnan(da_cat.values[0]):
                notna_cells +=1
            shpfile.loc[i, 'da_trend_cells'] = n_attributable_trend
            shpfile.loc[i,'da_data_cells'] = notna_cells

            shp_ndf.append({"shpfile_name": shpfile_name, "shpfile_id": i, "ndf_id": da_df.index[0]})

        else:

            ndf_ids = []
            for point in idx:
                lon = ndf.LON.unique()[point[0]]
                lat = ndf.LAT.unique()[point[1]]
                da_df = ndf[(ndf['LON']==lon) & (ndf['LAT']==lat)]

                shp_ndf.append({"shpfile_name": shpfile_name, "shpfile_id": i, "ndf_id": da_df.index[0]})

                ndf_ids.append(da_df.index[0])

                da_cat = da_df['da_cat']

                if abs(da_cat.values[0]) > 1:
                    n_attributable_trend +=1

                if not np.isnan(da_cat.values[0]):
                    notna_cells +=1

        shpfile.loc[i,'gridcells'] = ndots
        shpfile.loc[i,'da_trend_cells'] = n_attributable_trend
        shpfile.loc[i,'da_data_cells'] = notna_cells


    shp_ndf_df = pd.concat([shp_ndf_df, pd.DataFrame.from_dict(shp_ndf)])

    return shpfile, shp_ndf_df

# Load predictions
df = pd.read_csv('../data/1_predicted_category_documents.csv')

# Load locations
places = pd.read_csv('../data/place_df.csv')
places = places.drop_duplicates(["doc_id","geonameid"])

variables = [
    '6 - Temperature - upper_pred','6 - Temperature - mean_prediction','6 - Temperature - lower_pred',
    '6 - Precipitation - upper_pred','6 - Precipitation - mean_prediction','6 - Precipitation - lower_pred',
    "12 - Terrestrial ES - mean_prediction", "12 - Terrestrial ES - mean_prediction", "12 - Terrestrial ES - mean_prediction",
    "12 - Coastal and marine Ecosystems - mean_prediction", "12 - Coastal and marine Ecosystems - mean_prediction", "12 - Coastal and marine Ecosystems - mean_prediction",
    "12 - Mountains, snow and ice - mean_prediction", "12 - Mountains, snow and ice - mean_prediction", "12 - Mountains, snow and ice - mean_prediction",
    "12 - Rivers, lakes, and soil moisture - mean_prediction", "12 - Rivers, lakes, and soil moisture - mean_prediction", "12 - Rivers, lakes, and soil moisture - mean_prediction",
    "12 - Human and managed - mean_prediction", "12 - Human and managed - mean_prediction", "12 - Human and managed - mean_prediction"
    'all',
]


for variable in variables:
    print(f"merging data for {variable}")

    df = pd.read_csv('../data/1_predicted_category_documents.csv')
    if variable != "all":
        df = df[df[variable]>=0.5]
        df = df[df["2 - Trend or climate change attribution - upper_pred"]>=0.5]
    df_places = pd.merge(df,places,left_on="id",right_on="doc_id")

    if "Precipitation" in variable:
        da_degrees=2.5
        da_dataset = (
            xr
            .open_dataset('../data/d_a/9cat.195101-201012.nc')
            .roll(LON=72, roll_coords=True)
        )
        da_arr=np.zeros([72, 144])
        original_values = [4,3,2,1,0,-1,-2,-3,-4]
        arr_vars = ["CP4","CP3","CP2","CP1","CP0","CM1","CM2","CM3","CM4"]
        simplified_values = [3,3,2,1,0,-1,-2,-3,-3]

        da_dataset = da_dataset.to_dataframe()
        for o_v, s_v, arr_var in zip(original_values, simplified_values, arr_vars):
            da_arr[(da_dataset[arr_var].values==o_v).reshape(72, 144)]=s_v
            da_dataset.loc[da_dataset[arr_var].values==o_v, "da_cat"] = s_v
        da_dataset = da_dataset.reset_index()
    else:
        da_degrees=5
        da_dataset = (
            xr
            .open_dataset('../data/d_a/7cat.Fig.10-12.1951-2010.temp_ANN.CMIP5.nc', decode_times=False)
            .roll(LON37_108=72, roll_coords=True)
            .to_dataframe()
        )

        arr_vals = [3,2,1,0,-1,-2,-3]
        arr_vars = ["P3","P2","P1","P0","M1","M2","M3"]

        for val, arr_var in zip(arr_vals, arr_vars):
            da_dataset.loc[da_dataset[arr_var].values==val, "da_cat"] = val

        da_dataset = da_dataset.reset_index().rename(columns={"LON37_108": "LON"})

    for degrees in [2.5, 1]:# .25]:
        t0 = time.time()
        print(f"merging datasets for a grid with {degrees} degree cells")
        LON = np.linspace(-180+degrees*0.5,180-degrees*0.5,int(360/degrees))
        LON[LON<0] += 360
        LAT = np.linspace(-90+degrees*0.5,90-degrees*0.5,int(180/degrees))

        lon_df, lat_df = np.meshgrid(LON,LAT)

        df_places['LAT'] = df_places['lat']//degrees*degrees+degrees*0.5
        df_places['LON'] = df_places['lon']//degrees*degrees+degrees*0.5

        n = df_places.groupby(['LAT','LON']).size().to_frame("n_studies").reset_index()
        n.loc[n['LON']<0,"LON"] = n.loc[n['LON']<0,"LON"] + 360

        ndf = ndf = (
            pd.DataFrame({"LAT": lat_df.ravel(), "LON": lon_df.ravel()})
            .merge(n,how="left")
            .fillna(0)
        )
        ndf["LAT_25"] = ndf['LAT']//da_degrees*da_degrees+da_degrees*0.5
        ndf["LON_25"] = ndf['LON']//da_degrees*da_degrees+da_degrees*0.5
        ndf['order'] = list(ndf.index)

        ndf = ndf.merge(
            da_dataset
            .reset_index()
            .rename(columns={"LAT": "LAT_25", "LON": "LON_25"})
            [["LAT_25","LON_25","da_cat"]],
            how="inner",
            sort=False
        ).sort_values('order').drop(columns="order")

        ndf['index'] = ndf.index

        shp_ndf_df = pd.DataFrame({"shpfile_name": [],"shpfile_id": [], "ndf_id":[]})

        # Countries
        shpfilename = shpreader.natural_earth(resolution='50m',
                              category='cultural',
                              name='admin_0_countries')

        adm0shps = geopandas.read_file(shpfilename)
        adm0shps, shp_ndf_df = match_shp_da(adm0shps, ndf, "adm0shps", shp_ndf_df)

        # Admin1
        shpfilename = shpreader.natural_earth(resolution='10m',
                                              category='cultural',
                                              name='admin_1_states_provinces')

        adm1shps = geopandas.read_file(shpfilename)
        adm1shps, shp_ndf_df = match_shp_da(adm1shps, ndf, "adm1shps", shp_ndf_df)

        # Alternate admin1
        shpfilename = "../data/d_a/gadm36_1.shp"
        adm1shps_alt = geopandas.read_file(shpfilename)
        adm1shps_alt, shp_ndf_df = match_shp_da(adm1shps_alt, ndf, "adm1shps_alt", shp_ndf_df)

        # Geography
        shpfilename = shpreader.natural_earth(resolution='10m',
                                              category='physical',
                                              name='geography_regions_polys')

        geography = geopandas.read_file(shpfilename)

        geography, shp_ndf_df = match_shp_da(geography, ndf, "geography", shp_ndf_df)

        # change names to help match
        geography.loc[(geography["featurecla"]=="Range/mtn") & (geography["name"].str.contains("Altay", case=False)),"name"] = "Altay"
        geography.loc[(geography["featurecla"]=="Range/mtn") & (geography["name"].str.contains("Appalach", case=False)),"name"] = "Appalachian Mountains"
        geography.loc[(geography["featurecla"]=="Range/mtn") & (geography["name"].str.contains("cant", case=False)),"name"] = "Cordillera Cantábrica"
        geography.loc[(geography["featurecla"]=="Range/mtn") & (geography["name"].str.contains("Dabie", case=False)),"name"] = "Dabie Shan"
        geography.loc[(geography["featurecla"]=="Range/mtn") & (geography["name"].str.contains("EASTERN GHATS", case=False)),"name"] = "Eastern Ghāts"
        geography.loc[(geography["featurecla"]=="Range/mtn") & (geography["name"].str.contains("WESTERN GHATS", case=False)),"name"] = "Western Ghāts"
        geography.loc[(geography["featurecla"]=="Range/mtn") & (geography["name"].str.contains("kunlun", case=False)),"name"] = "Kalakunlun Shan"
        geography.loc[(geography["featurecla"]=="Range/mtn") & (geography["name"].str.contains("LEN MOUNTAIN", case=False)),"name"] = "Kölen"
        geography.loc[(geography["featurecla"]=="Range/mtn") & (geography["name"].str.contains("Taihang Mts.", case=False)),"name"] = "Taihang Shan"
        geography.loc[(geography["featurecla"]=="Range/mtn") & (geography["name"].str.contains("Tatra Mts.", case=False)),"name"] = "Tatry"
        geography.loc[(geography["featurecla"]=="Range/mtn") & (geography["name"].str.contains("TIAN SHAN", case=False)),"name"] = "Tien Shan"
        geography.loc[(geography["featurecla"]=="Range/mtn") & (geography["name"].str.contains("andes", case=False)),"name"] = "Andes Mountains"
        geography.loc[(geography["featurecla"]=="Range/mtn") & (geography["name"].str.contains("HINDU KUSH", case=False)),"name"] = "Hindū Kush"
        geography.loc[(geography["featurecla"]=="Range/mtn") & (geography["name"].str.contains("Marrah Mts", case=False)),"name"] = "Jabal Marrah"
        geography.loc[(geography["featurecla"]=="Range/mtn") & (geography["name"].str.contains("Lebanon", case=False)),"name"] = "Mount Lebanon"
        geography.loc[(geography["featurecla"]=="Range/mtn") & (geography["name"].str.contains("KARAKORAM RA", case=False)),"name"] = "Karakorum Shan"

        geography.loc[(geography["featurecla"]=="Desert") & (geography["name"].str.contains("Negev", case=False)), "name"] = "Negev"
        geography.loc[(geography["featurecla"]=="Desert") & (geography["name"].str.contains("Atacama", case=False)), "name"] = "Atacama Desert"
        geography.loc[(geography["featurecla"]=="Desert") & (geography["name"].str.contains("CHIHUAHUAN DESERT", case=False)), "name"] = "Chihuahua Desert"
        geography.loc[(geography["featurecla"]=="Desert") & (geography["name"].str.contains("Lut desert", case=False)), "name"] = "God-e Lut"
        geography.loc[(geography["featurecla"]=="Desert") & (geography["name"].str.contains("TAKLIMAKAN DESERT", case=False)), "name"] = "Takla Makan Desert"


        geography.loc[(geography["featurecla"]=="Plateau") & (geography["name"].str.contains("mongol", case=False)), "name"] = "Nei Mongol Gaoyuan"
        geography.loc[(geography["featurecla"]=="Plateau") & (geography["name"].str.contains("deccan", case=False)), "name"] = "Deccan"
        geography.loc[(geography["featurecla"]=="Plateau") & (geography["name"].str.contains("chota", case=False)), "name"] = "Chota Nāgpur Plateau"
        geography.loc[(geography["featurecla"]=="Plateau") & (geography["name"].str.contains("loess", case=False)), "name"] = "Huangtu Gaoyuan"
        geography.loc[(geography["featurecla"]=="Plateau") & (geography["name"].str.contains("khorat", case=False)), "name"] = "Khorat Plateau"
        geography.loc[(geography["featurecla"]=="Plateau") & (geography["name"].str.contains("tibet", case=False)), "name"] = "Qing Zang Gaoyuan"
        geography.loc[(geography["featurecla"]=="Plateau") & (geography["name"].str.contains("polar", case=False)), "name"] = "South Polar Plateau"
        geography.loc[(geography["featurecla"]=="Plateau") & (geography["name"].str.contains("YUNGUI", case=False)), "name"] = "Yungui Gaoyuan"


        adm0shps.loc[adm0shps.NAME.str.contains("Kosovo"),"ADM0_A3"] = "XKX"
        adm0shps.loc[adm0shps.NAME.str.contains("S. Sudan"),"ADM0_A3"] = "SSD"



        geography.loc[
            (geography["featurecla"]=="Plateau") & (geography["name"].str.contains("cumberland", case=False)),["name","featurecla"]
        ] = ["Cumberland Plateau", "Plain"]
        geography.loc[
            (geography["featurecla"]=="Plateau") & (geography["name"].str.contains("colorado", case=False)),["name","featurecla"]
        ] = ["San Francisco Plateau", "Plain"]
        geography.loc[(geography["featurecla"]=="Plain") & (geography["name"].str.contains("gange", case=False)),"name"] = "Gangetic Plain"
        geography.loc[(geography["featurecla"]=="Plain") & (geography["name"].str.contains("north china", case=False)),"name"] = "Huanghuai Pingyuan"
        
        
        ##### Oceans
        shpfilename = shpreader.natural_earth(resolution='10m',
                                              category='physical',
                                              name='geography_marine_polys')

        ocean = geopandas.read_file(shpfilename)

        ocean = ocean[pd.notna(ocean['name'])]

        ocean, shp_ndf_df = match_shp_da(ocean, ndf, "ocean", shp_ndf_df)
        ocean.head()


        # A list of combinations of studies and gridcells
        df_ndf = pd.DataFrame({"ndf_id": [], "doc_id": []})

        df["df_da"] = None
        df["gridcells"] = None
        df["da_trend_cells"] = None
        df["da_data_cells"] = None
        df["feature_type"] = None

        feature_mapping = {
            "MTS": {"shpfile": geography, "shpfile_name": "geography", "featurecla_list": ["Range/mtn"]},
            "PLAT": {"shpfile": geography, "shpfile_name": "geography", "featurecla_list": ["Plateau"]},
            "PLN": {"shpfile": geography, "shpfile_name": "geography", "featurecla_list": ["Plain"]},
            "DSRT": {"shpfile": geography, "shpfile_name": "geography", "featurecla_list": ["Desert"]},
            "OCN": {"shpfile": ocean, "shpfile_name": "ocean", "featurecla_list": ["ocean"]},
            "SEA": {"shpfile": ocean, "shpfile_name": "ocean", "featurecla_list": ["sea", "bay"]},
            "GULF": {"shpfile": ocean, "shpfile_name": "ocean", "featurecla_list": ["gulf","bay"]},
            "BAY": {"shpfile": ocean, "shpfile_name": "ocean", "featurecla_list": ["gulf","bay"]},
            "CHN": {"shpfile": ocean, "shpfile_name": "ocean", "featurecla_list": ["channel"]},
            "BSNU": {"shpfile": geography, "shpfile_name": "geography", "featurecla_list": ["basin"]},
            "ADM1": {"shpfile": adm1shps, "shpfile_name": "adm1shps", "featurecla_list": None},
            "PCLI": {"shpfile": adm0shps, "shpfile_name": "adm0shps", "featurecla_list": None},
        }

        # For each type of feature
        for i, (key, value) in enumerate(feature_mapping.items()):
            print(f"matching {key} features")

            # Get the study places with this type of feature
            sub_df = df_places.loc[df_places["feature_code"]==key]

            # Cycle through each place name
            for name, group in sub_df.groupby('place_name'):

                # How many studies are there with this placename
                n = len(group.doc_id.unique())

                # Get the matching shapefile
                shp = value["shpfile"]
                if value["featurecla_list"] is not None:
                    sub_shp = shp[
                        (shp["featurecla"].isin(value["featurecla_list"])) &
                        (shp["name"].str.lower().str.replace("mts.","mountains",regex=False)==name.lower().replace("mts.","mountains").strip())
                    ]
                else:
                    if "gn_id" in shp.columns:
                        sub_shp = shp[shp["gn_id"]==group.geonameid.values[0]]
                    else:
                        sub_shp = shp[shp["ADM0_A3"]==group.country_predicted.values[0]]

                if sub_shp.shape[0]==0:
                    if key=="ADM1":
                        sub_shp = adm1shps_alt[
                            (adm1shps_alt["NAME_1"]==group.place_name.values[0]) |
                            (adm1shps_alt["VARNAME_1"].str.contains(group.place_name.values[0]))
                        ]

                # If there is no matching shapefile, move on
                if sub_shp.shape[0]==0:
                    continue

                else:
                    # As long as this is the smallest feature in the document, give it a df_da value which
                    # is the number of cells with a d&a signal divided by the total number of cells in the feature
                    grid_vars = [
                        sub_shp.gridcells.values[0],
                        sub_shp.da_data_cells.values[0],
                        sub_shp.da_trend_cells.values[0],
                        key
                    ]
                    for did in group.doc_id.unique():
                        ps = df.loc[df['id']==did]
                        if not pd.isna(ps['gridcells'].values[0]):
                            if ps['gridcells'].values[0] < sub_shp.gridcells.values[0]:
                                continue
                        df.loc[
                            df['id']==did,
                            ["gridcells","da_data_cells", "da_trend_cells", "feature_type"]
                        ] = grid_vars

                        # These are the relevant grid indices
                        ndf_ids = shp_ndf_df.loc[
                            (shp_ndf_df["shpfile_name"]==value["shpfile_name"]) &
                            (shp_ndf_df["shpfile_id"]==sub_shp.index[0]),
                            "ndf_id"
                        ]

                        # Add these grid indices-this document combinations to our
                        # doc-grid indices dataframe
                        sub_df_ndf = pd.DataFrame.from_dict({"ndf_id": ndf_ids, "doc_id": [did]*len(ndf_ids)})
                        df_ndf = df_ndf[df_ndf["doc_id"]!=did].append(sub_df_ndf)

            print(f"{df_ndf.shape} doc-grid combinations")
        # These documents don't have a location
        no_loc_id = df.loc[pd.isna(df['gridcells']),"id"]

        # These documents don't have a location, or have a feature type not in
        # the ones above
        df_da = df_places[
            (~df_places["feature_code"].isin(feature_mapping.keys())) | (df_places["doc_id"].isin(no_loc_id))
        ][["doc_id","LAT","LON"]]

        # Deal with longitude centering
        df_da.loc[df_da["LON"]<0,"LON"]+=360

        # Merge this database with the grid database by lat and lon
        df_da = df_da.merge(ndf[["LAT","LON","da_cat","index"]])
        df_da["da_trend_cells"] = np.where(abs(df_da["da_cat"])>1,1,0)
        df_da["da_data_cells"] = np.where(~pd.isna(df_da["da_cat"]),1,0)
        df_da["gridcells"] = 1

        # Sum the cell types across all locations in a study
        df_da_study = df_da.groupby("doc_id")[['da_trend_cells','da_data_cells','gridcells']].sum().reset_index()

        # For each of these studies
        for i, row in df_da_study.iterrows():
            # Set the doc level database to have these summed cell types
            df.loc[
                df["id"]==row["doc_id"],
                ["gridcells","da_trend_cells","da_data_cells","feature_type"]
            ] = [row["gridcells"], row["da_trend_cells"], row['da_data_cells'], "OTHER"]

            # Add these grid indices to the doc-grid combination dataframe
            ndf_ids = df_da.loc[
                (df_da["doc_id"]==row["doc_id"]),
                "index"
            ]
            sub_df_ndf = pd.DataFrame.from_dict({"ndf_id": ndf_ids, "doc_id": [row["doc_id"]]*len(ndf_ids)})
            #df_ndf = df_ndf[df_ndf["doc_id"]!=did].append(sub_df_ndf)
            df_ndf = df_ndf.append(sub_df_ndf)

        ndf["n_study_prop"] = 0

        for did, group in df_ndf.groupby("doc_id"):
            ndf.loc[ndf["index"].isin(group["ndf_id"]),"n_study_prop"]+=1/group.shape[0]

        df.to_csv(f'../data/study_da_{variable}_{degrees}.csv', index=False)
        ndf.to_csv(f'../data/gridcell_studies_{variable}_{degrees}.csv', index=False)
        df_ndf.to_csv(f'../data/study_gridcell_{variable}_{degrees}.csv', index=False)
        print(time.time()-t0)
