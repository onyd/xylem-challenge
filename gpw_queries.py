import requests
import geopandas as gpd

URL = "http://api.globalplasticwatch.org/"

SITES = "sites"
SITES_STATS = "sites/stats"
COUNTRIES = "countries"
CONTOURS = "contours"

def _query(path, params):
    response = requests.get(path, params=params)
    data = response.json()
    return data

def _query_geodataframe(path, params):
    data = _query(path, params)
    return gpd.GeoDataFrame.from_features(data['features'])

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
    Get all sites within the bounding box bbox.
    Args:
        bbox: array-like (lon1, lat1, lon2, lat2)
    Returns:
        Associated GeoDataFrame of the sites.
    """
    endpoint = URL + SITES
    params = {'apikey':'xylem',
              'limit':'10000',
              'bbox': bbox}
    return _query_geodataframe(endpoint, params)

def get_sites_by_id(site_id):
    """
    Get the sites info from its id.
    Args:
        site_id: integer or string id
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
        site_id: integer or string id
    Returns:
        Associated GeoDataFrame of the site contour.
    """
    endpoint = URL + SITES + f"/{site_id}/" + CONTOURS
    params = {'apikey':'xylem',
              'limit':'10000'}
    return _query_geodataframe(endpoint, params)

