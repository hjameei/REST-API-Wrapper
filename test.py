from thecatapi.rest_adapter import RestAdapter
my_params = {'limit': 5}
catapi = RestAdapter(hostname="api.thecatapi.com", api_key=env("API_KEY"))
try:
    cat_list = catapi.get(endpoint="images/search/", params=my_params)
except Exception as e:
    print(str(e))