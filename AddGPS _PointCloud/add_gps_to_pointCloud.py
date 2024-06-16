import laspy
import struct

def parse_gps(latitude, lat_direction, longitude, lon_direction):
    lat_deg = int(float(latitude) / 100)
    lat_min = float(latitude) - lat_deg * 100
    lon_deg = int(float(longitude) / 100)
    lon_min = float(longitude) - lon_deg * 100
    
    lat = lat_deg + lat_min / 60.0
    lon = lon_deg + lon_min / 60.0
    
    if lat_direction == 'S':
        lat = -lat
    if lon_direction == 'W':
        lon = -lon
    
    return lat, lon

latitude = "4503.72099"
lat_direction = "N"
longitude = "00739.31393"
lon_direction = "E"

lat, lon = parse_gps(latitude, lat_direction, longitude, lon_direction)

# Read the LAS file
input_file = "Sample_1.las"
las = laspy.read(input_file)
gps_data = struct.pack('dd', lat, lon)

# Create a custom VLR for storing the GPS metadata
class CustomVLR(laspy.vlrs.VLR):
    def __init__(self, user_id, record_id, description, data):
        super().__init__(user_id, record_id, description)
        self.record_data = data

# Instantiate the custom VLR
custom_vlr = CustomVLR(user_id="GPS_METADATA", record_id=1, description="GPS coordinates", data=gps_data)

# Append the VLR to the LAS file
las.vlrs.append(custom_vlr)

# Save the LAS file with updated metadata
output_file = "Sample_1_with_gps.las"
las.write(output_file)

print(f"Point cloud saved with GPS metadata: {output_file}")
