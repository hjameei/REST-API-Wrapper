from thecatapi.cat_api import TheCatApi
cat_api = TheCatApi()
kitty = cat_api.get_kitty()
cat_api.fetch_image_data(kitty)
kitty.save_to()