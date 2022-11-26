import unittest
from contextlib import contextmanager
import json
import datetime

from dateutil.parser import *

from src.hawkflowclient._validation import _validate_process, _validate_meta, _validate_exception_text
from src.hawkflowclient._validation import _validate_uid, _validate_metric_items
from src.hawkflowclient._endpoints import _exception_data, _metric_data, _timed_data
from src.hawkflowclient._hawkflow_exceptions import *


class TestHawkFlowApi(unittest.TestCase):
    @contextmanager
    def assertNotRaises(self, exc_type):
        try:
            yield None
        except exc_type:
            raise self.failureException('{} raised'.format(exc_type.__name__))

    def test_process_illegal_chars(self):
        with self.assertRaises(HawkFlowDataTypesException):
            process = "dfjow @e54j25 5"
            _validate_process(process)

        with self.assertRaises(HawkFlowDataTypesException):
            process = "dfjow 'e54j25 5"
            _validate_process(process)

        with self.assertNotRaises(HawkFlowDataTypesException):
            process = "dfjow_-e54j255"
            _validate_process(process)

    def test_validate_meta(self):
        with self.assertRaises(HawkFlowException):
            _validate_meta('^%£$')

    def test_validate_exception_text(self):
        with self.assertNotRaises(HawkFlowException):
            _validate_exception_text('^%£$')

        with self.assertRaises(HawkFlowException):
            _validate_exception_text(1)

    def test_validate_time_empty_string(self):
        with self.assertNotRaises(Exception):
            x = _exception_data("", "", "")
            y = json.loads(x)

    def test_validate_uid(self):
        with self.assertRaises(HawkFlowException):
            _validate_uid(1)

    def test_metric_items_correct_type(self):
        with self.assertNotRaises(HawkFlowDataTypesException):
            items = [{"name": "this is a name", "value": 2}, {"name": "this is a name", "value": 2}]
            _validate_metric_items(items)

    def test_metric_items_is_list(self):
        with self.assertRaises(HawkFlowDataTypesException):
            items = {"name": "this is a name", "value": 2}
            _validate_metric_items(items)

    def test_metric_items_is_list_dict(self):
        with self.assertRaises(HawkFlowDataTypesException):
            items = [44]
            _validate_metric_items(items)

    def test_metric_items_correct_dict_key_names(self):
        with self.assertRaises(HawkFlowDataTypesException):
            items = [{"name": "this is a name", "vaklue": 0.55}]
            _validate_metric_items(items)

        with self.assertRaises(HawkFlowDataTypesException):
            items = [{"najme": "this is a name", "value": 0.55}]
            _validate_metric_items(items)

    def test_metric_items_correct_dict_number_of_keys(self):
        with self.assertRaises(HawkFlowDataTypesException):
            items = [{"name": "this is a name", "value": 0.55, "other": "woops"}]
            _validate_metric_items(items)

    def test_metric_items_correct_types_in_dict(self):
        with self.assertRaises(HawkFlowDataTypesException):
            items = [{"name": "this is a name", "value": 2}, {"name": "this is a name", "value": "string"}]
            _validate_metric_items(items)


