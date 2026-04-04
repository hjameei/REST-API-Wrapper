from thecatapi.cat_api import TheCatApi
from thecatapi.models import *
catapi = TheCatApi()
result = catapi.get_kitty()
print(result)