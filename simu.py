import numpy as np
import argparse
import ast 

"""
    Arguments:
    
        r   ---   A vector of the generating variates.
        mu  ---   Location
        L   ---   Scatter

    Value:  Elliptically distributed random numbers corrseponding
            To the values r.
"""
def pull_elliptical(r, mu, L):
    
    # Dimension
    dim = len(mu)

    # A random point on the unit sphere
    U = np.random.normal(size=dim)
    U = U/np.linalg.norm(U)

    return mu + r*np.matmul(L, U)

"""
    Arguments:

        sample  ---   A vector of non-negative numbers

    Value:  Hill estimator evaluated given the input "sample"
"""
def hill(sample):
    sample = sorted(np.array(sample))
    sample = np.log(sample)-np.log(sample[0])
    return np.mean(sample[1:])


"""
    Arguments:
        
        n     ---   Sample size
        df    ---   Degrees of freedom
        mu    ---   Location
        L     ---   Scatter
"""
def single_sample(n, df, mu, L):
    rs = np.random.standard_t(df, size = n)
    return np.array([pull_elliptical(r, mu, L) for r in rs])


"""
    Arguments:
        
        xs    ---   Elliptically distributed random vectors.
        mah   ---   (Boolean) Use an elliptical norm.

    Value:  Norms of the vectors xs.
"""
def norms(xs, mah=True):
    xs = np.array(xs)
    if mah:
        mu_ = np.mean(xs, axis=0)
        sg_ = np.cov(xs.T)
        inv = np.linalg.inv(sg_)
        return [np.sqrt(np.dot(x-mu_, np.matmul(inv, x-mu_))) for x in xs]
    else:
        return [np.linalg.norm(x) for x in xs]

"""
    Arguments:

        n   ---   Sample size
        k_n ---   Tail threshold
        df  ---   Degrees of freedom (Student-t)
        mu  ---   Location
        L   ---   Scatter

"""
def single_round(n, k_n, df, mu, L, mah=True):
    return hill(sorted(norms(single_sample(n,df,mu,L),mah=mah))[n-k_n:])




"""
    Arguments:

        bign  ---   Rounds
        n     ---   Sample size
        k_n   ---   Tail threshold
        df    ---   Degrees of freedom (Student-t)
        mu    ---   Location
        L     ---   Scatter
        ofile ---   Ouput file
"""
def main(bign, n, k_n, df, mu, L, mah=True, ofile="out.csv"):
    with open(ofile, "a") as f:
        out = [single_round(n, k_n, df, mu, L, mah) for _ in range(bign)]
        f.write(str(n)+";"+";".join(map(str, out))+"\n")

if __name__ == "__main__":
    arg = argparse.ArgumentParser()
    
    # Compulsory arguments
    arg.add_argument("rounds", type=int, help="the number of times the Hill estimator will be evaluated")
    arg.add_argument("n", type=int, help="the sample size per round")
    arg.add_argument("k_n", type=int, help="the tail threshold")
    arg.add_argument("df", type=float, help="degrees of freedom (Student-t)")
    arg.add_argument("mu", type=str, help="location vector as string")
    arg.add_argument("L", type=str, help="scatter matrix as string")

    # Optional arguments
    arg.add_argument("--ofile", type=str, help = "output file")
    arg.add_argument("--mah", type=int, help = """which norm to use: 0 = l2 norm, 1 = elliptical norm (default)""")

    args = arg.parse_args()

    mu = np.array(ast.literal_eval(args.mu), dtype=np.float64)
    L  = np.array(ast.literal_eval(args.L), dtype=np.float64)

    ofile = "out.csv"
    mah = True

    if args.ofile:
        ofile = args.ofile

    if args.mah == 0:
        mah = False

    main(args.rounds, args.n, args.k_n, args.df, mu, L, mah=mah, ofile=ofile)
