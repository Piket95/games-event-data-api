import os
import time

class Log:

    # this is a property that gets evaluated on each access and can be used like a class variable (Log.meta_info or self.meta_info)
    @property
    def meta_info(self):
        return f'[{os.getenv("ENVIRONMENT", "PROD")}] [{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}]'

    def __call__(self, message):
        """Standard-Logging-Methode"""
        print(f'{self.meta_info} - {message}')

    def success(self, message):
        """Fehler-Logging-Methode"""
        print(f'\033[92m{self.meta_info} - {message}\033[0m')

    def error(self, message):
        """Fehler-Logging-Methode"""
        print(f'\033[91m{self.meta_info} - {message}\033[0m')