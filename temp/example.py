from typing import List
import sys

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

def bar(x: int, y: str) -> List[int]:
    return [x, len(y)]

if "__main__" == __name__:
    random_num = bar(
        1,
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