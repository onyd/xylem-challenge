import requests
import json

def get_waterways(bbox):
    """ Returns the list of waterways in the bbox.
    The bbox must be in format "west_long,south_lat,east_long,north_lat".
    """

    # Set up the URL for the Overpass API endpoint
    overpass_url = "http://overpass-api.de/api/interpreter"

    # Define the query to retrieve waterways within the bounding box
    overpass_query = f"""
        [out:json];
        way["waterway"]({bbox});
        (._;>;);
        out;
    """

    # Send the query to the Overpass API
    response = requests.get(overpass_url, params={'data': overpass_query})

    # Parse the response JSON and extract the waterway features
    waterways = []
    for element in response.json()['elements']:
        if element['type'] == 'way' and 'waterway' in element['tags']:
            way_nodes = []
            for node_id in element['nodes']:
                node = next((x for x in response.json()['elements'] if x['id'] == node_id), None)
                if node:
                    way_nodes.append((node['lat'], node['lon']))
            if way_nodes:
                name = element['tags'].get('name', 'Unnamed')
                waterway = {'name': name, 'points': way_nodes}
                waterways.append(waterway)

    # Print the waterway features as a list of dictionaries with name and points keys
    return json.dumps(waterways)

if __name__ == "__main__":
    print(get_waterways("70,18,74,22"))
