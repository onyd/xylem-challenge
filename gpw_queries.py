import requests
import geopandas as gpd

URL = "http://api.globalplasticwatch.org/"

SITES = "sites"
SITES_STATS = "sites/stats"
COUNTRIES = "countries"
CONTOURS = "contours"

def _query(path, params):
    try:
        response = requests.get(path, params=params)
        data = response.json()
        return data
    except:
        print(f"Warning: query to {path} with params {params} couldn't return a valid json result.")
        return None

def _query_geodataframe(path, params):
    try:
        response = requests.get(path, params=params)
        data = response.json()
        return gpd.GeoDataFrame.from_features(data['features'])
    except:
        print(f"Warning: query to {path} with params {params} couldn't return a valid GeoDataFrame result.")
        return None
    
def get_stats():
    """
    Provides summary statistics for all sites broken out by country.
    Args:
    Returns:
        Associated json-formatted site statistics.
    """
    endpoint = URL + SITES_STATS
    params = {'apikey':'xylem',
              'limit':'10000'}
    return _query(endpoint, params)

def get_countries():
    """
    Gather all available countires.
    Args:
    Returns:
        list of available countries with names, codes and bounding boxes
    """
    endpoint = URL + COUNTRIES
    params = {'apikey':'xylem',
              'limit':'10000'}
    return _query(endpoint, params)

def get_sites_by_bounding_box(bbox):
    """
    Get all sites within the bounding box bbox. (bbox useless for now as it dosen't work)
    Args:
        bbox: array-like (lon1, lon2, lat1, lat2)
    Returns:
        Associated GeoDataFrame of the sites.
    """
    endpoint = URL + SITES
    params = {'apikey':'xylem',
              'limit':'10000'}
    return _query_geodataframe(endpoint, params)

def get_site_by_id(site_id):
    """
    Get the site info from its id.
    Args:
        site_id: site string id
    Returns:
        Associated json details of the site.
    """
    endpoint = URL + SITES + f"/{site_id}"
    params = {'apikey':'xylem',
              'limit':'10000'}
    return _query(endpoint, params)

def get_sites_by_country(country):
    """
    Get the sites info within the specified country.
    Args:
        country: country name
    Returns:
        Associated GeoDataFrame of the sites.
    """
    endpoint = URL + COUNTRIES + f"/{country}/" + SITES
    params = {'apikey':'xylem',
              'limit':'10000'}
    return _query_geodataframe(endpoint, params)

def get_sites_contour(site_id):
    """
    Provides summary statistics for all sites broken out by country.
    Args:
        site_id: site string id
    Returns:
        Associated GeoDataFrame of the site contour.
    """
    endpoint = URL + SITES + f"/{site_id}/" + CONTOURS
    params = {'apikey':'xylem',
              'limit':'10000'}
    return _query_geodataframe(endpoint, params)

