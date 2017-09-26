import numpy as np
import re

total_time = 0
total_jobs = 0

def write_sbatch(dim, df, mah, n):
    global total_jobs
    total_jobs += 1
    if mah != 2:
        params = "2000 %s %s %s %s --mah %s --ofile %s" % (n, int(np.sqrt(n)), df, dim, mah, outfile)
    else: 
        params = "2000 %s %s %s %s --known --ofile %s" % (n, int(np.sqrt(n)), df, dim, outfile)
    with open("jobs/%s.in" %(total_jobs), "w") as f:
        f.write(params)

for dim in [3, 20]:
    for df in [5, 10]:
        for mah in range(3):
            for r in range(1000):
                if r == 0:
                    continue
                n = 100*r
                write_sbatch(dim, df, mah, n)

print "%s jobs generated in total" %(total_jobs)

