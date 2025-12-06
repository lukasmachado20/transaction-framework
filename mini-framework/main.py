# Cache Mini-framework in Python
# Author: Lukas Silva Machado (lukasmachado.developer@gmail.com)

# Objective: Create a decorator method to save the parameters in a file and store the results.

import hashlib
import logging

import functools
import json
from typing import Callable, Any, Tuple

# To start the implementation, we store the cached values of the function in a dictionary
CACHED_VALUES = {}
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


def cached_function_key(func_name: str, func_args: Tuple): 
    dumped_func_args = json.dumps(func_args, separators=[";", ":"]) 
    dumped_func_args = f"{func_name}_{dumped_func_args[1:-1]}"

    hashed_key = hashlib.sha256()
    hashed_key.update(dumped_func_args.encode())

    return hashed_key.hexdigest()


def cache_result(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        cache_key = cached_function_key(func_name=func.__name__, func_args=tuple([*args, kwargs]))
        if cache_key in CACHED_VALUES.keys():
            _logger.info("returning value cached...")
            return CACHED_VALUES[cache_key]
        else:
            value = func(*args, **kwargs)
            _logger.info("caching the value...")
            CACHED_VALUES[cache_key] = value
        return value
    return wrapper

@cache_result
def testing_decorator(value1: float, value2: float):
    return (value1 ** value2 / 4) * 100


def main() -> None:
    print(testing_decorator(12, 14))
    print(testing_decorator(12, 14))
    print(CACHED_VALUES)



if __name__ == "__main__":
    main()