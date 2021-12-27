# Celem tego projektu jest napisanie dekoratora, który timinguje czas wykonania funkcji i wyświetla wynik na konsoli. 
# Dekorator jako parametr ma przyjmować liczbę powtórzeń funkcji (domyślnie jedno), a czas wykonania ma być po tych powtórzeniach uśredniany. 
# Dekorator ma działać zarówno z jak i bez podawania parametrów.

from numpy.lib.function_base import average
from rich.console import Console
import rich.traceback
import functools
import time

console = Console()
console.clear()
rich.traceback.install()


def called_decorator(_func = None, iterations = 1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

             t = []
             for i in range(iterations):
                start_time = time.time()
                res = func()
                end_time = time.time()
                t.append (end_time - start_time)
                console.print(f'Called {i+1} with time: {end_time - start_time}')
             
             if iterations is not 1:
                 console.print(f'Average time: {average(t)}')

             return func(*args, **kwargs)

        return wrapper

    if _func is not None:
        return decorator(_func)
        
    return decorator


#@called_decorator
def fun():
    a = 1
    for i in range(100000):
        a = a + a

    return a


fun = called_decorator(fun)
fun()

# fun = called_decorator(iterations=4)(fun)
# fun()


