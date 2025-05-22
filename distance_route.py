import pandas as pd
import openrouteservice
import time

# Load Excel
df = pd.read_excel("Ontbrekende addressen.xlsx")  # Replace with actual filename

# Initialize ORS client with your actual API key
client = openrouteservice.Client(key='5b3ce3597851110001cf62480e276e63b181490ab949324335adc417')

# Coordinates: (longitude, latitude)
def get_distance(row):
    try:
        coords = [
            (row["Ophaal longitude"], row["Ophaal latitude"]),
            (row["Afzet longitude"], row["Afzet latitude"])
        ]
        route = client.directions(coords, profile='driving-car', format='geojson')
        distance_meters = route['features'][0]['properties']['segments'][0]['distance']
        time.sleep(2.1)  # ← add a 1.5 second pause per request
        return round(distance_meters / 1000, 2)

    except Exception as e:
        print(f"Error for row {row.name}: {e}")
        return None

# Apply to each row
df["Driving Distance (km)"] = df.apply(get_distance, axis=1)

# Save results
df.to_excel("output_with_driving_distance_ontbrekende_adressen.xlsx", index=False)
