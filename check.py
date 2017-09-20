import os
import numpy as np

files = os.listdir("out")

for f in files:
    s = np.genfromtxt(os.path.join("out", f), delimiter=";")
    print "Array in %s: %s" % (f, s.shape) 
