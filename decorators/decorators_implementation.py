import logging
import functools
from abc import ABC, abstractmethod
from math import sqrt
from time import perf_counter
from typing import Any, Callable

logger = logging.getLogger(__name__)

def is_prime(number: int) -> bool:
    if number < 2:
        return False
    for element in range(2, int(sqrt(number)) + 1):
        if number % element == 0:
            return False
    return True


# Implementing object-oriented decorator
class AbstractComponent(ABC):
    @abstractmethod
    def execute(self, upper_bound: int) -> int:
        pass


class ConcreteComponent(AbstractComponent):
    def execute(self, upper_bound: int) -> int:
        count = 0
        for number in range(upper_bound):
            if is_prime(number):
                count += 1
        return count


class AbstractDecorator(AbstractComponent):
    def __init__(self, decorated: AbstractComponent) -> None:
        self._decorated = decorated


class BenchmarkDecorator(AbstractDecorator):
    def execute(self, upper_bound: int) -> int:
        start_time = perf_counter()
        value = self._decorated.execute(upper_bound)
        end_time = perf_counter()
        run_time = end_time - start_time
        logging.info(
            f"Execution of {self._decorated.__class__.__name__} took {run_time:.2f} second"
        )
        return value


class LoggingDecorator(AbstractDecorator):
    def execute(self, upper_bound: int) -> int:
        logging.info(f"Calling {self._decorated.__class__.__name__} ...")        
        value = self._decorated.execute(upper_bound)
        logging.info(f"Finished {self._decorated.__class__.__name__} ...")        
        return value


# Implementing decorator as pythonic way
def benchmark(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = perf_counter()
        value = func(*args, **kwargs)
        end_time = perf_counter()
        run_time = end_time - start_time
        logging.info(
            f"Execution of {func.__name__} took {run_time:.2f} second"
        )
        return value
    return wrapper

# decorator with arguments
# def with_logging(logger: logging.Logger):
#     def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
#         @functools.wraps(func)
#         def wrapper(*args: Any, **kwargs: Any) -> Any:
#             logger.info(f"Calling {func.__name__} ...")        
#             value = func(*args, **kwargs)
#             logger.info(f"Finished {func.__name__} ...")        
#             return value

#         return wrapper
#     return decorator

# other form to implement params 

def with_logging(func: Callable[..., Any], logger: logging.Logger) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.info(f"Calling {func.__name__} ...")        
        value = func(*args, **kwargs)
        logger.info(f"Finished {func.__name__} ...")        
        return value

    return wrapper

with_default_logging = functools.partial(with_logging, logger=logger)


@with_default_logging
@benchmark
def count_prime_numbers(upper_bound: int) -> int:
    count = 0
    for number in range(upper_bound):
        if is_prime(number):
            count += 1
    return count



def main() -> None:
    logging.basicConfig(level=logging.INFO)
    # component = ConcreteComponent()
    # benchmark_decorator = BenchmarkDecorator(component)
    # logging_decorator = LoggingDecorator(benchmark_decorator)
    # prime_numbers = logging_decorator.execute(100000)
    # logging.info(f"Found {prime_numbers} prime numbers.")
    value = count_prime_numbers(10000)
    logger.info(f"Found {value} prime numbers.")



if __name__ == "__main__":
    main()