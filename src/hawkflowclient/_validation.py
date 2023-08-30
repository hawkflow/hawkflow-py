import re
import os

from ._hawkflow_exceptions import *


# PROCESS_REGEX = r'^[a-zA-Z\d\s_-]*$'
# META_REGEX = r'^[\w\s\\/\-\_\*\&\=\.\,\+\?\@\:]*$'
# METRIC_KEY_REGEX = r'^[\w\s\\/\-\_\*\&\=\.\,\+\?\@\:]*$'

# PROCESS_REGEX_SUB = r'[^ a-zA-Z\d\s_-]'
# META_REGEX_SUB = r'[^ \w\s\\/\-\_\*\&\=\.\,\+\?\@\:]'
# METRIC_KEY_REGEX_SUB = r'[^ \w\s\\/\-\_\*\&\=\.\,\+\?\@\:]'

PROCESS_REGEX = r"['\"%]"
META_REGEX = r"['\"%]"
METRIC_KEY_REGEX = r"['\"%]"

PROCESS_REGEX_SUB = r"[\"'%]"
META_REGEX_SUB = r"[\"'%]"
METRIC_KEY_REGEX_SUB = r"[\"'%]"

API_KEY_REGEX = r'^[a-zA-Z0-9_-]+$'
UID_REGEX = r'^[a-zA-Z0-9_-]*$'


def _clean_process(input_str):
    return re.sub(PROCESS_REGEX_SUB, '', input_str)


def _clean_meta(input_str):
    return re.sub(META_REGEX_SUB, '', input_str)


def _clean_metric_key(items):
    cleaned_dict = {}
    for key, value in items.items():
        cleaned_key = re.sub(METRIC_KEY_REGEX_SUB, '', str(key))
        cleaned_dict[cleaned_key] = value
    return cleaned_dict


def _validate_timed_data(process: str, meta: str, uid: str):
    _validate_core(process, meta)
    _validate_uid(uid)


def _validate_metric_data(process: str, meta: str, items: dict, df: int):
    _validate_core(process, meta)

    if df == 1:
        _validate_metric_items_df(items)
    else:
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

    if re.search(PROCESS_REGEX, process):
        raise HawkFlowDataTypesException(f"process parameter: {process} contains illegal characters")


def _validate_meta(meta):
    if not isinstance(meta, str):
        raise HawkFlowDataTypesException("meta parameter must be type str")

    if len(meta) > 499:
        raise HawkFlowDataTypesException("meta parameter exceeded max length of 500")

    if re.search(META_REGEX, meta):
        raise HawkFlowDataTypesException(f"meta parameter: {meta} contains illegal characters")


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

        if re.search(METRIC_KEY_REGEX, key):
            raise HawkFlowDataTypesException(f"metric items parameter dictionary key: {key} contains illegal characters")


def _validate_metric_items_df(items):
    _metric_text = "metric items df parameter should be a dict {STR:{str:FLOAT or INT}, {str:FLOAT or INT}}"

    if not isinstance(items, dict):
        raise HawkFlowDataTypesException("metric items parameter must be type dict {STR:FLOAT or INT}")

    if not items:
        raise HawkFlowDataTypesException("metric items cannot be empty")

    for key, value in items.items():
        if re.search(METRIC_KEY_REGEX, key):
            raise HawkFlowDataTypesException("metric items parameter dictionary key contains illegal characters")
        if key == "":
            raise HawkFlowDataTypesException("metric items parameter dictionary key cannot be empty")
        # Check if each item in the dictionary is also a dictionary
        if not isinstance(value, dict):
            raise HawkFlowDataTypesException(_metric_text)

        for sub_key, sub_value in value.items():
            if re.search(METRIC_KEY_REGEX, sub_key):
                raise HawkFlowDataTypesException("metric items parameter dictionary key contains illegal characters")
            if sub_key == "":
                raise HawkFlowDataTypesException("metric items parameter dictionary key cannot be empty")
            # Check if each value in the sub-dictionaries is an integer (or a float)
            if not isinstance(sub_value, (int, float)):
                raise HawkFlowDataTypesException(_metric_text)