import os
import numpy as np

files = os.listdir("out")

for f in files:
    print "Array in %s: %s" % (f, np.genfromtxt(os.path.join("out", f), delimiter=";").shape) 
