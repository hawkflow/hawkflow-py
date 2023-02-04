def _docs_url():
    return "Please see docs at https://docs.hawkflow.ai/integration/index.html"


class HawkFlowException(Exception):
    def __init__(self, message=""):
        self.message = message

    def __str__(self):
        pass


class HawkFlowNoApiKeyException(HawkFlowException):
    def __str__(self):
        self.message = repr(f"HawkFlow API no HawkFlow API Key set. {_docs_url()}")
        return self.message


class HawkFlowApiKeyFormatException(HawkFlowException):
    def __str__(self):
        self.message = repr(f"HawkFlow API invalid API Key format. {_docs_url()}")
        return self.message


class HawkFlowDataTypesException(HawkFlowException):
    def __str__(self):
        self.message = repr(f"HawkFlow API HawkFlow data types not set correctly. {self.message}. {_docs_url()}")
        return self.message


class HawkFlowMetricsException(HawkFlowException):
    def __str__(self):
        self.message = repr(f"HawkFlow API @HawkflowMetrics missing items parameter. {_docs_url()}")
        return self.message
