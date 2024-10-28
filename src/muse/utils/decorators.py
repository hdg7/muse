from functools import wraps


def with_valid_options(**options_metadata):
    """
    Decorator to provide a `foo_valid_options` function alongside `foo` (or any decorated function).

    The options metadata is specified as keyword arguments to the decorator,
    where each argument contains the type, default value, and usage information.
    """

    def decorator(func):
        # Metadata function that returns the options dictionary
        def valid_options():
            return {name: meta for name, meta in options_metadata.items()}

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Add valid_options function to the original function's attributes
            wrapper.valid_options = valid_options
            return func(*args, **kwargs)

        # Attach the valid options dictionary to the decorated function
        wrapper.valid_options = valid_options
        return wrapper

    return decorator
