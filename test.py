import gpw_queries

country = 'egypt'
site_id = '8f3e60030853b4b'

data = gpw_queries.get_stats()
print(data)

data = gpw_queries.get_countries()
print(data)

data = gpw_queries.get_site_by_id(site_id)
print(data)

data = gpw_queries.get_sites_by_country(country)
print(data.head())

data = gpw_queries.get_sites_contour(site_id)
print(data.head())

