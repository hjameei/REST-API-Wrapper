import os
from typing import List, Dict, Union
from .exceptions import TheCatAPIException

class Result:
    def __init__(self, status_code: int, message: str = '', data: List[Dict] = None):
        """
        Result returned from low-level RestAdapter
        :param status_code: Standard HTTP Status code
        :param message: Human readable result
        :param data: Python List of Dictionaries (or maybe just a single Dictionary on error)
        """
        self.status_code = status_code
        self.message = message
        self.data = data if data is not None else []

    def __str__(self):
        return f"Result(status_code={self.status_code}, message='{self.message}', data={self.data})"

class Facts:
    def __init__(self, id: str, fact: str, breed_id: str, title: str):
        self.id = id
        self.fact = fact
        self.breed_id = breed_id
        self.title = title

    def __str__(self):
        return f"Facts(id='{self.id}', fact='{self.fact}', breed_id='{self.breed_id}', title='{self.title}')"

class Weight:
    def __init__(self, imperial: str, metric: str):
        self.imperial = imperial
        self.metric = metric
    
    def __str__(self):
        return f"Weight(imperial='{self.imperial}', metric='{self.metric}')"

class Category:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

class Image:
    def __init__(self, id: str, width: int, height: int, url: str) -> None:
        self.id = id
        self.width = width
        self.height = height
        self.url = url
    
    def __str__(self):
        return f"Image(id='{self.id}', width={self.width}, height={self.height}, url='{self.url}')"

class Breed:
    def __init__(self, weight: Union[Weight, dict], id: str, name: str, country_codes: str, country_code: str,
                 description: str, temperament: str = '', origin: str = '', life_span: str = '', alt_names: str = '',
                 wikipedia_url: str = '', image: Union[Image, dict] = None, **kwargs) -> None:
        self.weight = Weight(**weight) if isinstance(weight, dict) else weight
        self.id = id
        self.name = name
        self.origin = origin
        self.country_codes = country_codes
        self.country_code = country_code
        self.description = description
        self.temperament = temperament
        self.life_span = life_span
        self.alt_names = alt_names
        self.wikipedia_url = wikipedia_url
        self.image = Image(**image) if isinstance(image, dict) else image
        self.__dict__.update(kwargs)

class ImageShort:
    def __init__(self, id: int, url: str, categories: List[Category] = None, breeds: List[Breed] = None, data: bytes = bytes(), **kwargs):
        self.id = id
        self.url = url
        self.categories = [Category(**c) for c in categories] if categories else []
        self.breeds = [Breed(**b) for b in breeds] if breeds else []
        self.data = data
        self.__dict__.update(kwargs)
    
    def __str__(self):
        return f"ImageShort(id={self.id}, url='{self.url}', categories={self.categories}, breeds={self.breeds})"
    
    def save_to(self, path: str = './', file_name: str = ''):
        if not self.data:
            raise TheCatAPIException("No data to save")
        try:
            save_file_name = file_name if file_name else self.url.split('/')[-1]
            save_path = os.path.join(path, save_file_name)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, "wb") as f:
                f.write(self.data)
        except Exception as e:
            raise TheCatAPIException(str(e)) from e

class ImageFull(ImageShort):
    def __init__(self, id: int, url: str, sub_id: int = 0, created_at: str = '', original_filename: str = '',
                 categories: List[Category] = None, breeds: List[Breed] = None, **kwargs):
        super().__init__(id, url, categories, breeds)
        self.sub_id = sub_id
        self.created_at = created_at
        self.original_filename = original_filename
        self.__dict__.update(kwargs)

    def __str__(self):
        return f"ImageFull(id={self.id}, url='{self.url}', sub_id={self.sub_id}, created_at='{self.created_at}', original_filename='{self.original_filename}', categories={self.categories}, breeds={self.breeds})"