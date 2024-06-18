import os
import json

from ._validation import _validate_timed_data
from ._validation import _validate_metric_data
from ._validation import _validate_exception_data
from ._validation import _clean_process, _clean_meta, _clean_metric_key


def _timed_data_start(process: str, meta: str, uid: str) -> str:
    process = _clean_process(process)
    meta = _clean_meta(meta)

    _validate_timed_data(process, meta, uid, "")

    x = json.dumps({
        "process": process,
        "meta": meta,
        "uid": uid,
    })

    return x


def _timed_data_end(process: str, meta: str, uid: str, info: str) -> str:
    process = _clean_process(process)
    meta = _clean_meta(meta)

    _validate_timed_data(process, meta, uid, info)

    x = json.dumps({
        "process": process,
        "meta": meta,
        "uid": uid,
        "info": info
    })

    return x


def _metric_data(process: str, meta: str, items: dict, df: int) -> str:
    process = _clean_process(process)
    meta = _clean_meta(meta)
    items = _clean_metric_key(items)

    _validate_metric_data(process, meta, items, df)

    x = json.dumps({
        "process": process,
        "meta": meta,
        "items": items,
        "df": df
    })

    return x


def _exception_data(process: str, meta: str, exception_text: str) -> str:
    process = _clean_process(process)
    meta = _clean_meta(meta)

    _validate_exception_data(process, meta, exception_text)

    x = json.dumps({
        "process": process,
        "meta": meta,
        "exception": exception_text
    })

    return x

