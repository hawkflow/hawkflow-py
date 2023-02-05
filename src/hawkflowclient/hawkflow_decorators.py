from functools import wraps

from .hawkflow_api import *


class HawkflowTimed:
    def __init__(self, api_key=""):
        self.api = HawkflowAPI(api_key)

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            meta = ""
            for k in kwargs.keys():
                if k == "hawkflow_meta":
                    meta = kwargs['hawkflow_meta']

            self.api.start(process=func.__name__, meta=meta)
            result = func(*args, **kwargs)
            self.api.end(process=func.__name__, meta=meta)
            return result
        return wrapper


class HawkflowMetrics:
    def __init__(self, api_key=""):
        self.api = HawkflowAPI(api_key)

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "items" not in kwargs.keys():
                kwargs['items'] = []

            meta = ""
            for k in kwargs.keys():
                if k == "hawkflow_meta":
                    meta = kwargs['hawkflow_meta']

            self.api.metrics(process=func.__name__, meta=meta, items=kwargs['items'])
            result = func(*args, **kwargs)
            return result
        return wrapper


class HawkflowException:
    def __init__(self, api_key=""):
        self.api = HawkflowAPI(api_key)

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
                self.api.exception(process=func.__name__, meta=meta, exception_text=traceback.format_exc())
        return wrapper
