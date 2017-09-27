import os
import numpy as np

files = os.listdir("out")

ERRORS = 0

def generate_command(f, count):
    
    n         =   int(re.sub(".+n([0-9]+?)-.+", "\\1", f))
    dim       =   int(re.sub(".+dim([0-9]+?)-.+", "\\1", f))
    df        =   int(re.sub(".+df([0-9]+?)-.+", "\\1", f))
    mah       =   int(re.sub(".+mah([0-9]+?)-.+", "\\1", f))
    outfile   =   "out/n%s-dim%s-df%s-mah%s.csv" %(n, dim, df, mah)

    if mah != 2:
        params = "2000 %s %s %s %s --mah %s --ofile %s" % (n, int(np.sqrt(n)), df, dim, mah, outfile)
    else:
        params = "2000 %s %s %s %s --known --ofile %s" % (n, int(np.sqrt(n)), df, dim, outfile)

    with open("jobs/%s.in" %count, "w") as f:
        f.write(params)


for f in files:
    if np.genfromtxt(os.path.join("out", f), delimiter=";").shape != (2001,):
        ERRORS += 1
        generate_command(f, ERRORS)

if ERRORS == 0:
    print "Completed without errors."
else:
    print "There were %s errors." %ERRORS

