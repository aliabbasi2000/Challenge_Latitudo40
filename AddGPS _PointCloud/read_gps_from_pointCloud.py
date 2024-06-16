import laspy
import struct

# Read the updated LAS file
input_file = "Sample_1_with_gps.las"
las = laspy.read(input_file)

# Print out the VLRs
for vlr in las.vlrs:
    if vlr.user_id == "GPS_METADATA":
        gps_data = vlr.record_data
        lat, lon = struct.unpack('dd', gps_data)
        print(f"GPS Metadata - Latitude: {lat}, Longitude: {lon}")
