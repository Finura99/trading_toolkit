def reverse_string(symbol: str) -> str:
    return symbol[::-1] #reversed using a slicing method


def log_execution(func): #decorator

    def wrapper(*args, **kwargs):
        print(f"Running function: {func.__name__}") # extended behaviour before-------

        result = func(*args, **kwargs)

        print(f"Finished function: {func.__name__}") # extended behaviour after------

        return result
    return wrapper



