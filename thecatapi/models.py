from typing import List, Dict, Union

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
from typing import Optional


class Image:
    def __init__(self, id: str, width: int, height: int, url: str) -> None:
        self.id = id
        self.width = width
        self.height = height
        self.url = url



class Weight:
    def __init__(self, imperial: str, metric: str):
        self.imperial = imperial
        self.metric = metric


class Category:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


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
        