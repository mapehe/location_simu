import numpy as np
import re

total_time = 0
total_jobs = 0

def write_sbatch(dim, df, mah, n):

    global total_time, total_jobs

    # Execution time: Linear estimate, sample size 100 => 6s
    ex_time = float(6)/float(100)*n
    ex_time = max(ex_time, 10)
    total_time += ex_time
    total_jobs += 1
    m, s = divmod(ex_time, 60)
    h, m = divmod(m, 60)
    outfile = "out/dim%s-df%s-mah%s.csv" %(dim, df, mah)
    if mah != 2:
        jobscript = '''#!/bin/bash
        #SBATCH -t %d:%02d:%02d
        #SBATCH --mem-per-cpu=100M
        #SBATCH -o debug.out
        srun python simu.py 2000 %s %s %s %s --mah %s --ofile %s''' % (h, m, s, n, int(np.sqrt(n)), df, dim, mah, outfile)
    else:
        jobscript = '''#!/bin/bash
        #SBATCH -t %d:%02d:%02d
        #SBATCH --mem-per-cpu=100M
        #SBATCH -o debug.out
        srun python simu.py 2000 %s %s %s %s --known --ofile %s''' % (h, m, s, n, int(np.sqrt(n)), df, dim, outfile)
    jobscript = re.sub("\n +", "\n", jobscript)
    with open("jobs/dim%s-df%s-n%s-mah%s.sbatch" %(dim, df, n, mah), "w") as f:
        f.write(jobscript)

for dim in [3, 20]:
    for df in [5, 10]:
        for mah in range(3):
            for r in range(25):
                n = (r+1)*20
                write_sbatch(dim, df, mah, n)

m, s = divmod(total_time, 60)
h, m = divmod(m, 60)

print "%s jobs generated in total, estimated total time %d:%02d:%02d" %(total_jobs, h, m, s)

