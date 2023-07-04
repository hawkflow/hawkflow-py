import re
import os

from ._hawkflow_exceptions import *


PROCESS_REGEX = r'^[a-zA-Z\d\s_-]*$'
META_REGEX = r'^[\w\s\\/\-\_\*\&\=\.\+\?\@\:]*$'
API_KEY_REGEX = r'^[a-zA-Z0-9_-]+$'
METRIC_KEY_REGEX = r'^[\w\s\\/\-\_\*\&\=\.\+\?\@\:]*$'
UID_REGEX = r'^[a-zA-Z0-9_-]*$'


def _validate_timed_data(process: str, meta: str, uid: str):
    _validate_core(process, meta)
    _validate_uid(uid)


def _validate_metric_data(process: str, meta: str, items: dict):
    _validate_core(process, meta)
    _validate_metric_items(items)


def _validate_exception_data(process: str, meta: str, exception_text: str):
    _validate_core(process, meta)
    _validate_exception_text(exception_text)


def _validate_api_key(api_key):
    if not api_key or api_key == "":
        api_key = os.environ.get("HAWKFLOW_API_KEY")

    if not api_key or api_key == "":
        raise HawkFlowNoApiKeyException()

    if len(api_key) > 50:
        raise HawkFlowApiKeyFormatException()

    if not re.match(API_KEY_REGEX, api_key):
        raise HawkFlowApiKeyFormatException()

    return api_key


def _validate_core(process, meta):
    _validate_process(process)
    _validate_meta(meta)


def _validate_uid(uid):
    if not isinstance(uid, str):
        raise HawkFlowDataTypesException("uid parameter must be type str.")

    if len(uid) > 50:
        raise HawkFlowDataTypesException("uid parameter exceeded max length of 50.")

    if not re.match(UID_REGEX, uid):
        raise HawkFlowDataTypesException("uid parameter incorrect format.")


def _validate_process(process):
    if not isinstance(process, str):
        raise HawkFlowDataTypesException("process parameter must be type str")

    if process == "":
        raise HawkFlowDataTypesException("process parameter cannot be empty")

    if len(process) > 249:
        raise HawkFlowDataTypesException("process parameter exceeded max length of 250")

    if not re.match(PROCESS_REGEX, process):
        raise HawkFlowDataTypesException("process parameter contains illegal characters")


def _validate_meta(meta):
    if not isinstance(meta, str):
        raise HawkFlowDataTypesException("meta parameter must be type str")

    if len(meta) > 499:
        raise HawkFlowDataTypesException("meta parameter exceeded max length of 500")

    if not re.match(META_REGEX, meta):
        raise HawkFlowDataTypesException("meta parameter contains illegal characters")


def _validate_exception_text(exception_text):
    if not isinstance(exception_text, str):
        raise HawkFlowDataTypesException("exception_text parameter must be type str")

    if len(exception_text) > 15000:
        raise HawkFlowDataTypesException("exception_text parameter exceeded max length of 15000")


def _validate_metric_items(items):
    _metric_text = "metric items parameter should be a dict {STR:FLOAT or INT}"

    if not isinstance(items, dict):
        raise HawkFlowDataTypesException("metric items parameter must be type dict {STR:FLOAT or INT}")

    for key in items.keys():
        if not isinstance(key, str) or (not isinstance(items[key], int) and not isinstance(items[key], float)):
            raise HawkFlowDataTypesException(_metric_text)

        if key == "":
            raise HawkFlowDataTypesException("metric items parameter dictionary key cannot be empty")

        if not re.match(METRIC_KEY_REGEX, key):
            raise HawkFlowDataTypesException("metric items parameter dictionary key contains illegal characters")
