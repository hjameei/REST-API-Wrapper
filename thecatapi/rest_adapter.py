import requests
import requests.packages
from json import JSONDecodeError
from typing import List, Dict
import logging
from .models import Result
from .exceptions import TheCatAPIException



class RestAdapter:
    def __init__(self, hostname: str='api.thecatapi.com', api_key: str = '', ver: str = 'v1', ssl_verify: bool = True, logger: logging.Logger = None):
        """""
        Constructor for RestAdapter
        :param hostname: Normally, api.thecatapi.com
        :param api_key: (optional) string used for authentication when POSTing or DELETEing
        :param ver: always v1
        :param ssl_verify: Normally set to True, but if having SSL/TLS cert validation issues, can turn off with False
        :param logger: (optional) If your app has a logger, pass it in here.
        """
        self.url = "https://{}/{}".format(hostname, ver)
        self._api_key = api_key
        self._ssl_verify = ssl_verify
        self._logger = logger or logging.getLogger(__name__)
        if not ssl_verify:
            # noinspection PyUnresolvedReferences
            requests.packages.urllib3.disable_warnings()

    def _do(self, http_method: callable, endpoint: str, params: Dict = None, data: Dict = None) -> Result:
        full_url = self.url + endpoint
        headers = {'x-api-key': self._api_key}
        log_line_pre = f"method={http_method}, url={full_url}, params={params}, data={data}"
        log_line_post = ', '.join((log_line_pre, "success={}, status_code={}, message={}"))
        # Log HTTP params and perform an HTTP request, catching and re-raising any exceptions
        try:
            self._logger.debug(msg=log_line_pre)
            response = requests.request(method=http_method, url=full_url, headers=headers, params=params, json=data, verify=self._ssl_verify)
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=str(e))
            raise TheCatAPIException("Request failed") from e
        # Deserialize JSON output to Python object, or return failed Result on exception
        try:
            data_out = response.json()
        except (ValueError, JSONDecodeError) as e:
            self._logger.error(msg=log_line_post.format(False, None, e))
            raise TheCatAPIException("Bad JSON in response") from e
        # If status_code in 200-299 range, return success Result with data, otherwise raise exception
        is_success = 299 >= response.status_code >= 200 # 200 to 299 is OK
        log_line = log_line_post.format(is_success, response.status_code, response.reason)
        if is_success:
            self._logger.debug(msg=log_line)
            return Result(status_code=response.status_code, message=response.json, data=data_out)
        self._logger.error(msg=log_line)
        raise TheCatAPIException(f"{response.status_code}: {response.reason}")

    def get(self, endpoint: str, params: Dict = None) -> Result:
        return self._do(http_method="GET", endpoint=endpoint, params=params)
    
    def post(self, endpoint: str, params: Dict = None, data: Dict = None) -> Result:
        return self._do(http_method="POST", endpoint=endpoint, params=params, data=data)
    
    def delete(self, endpoint: str, params: Dict = None, data: Dict = None) -> Result:
        return self._do(http_method='DELETE', endpoint=endpoint, params=params, data=data)
