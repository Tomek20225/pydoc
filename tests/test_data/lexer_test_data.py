from typing import List, Callable, Any
import sys

class SuperException:
    ...

class   Foo:
    a = None
    b: int = -2

    def __init__(self):
        temp = self.a + 3
        self.b = temp

    def greeting(self, msg: str):
        print(msg)

class Bar(Foo):
    def shout(self):
        super().greeting("I'm screaming!")

class Baz(Foo, Bar, SuperException):
    pass

def bar(x: int, y: str) -> List[int]:
    return [x, len(y)]

def func_without_args():
    pass

def func_with_args(key, pop):
    pass

def func_with_typed_args(key: str, pop: Callable[[Any], int]):
    pass

def func_with_typed_args_and_defaults(key: str = 'Default key', pop: Callable[[Any], int] = lambda x: 3.33):
    pass

def func_with_defaults(key = "Default key", pop = lambda x: 20):
    pass

if "__main__" == __name__:
    random_num = bar(
        10,
        y=sys.argv[0]
    )
    for i in random_num:
        i *= 2.5
        print(i)
else:
    def_anon = lambda x: x + 1
    classless_freak = def_anon(3_0)
    for i in range(classless_freak):
        print(i)

"Adam \" night"