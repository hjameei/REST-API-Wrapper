from thecatapi.rest_adapter import RestAdapter
from dotenv import load_dotenv
import os

# Loading the environment variables from the .env file
load_dotenv() 
api_key = os.getenv("API_KEY")

if not api_key:
    raise RuntimeError("API_KEY is not set")

catapi = RestAdapter(hostname="api.thecatapi.com", api_key=api_key)
# try:
#     cat_list = catapi.get(endpoint="images/search/")
#     print(cat_list)
# except Exception as e:
#     print("An error occurred while fetching cat images:")
#     print(str(e))

from thecatapi.rest_adapter import RestAdapter
from thecatapi.models import Weight, Breed
catapi = RestAdapter()
result = catapi.get("breeds")
breed_list = []
for d in result.data:
    breed_list.append(Breed(**d))

# try:
#     fact = catapi.get(endpoint="facts/")
#     print(fact)
# except Exception as e:
#     print("An error occurred while fetching cat facts:")
#     print(str(e))