import ee
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

def get_soil_data_by_coords(lat, lon, buffer_distance=1000):
    try:
        # Create a point geometry from lat/lon
        point = ee.Geometry.Point([lon, lat])

        # Create a buffer around the point (in meters)
        region_of_interest = point.buffer(buffer_distance)

        # Use the correct dataset ID
        soil_data = ee.Image("OpenLandMap/SOL/SOL_ORGANIC-CARBON_USDA-6A1C_M/v02")

        # Select the surface layer (0cm depth)
        surface_soil = soil_data.select('b0')

        # Clip to region of interest
        clipped_data = surface_soil.clip(region_of_interest)

        return clipped_data

    except Exception as e:
        print(f"Error getting soil data: {e}")
        return None
def classify_land_use(soc):
    """
    Classifies land use based on Soil Organic Carbon (SOC) in g/kg.
    Values are scaled by a factor of 5, so adjust thresholds accordingly.
    """
    soc_scaled = soc / 5  # Adjust SOC to original scale
    if soc_scaled > 20:
        return ["Agriculture", "Forestry", "Grazing/Livestock"]
    elif 10 <= soc_scaled <= 20:
        return ["Horticulture", "Recreation", "Wildlife Habitats"]
    elif soc_scaled < 10:
        return ["Construction", "Landfill Sites", "Road Construction"]
    else:
        return ["Unknown"]
def classify_land_use(soc):
    """
    Classifies land use based on Soil Organic Carbon (SOC) in g/kg.
    SOC values are scaled by a factor of 5.
    """
    soc_scaled = soc / 5  # Adjust SOC to the original scale
    if soc_scaled > 20:
        return ["Agriculture", "Forestry", "Grazing/Livestock"]
    elif 10 <= soc_scaled <= 20:
        return ["Horticulture", "Recreation", "Wildlife Habitats"]
    elif soc_scaled < 10:
        return ["Construction", "Landfill Sites", "Road Construction"]
    else:
        return ["Unknown"]

def Findmain(lat,lon):
    ee.Initialize(project='stalwart-veld-298716')
    TextSum=''
    try:


        print(f"Fetching soil data for coordinates:")
        print(f"West: {lon}, South: {lat}, East: {lon+0.1}, North: {lat+0.1}")

        soil_data = get_soil_data_by_coords(lat, lon)

        if soil_data:
            # Get the mean SOC value for the region
            stats = soil_data.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=soil_data.geometry(),
                scale=30,
                maxPixels=1e6
            ).getInfo()

            soc_value = stats.get('b0', None)
            if soc_value:
                TextSum+=(f"Average SOC Value (scaled): {soc_value}")

                # Classify the land use based on SOC value
                land_use = classify_land_use(soc_value)
                TextSum+=(f"Based on SOC, the land is suitable for: {land_use}")
            else:
                TextSum+=("SOC value could not be retrieved.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    return  TextSum

