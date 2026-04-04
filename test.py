from thecatapi.cat_api import TheCatApi
from thecatapi.models import *
catapi = TheCatApi()
kitty = catapi.get_kitty()
catapi.fetch_image_data(kitty)
kitty.save_to()