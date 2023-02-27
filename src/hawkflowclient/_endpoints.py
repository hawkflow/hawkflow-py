import os
import json

from ._validation import _validate_timed_data
from ._validation import _validate_metric_data
from ._validation import _validate_exception_data


def _timed_data(process: str, meta: str, uid: str) -> str:
    _validate_timed_data(process, meta, uid)

    x = json.dumps({
        "process": process,
        "meta": meta,
        "uid": uid
    })

    return x


def _metric_data(process: str, meta: str, items: dict) -> str:
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

