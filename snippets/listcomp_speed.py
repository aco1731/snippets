import timeit

TIMES = 10000

SETUP = """
symbols = '$¢£¥€¤abceder$$$$'
def non_ascii(c):
    return c > 127
"""

def is_prime(x):
    return not any(x//i == x/i for i in range(x-1,1,-1))

def is_prime_rev(x):
    metade = (x//2)+1
    for i in range(2,metade,1):
        if x//i == x/i:
            print(f'Divisivel por {i}')
            return False
    print(f'{x} é primo')
    return True

def is_prime_mod(x):
    metade = (x//2)+1
    for i in range(2,metade,1):
        if not x % i:
            print(f'Divisivel por {i}')
            return False
    print(f'{x} é primo')
    return True

def clock(label, cmd):
    res = timeit.repeat(cmd, setup=SETUP, number=TIMES, repeat=5)
    print(label, *('{:.3f}'.format(x) for x in res))

clock('listcomp        :', '[ord(s) for s in symbols if ord(s) > 127]')
clock('listcomp + func :', '[ord(s) for s in symbols if non_ascii(ord(s))]')
clock('filter + lambda :', 'list(filter(lambda c: c > 127, map(ord, symbols)))')
clock('filter + func   :', 'list(filter(non_ascii, map(ord, symbols)))')
