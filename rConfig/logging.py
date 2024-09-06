import logging

class Logger:
    def __init__(self):
        self.logger = logging.getLogger('rConfig')
    
    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, args, kwargs)
    
    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, args, kwargs)
    
    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, args, kwargs)
    
    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, args, kwargs)
    
    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, args, kwargs)