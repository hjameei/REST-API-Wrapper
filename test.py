from thecatapi.rest_adapter import RestAdapter
import os

api_key = os.getenv("API_KEY")

if not api_key:
    raise RuntimeError("API_KEY is not set")

my_params = {'limit': 5}
catapi = RestAdapter(hostname="api.thecatapi.com", api_key=api_key)
try:
    cat_list = catapi.get(endpoint="images/search/", params=my_params)
except Exception as e:
    print(str(e))