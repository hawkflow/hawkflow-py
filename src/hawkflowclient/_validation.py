import re

from ._hawkflow_exceptions import *


def _validate_timed_data(process: str, meta: str, uid: str):
    _validate_core(process, meta)
    _validate_uid(uid)


def _validate_metric_data(process: str, meta: str, items: list):
    _validate_core(process, meta)
    _validate_metric_items(items)


def _validate_exception_data(process: str, meta: str, exception_text: str):
    _validate_core(process, meta)
    _validate_exception_text(exception_text)


def _validate_api_key(api_key):
    if not api_key or api_key == "":
        raise HawkFlowNoApiKeyException()

    if not re.match('^[a-zA-Z\\d\\s_-]*$', api_key):
        raise HawkFlowApiKeyFormatException()

    if len(api_key) > 50:
        raise HawkFlowApiKeyFormatException()


def _validate_core(process, meta):
    _validate_process(process)
    _validate_meta(meta)


def _validate_uid(uid):
    if not isinstance(uid, str):
        raise HawkFlowDataTypesException("uid parameter incorrect format.")

    if len(uid) > 50:
        raise HawkFlowDataTypesException("uid parameter incorrect format.")

    if not re.match('^[a-zA-Z\\d\\s_-]*$', uid):
        raise HawkFlowDataTypesException("uid parameter incorrect format.")


def _validate_process(process):
    if not isinstance(process, str):
        raise HawkFlowDataTypesException("process parameter must be type str")

    if len(process) > 249:
        raise HawkFlowDataTypesException("process parameter exceeded max length of 300")

    if not re.match('^[a-zA-Z\\d\\s_-]*$', process):
        raise HawkFlowDataTypesException("process parameter contains illegal characters")


def _validate_meta(meta):
    if not isinstance(meta, str):
        raise HawkFlowDataTypesException("meta parameter must be type str")

    if len(meta) > 499:
        raise HawkFlowDataTypesException("meta parameter exceeded max length of 500")

    if not re.match('^[a-zA-Z\\d\\s_-]*$', meta):
        raise HawkFlowDataTypesException("meta parameter contains illegal characters")


def _validate_exception_text(exception_text):
    if not isinstance(exception_text, str):
        raise HawkFlowDataTypesException("exception_text parameter must be type str")

    if len(exception_text) > 15000:
        raise HawkFlowDataTypesException("exception_text parameter exceeded max length of 15000")


def _validate_metric_items(items):
    _metric_text = "metric items parameter should be a list of dict {name: STR, value: INT|FLOAT}"

    if not isinstance(items, list):
        raise HawkFlowDataTypesException("metric items parameter must be type list")

    for d in items:
        if not isinstance(d, dict):
            raise HawkFlowDataTypesException("metric items parameter must be type List[dict]")

        if len(d) != 2:
            raise HawkFlowDataTypesException(_metric_text)

        if "name" not in d or "value" not in d:
            raise HawkFlowDataTypesException(_metric_text)

        if not isinstance(d["name"], str) or (not isinstance(d["value"], int) and not isinstance(d["value"], float)):
            raise HawkFlowDataTypesException(_metric_text)

        if not re.match('^[a-zA-Z\\d\\s_-]*$', d["name"]):
            raise HawkFlowDataTypesException("metric name parameter contains illegal characters")
