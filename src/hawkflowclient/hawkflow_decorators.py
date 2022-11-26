from functools import wraps

from .hawkflow import *


class HawkflowTimed:
    def __init__(self, api_key=""):
        self.api_key = api_key

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            meta = ""
            for k in kwargs.keys():
                if k == "hawkflow_meta":
                    meta = kwargs['hawkflow_meta']

            hawkflow_start(process=func.__name__, meta=meta, api_key=self.api_key)
            result = func(*args, **kwargs)
            hawkflow_end(process=func.__name__, meta=meta, api_key=self.api_key)
            return result
        return wrapper


class HawkflowMetrics:
    def __init__(self, api_key=""):
        self.api_key = api_key

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "items" not in kwargs.keys():
                kwargs['items'] = []

            meta = ""
            for k in kwargs.keys():
                if k == "hawkflow_meta":
                    meta = kwargs['hawkflow_meta']

            hawkflow_metrics(process=func.__name__, meta=meta, items=kwargs['items'], api_key=self.api_key)
            result = func(*args, **kwargs)
            return result
        return wrapper


class HawkflowException:
    def __init__(self, api_key=""):
        self.api_key = api_key

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            meta = ""
            for k in kwargs.keys():
                if k == "hawkflow_meta":
                    meta = kwargs['hawkflow_meta']

            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                hawkflow_exception(process=func.__name__, meta=meta, exception_text=traceback.format_exc(), api_key=self.api_key)
        return wrapper
