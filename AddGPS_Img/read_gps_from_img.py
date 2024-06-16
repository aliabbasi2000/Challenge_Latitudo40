from PIL import Image
import piexif

def get_gps_location(file_path):
    def convert_to_degrees(value):
        d = value[0][0] / value[0][1]
        m = value[1][0] / value[1][1]
        s = value[2][0] / value[2][1]
        return d + (m / 60.0) + (s / 3600.0)

    image = Image.open(file_path)
    exif_data = piexif.load(image.info['exif'])

    gps_info = exif_data.get("GPS")
    if gps_info:
        lat_data = gps_info[piexif.GPSIFD.GPSLatitude]
        lat_ref = gps_info[piexif.GPSIFD.GPSLatitudeRef].decode()
        lon_data = gps_info[piexif.GPSIFD.GPSLongitude]
        lon_ref = gps_info[piexif.GPSIFD.GPSLongitudeRef].decode()

        lat = convert_to_degrees(lat_data)
        if lat_ref != "N":
            lat = -lat

        lon = convert_to_degrees(lon_data)
        if lon_ref != "E":
            lon = -lon

        return lat, lon
    else:
        return None

# Example usage
jpeg_file = "european_nettle_tree.jpeg"
gps_location = get_gps_location(jpeg_file)
if gps_location:
    print(f"Latitude: {gps_location[0]}, Longitude: {gps_location[1]}")
else:
    print("No GPS data")