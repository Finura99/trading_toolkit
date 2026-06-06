def log_execution(func):
    def wrapper():
        print (f"Starting function... {func.__name__}")
        func()
        print(f"Finished function... {func.__name__}")

    return wrapper

    

@log_execution
def say_hello():
    print("Hello")

say_hello()