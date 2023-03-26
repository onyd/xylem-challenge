import gpw_queries

country = 'egypt'

data = gpw_queries.get_sites_by_country(country)
print(data.keys())
print(data.info(['verbose']))
print(data.head())