from pyproj import Transformer
import json

# Initialize the transformer: From EPSG:2000 to EPSG:4326
transformer = Transformer.from_crs("EPSG:2000", "EPSG:4326", always_xy=True)

# Load the GeoJSON file
input_file = "karnataka_data.json"
output_file = "karnataka_data_epsg4326.json"

with open(input_file, 'r') as f:
    geojson_data = json.load(f)

# Transform coordinates in GeoJSON
def transform_coordinates(geometry):
    if geometry["type"] == "Point":
        # Transform a single point
        return list(transformer.transform(*geometry["coordinates"]))
    elif geometry["type"] in ["LineString", "MultiPoint"]:
        # Transform a list of points
        return [list(transformer.transform(*coords)) for coords in geometry["coordinates"]]
    elif geometry["type"] in ["Polygon", "MultiLineString"]:
        # Transform a list of rings or lines
        return [[list(transformer.transform(*coords)) for coords in ring] for ring in geometry["coordinates"]]
    elif geometry["type"] == "MultiPolygon":
        # Transform a list of polygons
        return [[[list(transformer.transform(*coords)) for coords in ring] for ring in polygon] for polygon in geometry["coordinates"]]
    else:
        raise ValueError(f"Geometry type {geometry['type']} is not supported")

# Update the GeoJSON features
for feature in geojson_data["features"]:
    feature["geometry"]["coordinates"] = transform_coordinates(feature["geometry"])

# Save the transformed GeoJSON
with open(output_file, 'w') as f:
    json.dump(geojson_data, f, indent=4)

print(f"Converted GeoJSON saved to {output_file}")
