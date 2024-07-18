import threading
import time
import traceback
import uuid

from ._validation import _validate_api_key
from ._validation import _clean_process, _clean_meta, _validate_core
from ._hawkflow_exceptions import HawkFlowIntervalLengthException
from .hawkflow_api import HawkflowAPI


class Heart:
    def __init__(self, app_name, meta, interval_minutes, api_key):
        self.app_name = _clean_process(app_name)
        self.meta = _clean_meta(meta)

        _validate_core(app_name, meta)

        self.api_key = _validate_api_key(api_key)
        self.hf_api = HawkflowAPI(api_key)
        self.interval_minutes = interval_minutes
        self.keep_running = True
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def start_beat(self):
        heartbeat_uuid = str(uuid.uuid4())
        self.hf_api.start(process=self.app_name, meta=self.meta, uid=heartbeat_uuid)
        time.sleep(0.5)
        self.hf_api.end(process=self.app_name, meta=self.meta, uid=heartbeat_uuid)

    def run(self):
        while self.keep_running:
            try:
                self.start_beat()
                time.sleep(self.interval_minutes*60)
            except Exception as e:
                self.hf_api.exception(self.app_name, "heartbeat", exception_text=traceback.format_exc())
                print(f"Error in Hawkflow HeartBeat: {traceback.format_exc()}")

    def stop(self):
        self.keep_running = False
        self.thread.join()

    @staticmethod
    def beat(app_name, meta="heartbeat", interval_minutes=60, api_key=""):
        if interval_minutes < 15:
            raise HawkFlowIntervalLengthException()
        return Heart(app_name, meta, interval_minutes, api_key)



