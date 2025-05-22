import pandas as pd
import openrouteservice

# Load Excel
df = pd.read_excel("your_file.xlsx")  # Replace with actual filename

# Initialize ORS client with your actual API key
client = openrouteservice.Client(key='PASTE_YOUR_API_KEY_HERE')

# Coordinates: (longitude, latitude)
def get_distance(row):
    try:
        coords = [
            (row["Ophaal longitude"], row["Ophaal latitude"]),
            (row["Afzet longitude"], row["Afzet latitude"])
        ]

        route = client.directions(coords, profile='driving-car', format='geojson')
        distance_meters = route['features'][0]['properties']['segments'][0]['distance']
        return round(distance_meters / 1000, 2)  # Convert to km

    except Exception as e:
        print(f"Error for row {row.name}: {e}")
        return None

# Apply to each row
df["Driving Distance (km)"] = df.apply(get_distance, axis=1)

# Save results
df.to_excel("output_with_driving_distance.xlsx", index=False)
