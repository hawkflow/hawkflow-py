import re
import unittest

from src.hawkflowclient._validation import _validate_api_key, _validate_process, _validate_uid
from src.hawkflowclient._validation import _validate_meta, _validate_metric_items
from src.hawkflowclient._hawkflow_exceptions import *


class TestValidation(unittest.TestCase):
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

