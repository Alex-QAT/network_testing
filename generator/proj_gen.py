from model.proj_mod import Proj
import random
import string
import os.path
import jsonpickle
import getopt
import sys

try:
    opts, args = getopt.getopt(sys.argv[1:], "n:f:", ["number of projects", "file"])
except getopt.GetoptError as err:
    # print help information and exit:
    print(err)  # will print something like "option -a not recognized"
    getopt.usage()
    sys.exit(2)

n = 1
f = "data/projects.json"

for o, a in opts:
        if o == "-n":
            n = int(a)
        elif o == "-f":
            f = a


def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + string.punctuation
    return prefix + "".join([random.choice(symbols)
                             for i in range(random.randrange(maxlen))])

testdata = [Proj(name=random_string("=name=", 10), description=random_string("=descr=", 20))
                                                     for i in range(n)]

file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", f)

with open(file, "w") as f_out:
    jsonpickle.set_encoder_options("json", indent=2)
    f_out.write(jsonpickle.encode(testdata))