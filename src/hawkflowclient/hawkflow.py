import logging
import traceback

from ._endpoints import _headers, _timed_data, _metric_data, _exception_data
from ._hawkflow_exceptions import HawkFlowException

import requests
from requests.adapters import HTTPAdapter, Retry


_hawkflow_api_url = 'https://api.hawkflow.ai/v1'

_retry_strategy = Retry(
    total=3,
    backoff_factor=2,
    status_forcelist=[500, 502, 503, 504],
    method_whitelist=["POST"]
)

_adapter = HTTPAdapter(max_retries=_retry_strategy)

_http = requests.Session()
_http.mount("https://", _adapter)


def hawkflow_metrics(process: str, meta: str = "", items=None, api_key: str = ""):
    if items is None:
        items = []

    url = f"{_hawkflow_api_url}/metrics"
    data = _metric_data(process, meta, items)
    _hawkflow_post(url, data, _headers(api_key))


def hawkflow_exception(process: str, meta: str = "", exception_text: str = "", api_key: str = ""):
    url = f"{_hawkflow_api_url}/exception"
    data = _exception_data(process, meta, exception_text)
    _hawkflow_post(url, data, _headers(api_key))


def hawkflow_start(process: str, meta: str = "", uid: str = "", api_key: str = ""):
    url = f"{_hawkflow_api_url}/timed/start"
    data = _timed_data(process, meta, uid)
    _hawkflow_post(url, data, _headers(api_key))


def hawkflow_end(process: str, meta: str = "", uid: str = "",  api_key: str = ""):
    url = f"{_hawkflow_api_url}/timed/end"
    data = _timed_data(process, meta, uid)
    _hawkflow_post(url, data, _headers(api_key))


def _hawkflow_post(url, data, api_headers):
    try:
        _http.post(url, data=data, headers=api_headers, timeout=1)
    except HawkFlowException as he:
        logging.error(he.message)
    except requests.exceptions.HTTPError as err:
        logging.error(f"HawkFlow post_metrics failed - {traceback.format_exc()}")

