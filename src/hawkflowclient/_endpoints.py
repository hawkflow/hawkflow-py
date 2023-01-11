import os
import json

from ._validation import _validate_timed_data
from ._validation import _validate_metric_data
from ._validation import _validate_exception_data
from ._validation import _validate_api_key


def _headers(api_key):
    if api_key == "":
        api_key = os.environ.get("HAWKFLOW_API_KEY")

    _validate_api_key(api_key)

    return {
        "Content-type": "application/json",
        "hawkflow-api-key": f"{api_key}"
    }


def _timed_data(process: str, meta: str, uid: str) -> str:
    _validate_timed_data(process, meta, uid)

    x = json.dumps({
        "process": process,
        "meta": meta,
        "uid": uid
    })

    return x


def _metric_data(process: str, meta: str, items: list) -> str:
    _validate_metric_data(process, meta, items)

    x = json.dumps({
        "process": process,
        "meta": meta,
        "items": items
    })

    return x


def _exception_data(process: str, meta: str, exception_text: str) -> str:
    _validate_exception_data(process, meta, exception_text)

    x = json.dumps({
        "process": process,
        "meta": meta,
        "exception": exception_text
    })

    return x

