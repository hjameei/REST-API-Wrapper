import requests
import requests.packages
from json import JSONDecodeError
from typing import List, Dict
import logging
from .exceptions import TheCatAPIException
from .models import Result


class RestAdapter:
    def __init__(self, hostname: str, api_key: str = '', ver: str = 'v1', ssl_verify: bool = True, logger: logging.Logger = None):
        self.url = "https://{}/{}/".format(hostname, ver)
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
        try:
            self._logger.debug(msg=log_line_pre)
            response = requests.request(method=http_method, url=full_url, headers=headers, params=params, json=data, verify=self._ssl_verify)
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=str(e))
            raise TheCatAPIException("Request failed") from e
        try:
            data_out = response.json()
        except (ValueError, JSONDecodeError) as e:
            self._logger.error(msg=log_line_post.format(False, None, e))
            raise TheCatAPIException("Bad JSON in response") from e
        is_success = 299 >= response.status_code >= 200
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
    
    def delete(self, endpoint: str, ep_params: Dict = None, data: Dict = None) -> Result:
        return self._do(http_method='DELETE', endpoint=endpoint, ep_params=ep_params, data=data)
