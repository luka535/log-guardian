import logging
import sys
from pythonjsonlogger import jsonlogger

def get_logger(name):

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        log_handler = logging.StreamHandler(sys.stdout)
        
        formatter = jsonlogger.JsonFormatter(
            '%(asctime)s %(name)s %(levelname)s %(message)s'
        )
        
        log_handler.setFormatter(formatter)
        
        logger.addHandler(log_handler)
    
    logger.propagate = False
    
    return logger

if __name__ == "__main__":
    log = get_logger("TestLogger")
    log.info("This is an info message from the test block.")
    log.warning("This is a warning message.", extra={'user': 'testuser', 'request_id': '123'})
    try:
        result = 1 / 0
    except ZeroDivisionError:
        log.error("A division by zero error occurred!", exc_info=True)