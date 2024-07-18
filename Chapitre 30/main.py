import exifread
import webbrowser

def get_decimal_from_dms(dms, ref):
    degrees = dms[0].num / dms[0].den
    minutes = dms[1].num / dms[1].den
    seconds = dms[2].num / dms[2].den
    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if ref in ['S', 'W']:
        decimal = -decimal
    return decimal

def get_exif_data(image_path):
    with open(image_path, 'rb') as image_file:
        tags = exifread.process_file(image_file)
        return tags

def get_gps_data(tags):
    gps_latitude = tags.get('GPS GPSLatitude')
    gps_latitude_ref = tags.get('GPS GPSLatitudeRef')
    gps_longitude = tags.get('GPS GPSLongitude')
    gps_longitude_ref = tags.get('GPS GPSLongitudeRef')

    if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
        lat = get_decimal_from_dms(gps_latitude.values, gps_latitude_ref.values)
        lon = get_decimal_from_dms(gps_longitude.values, gps_longitude_ref.values)
        return lat, lon
    else:
        return None, None

def generate_google_maps_url(lat, lon):
    return f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"

if __name__ == "__main__":
    image_path = 'mcafee.jpg'  # Remplacer par le chemin de votre image
    tags = get_exif_data(image_path)
    
    print("Métadonnées de l'image :")
    for tag in tags.keys():
        if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
            print(f"{tag}: {tags[tag]}")

    lat, lon = get_gps_data(tags)
    if lat is not None and lon is not None:
        print(f"\nCoordonnées GPS : Latitude = {lat}, Longitude = {lon}")
        maps_url = generate_google_maps_url(lat, lon)
        print(f"URL Google Maps : {maps_url}")
        
        # Ouvrir l'URL dans le navigateur par défaut
        webbrowser.open(maps_url)
    else:
        print("\nPas de données GPS trouvées.")
