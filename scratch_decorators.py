
def log_execution(obj):
    def wrapper(*args, **kwargs): 
        # *args are variable arguments stored in a tuple.
        # kwrgs are variable key word arguments stored in a dict.
        print(f"Started {obj.__name__}") # before behaviour
        result = obj(*args,**kwargs)
        print(f"Stopped {obj.__name__}") # after behaviour
        
        return result
        
    
    return wrapper



@log_execution
def calculate_fee(price):
    return price * 0.01


print(calculate_fee(100))

