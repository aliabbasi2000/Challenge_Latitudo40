import torch
import torchvision
import torchvision.transforms as transforms
import PIL.Image as Image
import piexif
import os
import sqlite3

classes = [
    'European Nettle Tree',
    'European Red Pine',
    'Horse Chestnut',
]

model = torch.load('best_model.pth')

mean = [0.4225, 0.5102, 0.2710]
std = [0.1951, 0.1951, 0.1858]

image_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(torch.Tensor(mean), torch.Tensor(std))
])

def classify(model, image_transforms, image_path, classes, id):
    model = model.eval()
    image = Image.open(image_path)
    image = image_transforms(image).float()
    image = image.unsqueeze(0)
    
    output = model(image)
    _, predicted = torch.max(output.data, 1)
    
    species = classes[predicted.item()]
    gps_location = get_gps_location(image_path)
    
    if gps_location:
        latitude, longitude = gps_location
    else:
        latitude, longitude = "No GPS data", "No GPS data"
    
    return id, species, latitude, longitude


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

# Database setup
conn = sqlite3.connect('tree_species.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tree_classification (
        id INTEGER PRIMARY KEY,
        species TEXT,
        latitude TEXT,
        longitude TEXT
    )
''')

# Output file setup
output_file = 'classification_results.txt'
with open(output_file, 'w') as f:
    f.write("Id, Species, Latitude, Longitude\n")

# Process images
image_extensions = ['.jpeg', '.jpg', '.png']
image_files = [f for f in os.listdir('.') if os.path.isfile(f) and os.path.splitext(f)[1].lower() in image_extensions]

for idx, image_file in enumerate(image_files, start=1):
    id, species, latitude, longitude = classify(model, image_transforms, image_file, classes, idx)
    
    # Write to text file
    with open(output_file, 'a') as f:
        f.write(f"{id}, {species}, {latitude}, {longitude}\n")
    
    # Insert into database
    cursor.execute('''
        INSERT INTO tree_classification (id, species, latitude, longitude)
        VALUES (?, ?, ?, ?)
    ''', (id, species, latitude, longitude))

# Commit and close the database connection
conn.commit()
conn.close()

print(f"Results have been written to {output_file} and inserted into the SQLite database.")
