import yaml
import logging
from functools import wraps
import time

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

print(config)



def reverse_string(symbol: str) -> str:
    return symbol[::-1] #reversed using a slicing method


def log_execution(func): #decorator
    @wraps(func) # preserves the original function's metadata (name, docstring, etc.) when wrapping it with the decorator
    
    def wrapper(*args, **kwargs): # accepts many arguments the function needs.
        start_time = time.time()
        logging.info(f"Running function: {func.__name__}") # extended behaviour before-------

        result = func(*args, **kwargs)

        duration = time.time() - start_time
        logging.info(f"Finished function: {func.__name__} in {duration:4f}s") # extended behaviour after-------

        return result
    
    return wrapper






