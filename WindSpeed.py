import requests
from datetime import datetime, timedelta

def get_climate_data(latitude, longitude, start_date=None, end_date=None):

    # If no dates provided, use last 30 days
    if not start_date or not end_date:
        end = datetime.now()
        start = end - timedelta(days=30)
        start_date = start.strftime('%Y%m%d')
        end_date = end.strftime('%Y%m%d')

    # NASA POWER API endpoint
    base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"

    # Parameters for the API request
    params = {
        'parameters': 'ALLSKY_SFC_SW_DWN,WS10M',  # Solar radiation and wind speed
        'community': 'RE',                         # RE = Renewable Energy
        'longitude': longitude,
        'latitude': latitude,
        'start': start_date,
        'end': end_date,
        'format': 'JSON'
    }

    try:
        # Make the API request
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise exception for bad status codes

        data = response.json()

        # Extract the parameters from the response
        properties = data['properties']['parameter']

        # Extract values for solar radiation and wind speed
        solar_values = [v for v in properties['ALLSKY_SFC_SW_DWN'].values() if v >= 0]
        wind_values = [v for v in properties['WS10M'].values() if v >= 0]

        # Check for valid data before averaging
        if not solar_values or not wind_values:
            raise ValueError("No valid data points found for solar radiation or wind speed.")

        avg_solar = sum(solar_values) / len(solar_values)
        avg_wind = sum(wind_values) / len(wind_values)

        return {
            'Solar Radiation': str(round(avg_solar, 2)) + " kWh/m²/day",  # kWh/m²/day
            'Wind Speed': str(round(avg_wind, 2)) + " m/s",        # m/s
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except ValueError as e:
        print(f"Data error: {e}")
        return None

# # Example usage
# def main():
#     # Example coordinates (Warren, NJ)
#     latitude = 40.6
#     longitude = -74.9

#     # Get climate data
#     result = get_climate_data(latitude, longitude)

#     if result:
#         print(f"\nClimate Data Results:")
#         print(f"Average Solar Radiation: {result['solar_radiation']} kWh/m²/day")
#         print(f"Average Wind Speed: {result['wind_speed']} m/s")
#     else:
#         print("Failed to retrieve climate data.")

# if __name__ == "__main__":
#     main()