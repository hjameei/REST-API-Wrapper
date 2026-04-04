import logging
from thecatapi.rest_adapter import RestAdapter
from thecatapi.exceptions import TheCatAPIException
from thecatapi.models import *


class TheCatApi:
    def __init__(self, hostname: str = 'api.thecatapi.com', api_key: str = '', ver: str = 'v1', ssl_verify: bool = True, logger: logging.Logger = None):
        self._rest_adapter = RestAdapter(hostname, api_key, ver, ssl_verify, logger)

    def get_kitty(self) -> ImageShort:
        result = self._rest_adapter.get(endpoint='/images/search')
        kitty_img = ImageShort(**result.data[0])
        return kitty_img