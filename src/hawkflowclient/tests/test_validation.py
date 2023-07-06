import re
import unittest
from contextlib import contextmanager
import json

from src.hawkflowclient._validation import _validate_api_key
from src.hawkflowclient._validation import _validate_process, _validate_meta, _validate_exception_text
from src.hawkflowclient._validation import _validate_uid, _validate_metric_items, _validate_metric_items_df
from src.hawkflowclient._endpoints import _exception_data
from src.hawkflowclient._hawkflow_exceptions import *


class TestValidation(unittest.TestCase):
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
        with self.assertRaises(HawkFlowDataTypesException):
            x = _exception_data("", "", "")
            y = json.loads(x)

    def test_validate_uid(self):
        with self.assertRaises(HawkFlowException):
            _validate_uid(1)

    def test_metric_items_correct_type(self):
        with self.assertNotRaises(HawkFlowDataTypesException):
            items = {"value": 2}
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

    def test_metric_items_df_valid(self):
        dic = {'col1': {'metric1': 1, 'metric2': 2}, 'col2': {'metric1': 1, 'metric2': 2}}
        with self.assertNotRaises(Exception):
            _validate_metric_items_df(dic)

    def test_metric_items_df_valid_1(self):
        dic = {'co.,l1': {'metri.,c1': 1, 'metric2': 2}, 'col2': {'metric1': 1, 'metric2': 2}}
        with self.assertNotRaises(Exception):
            _validate_metric_items_df(dic)

    def test_metric_items_df_invalid_value(self):
        dic = {'col1': {'metric1': "df", 'metric2': 2}, 'col2': {'metric1': 1, 'metric2': 2}}
        with self.assertRaises(HawkFlowDataTypesException):
            _validate_metric_items_df(dic)

    def test_metric_items_df_invalid_key(self):
        dic = {'col1': {'metric1%': 2.9, 'metric2': 2}, 'col2': {'metric1': 1, 'metric2': 2}}
        with self.assertRaises(HawkFlowDataTypesException):
            _validate_metric_items_df(dic)

    def test_metric_items_df_invalid_key_1(self):
        dic = {'col1%': {'metric1': 2.9, 'metric2': 2}, 'col2': {'metric1': 1, 'metric2': 2}}
        with self.assertRaises(HawkFlowDataTypesException):
            _validate_metric_items_df(dic)

    def test_valid_api_key_regex(self):
        try:
            key = "azure345345s"
            _validate_api_key(key)
        except HawkFlowApiKeyFormatException:
            self.fail("test_valid_api_key_regex raised Exception")

    def test_invalid_api_key_regex(self):
        with self.assertRaises(HawkFlowApiKeyFormatException):
            key = "azure*?%£s"
            _validate_api_key(key)

    def test_invalid_empty_string_api_key_regex(self):
        with self.assertRaises(HawkFlowNoApiKeyException):
            key = ""
            _validate_api_key(key)

    def test_valid_meta_regex_1(self):
        try:
            key = r"a=zu+re\34/53*45&s"
            _validate_meta(key)
        except HawkFlowDataTypesException:
            self.fail("test_valid_api_meta_regex raised Exception")

    def test_valid_meta_regex_2(self):
        try:
            key = r'127.0.0.1 story /'
            _validate_meta(key)
        except HawkFlowDataTypesException:
            self.fail("test_valid_api_meta_regex raised Exception")

    def test_valid_meta_regex_4(self):
        try:
            key = r'127.0.0.1 story / ,'
            _validate_meta(key)
        except HawkFlowDataTypesException:
            self.fail("test_valid_api_meta_regex raised Exception")

    def test_valid_meta_regex_3(self):
        try:
            key = r'http://127.0.0.1:5001/v1/start'
            _validate_meta(key)
        except HawkFlowDataTypesException:
            self.fail("test_valid_api_meta_regex raised Exception")

    def test_invalid_meta_regex(self):
        with self.assertRaises(HawkFlowDataTypesException):
            key = r"azu%re\34/53*45s"
            _validate_meta(key)

    def test_valid_meta_empty_string_regex(self):
        try:
            key = r''
            _validate_meta(key)
        except HawkFlowDataTypesException:
            self.fail("test_valid_meta_empty_string_regex raised Exception")

    def test_valid_uid_regex(self):
        try:
            key = r'xfghgh456456-_ads_fd345345'
            _validate_uid(key)
        except HawkFlowDataTypesException:
            self.fail("test_valid_api_uid_regex raised Exception")

    def test_valid_uid_empty_string_regex(self):
        try:
            key = r''
            _validate_uid(key)
        except HawkFlowDataTypesException:
            self.fail("test_valid_api_uid_empty_string_regex raised Exception")

    def test_invalid_uid_regex(self):
        with self.assertRaises(HawkFlowDataTypesException):
            key = r"azu%re\34/53*45s"
            _validate_uid(key)

    def test_valid_process_regex(self):
        try:
            key = r'xfghgh456456-_ads_fd345345'
            _validate_process(key)
        except HawkFlowDataTypesException:
            self.fail("test_valid_api_process_regex raised Exception")

    def test_valid_process_empty_string_regex(self):
        with self.assertRaises(HawkFlowDataTypesException):
            key = r''
            _validate_process(key)

    def test_invalid_process_regex(self):
        with self.assertRaises(HawkFlowDataTypesException):
            key = r"azu%re\34/53*45s"
            _validate_process(key)

    def test_valid_metric_items_regex(self):
        try:
            key = r'xfghgh456456-_ads_fd345345'
            items = {key: 45}
            _validate_metric_items(items)
        except HawkFlowDataTypesException:
            self.fail("test_valid_api_metric_items_regex raised Exception")

    def test_valid_metric_items_regex_1(self):
        try:
            key = r'xfghgh456456-_ads_fd345345,'
            items = {key: 45}
            _validate_metric_items(items)
        except HawkFlowDataTypesException:
            self.fail("test_valid_api_metric_items_regex raised Exception")

    def test_valid_metric_items_empty_string_regex(self):
        with self.assertRaises(HawkFlowDataTypesException):
            key = r''
            items = {key: 45}
            _validate_metric_items(items)

    def test_invalid_metric_items_regex(self):
        with self.assertRaises(HawkFlowDataTypesException):
            key = r"azu%re\34/53*45s"
            items = {key: 45}
            _validate_metric_items(items)

