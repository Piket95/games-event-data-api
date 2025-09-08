import os
import time
import inspect

class Log:

    silent_meta_info = False

    # this is a property that gets evaluated on each access and can be used like a class variable (Log.meta_info or self.meta_info)
    @property
    def meta_info(self):
        caller_frame = inspect.currentframe().f_back.f_back
        caller_function = inspect.getframeinfo(caller_frame).function
        caller_function = caller_function if caller_function != "<module>" else "Main"
        return f'[{os.getenv("ENVIRONMENT", "PROD")}] [{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}] [{caller_function}]'

    def __init__(self, silent=False):
        self.silent_meta_info = silent
    

    def __call__(self, message):
        """Standard-Logging-Methode"""
        print(f'{self.meta_info if not self.silent_meta_info else ""} - {message}')

    def success(self, message):
        """Fehler-Logging-Methode"""
        print(f'\033[92m{self.meta_info if not self.silent_meta_info else ""} - {message}\033[0m')

    def error(self, message):
        """Fehler-Logging-Methode"""
        print(f'\033[91m{self.meta_info if not self.silent_meta_info else ""} - {message}\033[0m')