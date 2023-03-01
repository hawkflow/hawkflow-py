import logging
import traceback

from ._endpoints import _timed_data, _metric_data, _exception_data
from ._hawkflow_exceptions import HawkFlowException
from ._validation import _validate_api_key

import requests

_hawkflow_api_url = 'https://api.hawkflow.ai/v1'


class HawkflowAPI:
    def __init__(self, api_key="", max_retries=3, wait_time=1):
        self.api_key = api_key
        self.max_retries = max_retries
        self.wait_time = wait_time

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
        url = f"{_hawkflow_api_url}/start"
        data = _timed_data(process, meta, uid)
        self._hawkflow_post(url, data)

    def end(self, process: str, meta: str = "", uid: str = ""):
        url = f"{_hawkflow_api_url}/end"
        data = _timed_data(process, meta, uid)
        self._hawkflow_post(url, data)

    def _hawkflow_post(self, url, data):
        try:
            retries = 0
            success = False

            self.api_key = _validate_api_key(self.api_key)

            api_headers = {
                "content-type": "application/json",
                "x-hawkflow-api-key": f"{self.api_key}"
            }

            while not success and retries < self.max_retries:
                try:
                    requests.post(url, data=data, headers=api_headers, timeout=self.wait_time)
                    success = True
                except Exception as err:
                    retries = retries + 1
                    logging.error(f"HawkFlow post_metrics failed on attempt {retries} - {traceback.format_exc()}")
        except HawkFlowException as he:
            logging.error(he.message)

