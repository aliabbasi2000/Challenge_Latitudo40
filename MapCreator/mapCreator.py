import folium
import pandas as pd
import branca.colormap as cm

# Read data from the text file
file_path = 'carbon_sequestration_dataset.txt'
df = pd.read_csv(file_path)

# Strip any whitespace from the column names
df.columns = df.columns.str.strip()

# Create a colormap using branca
colormap = cm.LinearColormap(
    colors=['lightcoral', 'red', 'darkred'],
    vmin=df['CARBON_SEQUESTRATION'].min(),
    vmax=df['CARBON_SEQUESTRATION'].max(),
    caption='CARBON SEQUESTRATION'
)

# Create a folium map centered around Torino
m = folium.Map(location=[45.0703, 7.6869], zoom_start=13)

# Add markers to the map
for idx, row in df.iterrows():
    popup_text = (
        f"Tree Id: {row['Id']}<br>"
        f"Tree Species: {row['Species']}<br>"
        f"Carbon Storage: {row['CARBON_SEQUESTRATION']} kg"
    )
    folium.CircleMarker(
        location=(row['Latitude'], row['Longitude']),
        radius=10,  # Larger radius for bigger points
        color=colormap(row['CARBON_SEQUESTRATION']),
        fill=True,
        fill_color=colormap(row['CARBON_SEQUESTRATION']),
        fill_opacity=0.6,
        popup=popup_text
    ).add_to(m)

# Add the colormap to the map
colormap.add_to(m)

# Save the map to an HTML file
m.save("torino_carbon_storage_map.html")
