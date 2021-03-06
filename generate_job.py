import numpy as np
import re

total_time = 0
total_jobs = 0

def write_sbatch(dim, df, mah, n):
    global total_jobs
    total_jobs += 1
    outfile = "out/n%s-dim%s-df%s-mah%s.csv" %(n, dim, df, mah)
    if mah != 2:
        params = "2000 %s %s %s %s --mah %s --ofile %s" % (n, int(np.sqrt(n)), df, dim, mah, outfile)
    else:
        params = "2000 %s %s %s %s --known --ofile %s" % (n, int(np.sqrt(n)), df, dim, outfile)
    with open("jobs/%s.in" %(total_jobs), "w") as f:
        f.write(params)

for dim in [3, 20]:
    for df in [5, 10]:
        for mah in range(3):
            for r in range(2000):
                if r == 0:
                    continue
                n = 100*r
                write_sbatch(dim, df, mah, n)

with open("submit.sbatch", "r") as f:
    s = f.read()
    s = re.sub("--array=.+?\n", "--array=1-%s\n" %(total_jobs), s)

with open("submit.sbatch", "w") as f:
    f.write(s)

