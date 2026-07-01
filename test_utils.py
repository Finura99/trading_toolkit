from src.utils import log_execution


def test_log_execution_returns_original_result():
    @log_execution
    def add_numbers(a, b):
        return a + b
    
    result = add_numbers(2, 3)

    assert result == 5


def test_log_execution_preserves_function_name():
    @log_execution
    def sample_function():
        return "ok"
    
    assert sample_function.__name__ == "sample_function"

# unit tests for decorators and wraps

# without wraps the func.__name__ woudl return wrapper...
