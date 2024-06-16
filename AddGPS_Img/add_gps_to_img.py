from PIL import Image
import piexif

def set_gps_location(file_path, latitude, longitude):
    # Convert degrees to EXIF format
    def to_deg(value, loc):
        if value < 0:
            loc_value = loc[0]
            value = -value
        else:
            loc_value = loc[1]

        deg = int(value)
        min = int((value - deg) * 60)
        sec = round((value - deg - min / 60) * 3600, 5)

        return (deg, min, sec, loc_value)

    lat_deg = to_deg(latitude, ["S", "N"])
    lng_deg = to_deg(longitude, ["W", "E"])

    gps_ifd = {
        piexif.GPSIFD.GPSLatitudeRef: lat_deg[3],
        piexif.GPSIFD.GPSLatitude: [(lat_deg[0], 1), (lat_deg[1], 1), (int(lat_deg[2] * 100), 100)],
        piexif.GPSIFD.GPSLongitudeRef: lng_deg[3],
        piexif.GPSIFD.GPSLongitude: [(lng_deg[0], 1), (lng_deg[1], 1), (int(lng_deg[2] * 100), 100)]
    }

    exif_dict = {"GPS": gps_ifd}
    exif_bytes = piexif.dump(exif_dict)

    image = Image.open(file_path)
    image.save(file_path, "jpeg", exif=exif_bytes)

# Example usage
jpeg_file = "image.jpeg"
latitude = 45.0729  # Example latitude
longitude = 7.6868  # Example longitude
set_gps_location(jpeg_file, latitude, longitude)