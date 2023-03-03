import sys
import logging
from logging import NullHandler

from .hawkflow_decorators import HawkflowTimed, HawkflowMetrics, HawkflowException


logging.getLogger(__name__).addHandler(NullHandler())

