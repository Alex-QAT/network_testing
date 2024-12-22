from model.proj_mod import Proj

import random
import string

def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + string.punctuation + " "*10
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])

testdata = [Proj(name=random_string("=name=", 10), description=random_string("=descr=", 20))
            for i in range(5)
            ]