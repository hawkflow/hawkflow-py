import logging
import traceback

from ._endpoints import _timed_data, _metric_data, _exception_data
from ._hawkflow_exceptions import HawkFlowException
from ._validation import _validate_api_key

import requests
from requests.adapters import HTTPAdapter, Retry

_hawkflow_api_url = 'https://api.hawkflow.ai/v1'

_retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504],
    method_whitelist=["POST"]
)

_adapter = HTTPAdapter(max_retries=_retry_strategy)

_http = requests.Session()
_http.mount("https://", _adapter)

class HawkflowAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def metrics(self, process: str, meta: str = "", items=None):
        if items is None:
            items = []

        url = f"{_hawkflow_api_url}/metrics"
        data = _metric_data(process, meta, items)
        self._hawkflow_post(url, data)

    def exception(self, process: str, meta: str = "", exception_text: str = ""):
        url = f"{_hawkflow_api_url}/exception"
        data = _exception_data(process, meta, exception_text)
        self._hawkflow_post(url, data)


    def start(self, process: str, meta: str = "", uid: str = ""):
        url = f"{_hawkflow_api_url}/timed/start"
        data = _timed_data(process, meta, uid)
        self._hawkflow_post(url, data)


    def end(self, process: str, meta: str = "", uid: str = ""):
        url = f"{_hawkflow_api_url}/timed/end"
        data = _timed_data(process, meta, uid)
        self._hawkflow_post(url, data)

    def _hawkflow_post(self, url, data):
        try:
            _validate_api_key(self.api_key)
            
            api_headers = {
                "Content-type": "application/json",
                "hawkflow-api-key": f"{self.api_key}"
            }

            _http.post(url, data=data, headers=api_headers, timeout=1)
        except HawkFlowException as he:
            logging.error(he.message)
        except requests.exceptions.HTTPError as err:
            logging.error(f"HawkFlow post_metrics failed - {traceback.format_exc()}")

