import timeit

TIMES = 10

SETUP = """
def is_prime(x):
    return not any(x % i == 0 for i in range(x-1,1,-1))

def is_prime_rev(x):
    metade = (x//2)+1
    for i in range(2,metade,1):
        if x//i == x/i:
            #print(f'Divisivel por {i}')
            return False
    #print(f'{x} é primo')
    return True

def is_prime_rev_mod(x):
    metade = (x//2)+1
    for i in range(2,metade,1):
        if not x % i:
            #print(f'Divisivel por {i}')
            return False
    #print(f'{x} é primo')
    return True
"""

def is_prime(x):
    return not any(x//i == x/i for i in range(x-1,1,-1))

def is_prime_rev(x):
    metade = (x//2)+1
    for i in range(2,metade,1):
        if x//i == x/i:
            #print(f'Divisivel por {i}')
            return False
    #print(f'{x} é primo')
    return True

def is_prime_rev_mod(x):
    metade = (x//2)+1
    for i in range(2,metade,1):
        if not x % i:
            #print(f'Divisivel por {i}')
            return False
    #print(f'{x} é primo')
    return True

def clock(label, cmd):
    res = timeit.repeat(cmd, setup=SETUP, number=TIMES, repeat=5)
    print(label, *('{:.3f}'.format(x) for x in res))

clock('is_prime                :', 'is_prime(1430243)')
clock('is_prime_rev_metade     :', 'is_prime_rev(1430243)')
clock('is_prime_rev_mod_metade :', 'is_prime_rev_mod(1430243)')


"""
is_prime                : 3.985 4.164 4.314 4.307 4.235
is_prime_rev_metade     : 1.939 2.035 1.900 2.100 2.043
is_prime_rev_mod_metade : 1.087 1.127 1.029 0.989 1.000
"""

