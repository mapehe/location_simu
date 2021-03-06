import numpy as np
import argparse
import ast 
import json

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
def single_round(n, k_n, df, mu, L, mah=True, known=False):
    if not known:
        return hill(sorted(norms(single_sample(n,df,mu,L),mah=mah))[n-k_n:])
    else:
        return hill(sorted(np.random.standard_t(df, size = n))[n-k_n:])



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
def main(bign, n, k_n, df, mu, L, mah=True, ofile="out.csv", known=False):
    with open(ofile, "a") as f:
        out = [single_round(n, k_n, df, mu, L, mah, known=known) for _ in range(bign)]
        f.write(str(n)+";"+";".join(map(str, out))+"\n")

if __name__ == "__main__":
    arg = argparse.ArgumentParser()
    
    # Compulsory arguments
    arg.add_argument("rounds", type=int, help="the number of times the Hill estimator will be evaluated")
    arg.add_argument("n", type=int, help="the sample size per round")
    arg.add_argument("k_n", type=int, help="the tail threshold")
    arg.add_argument("df", type=float, help="degrees of freedom (Student-t)")
    arg.add_argument("dim", type=int, help="dimension (3 or 20)")

    # Optional arguments
    arg.add_argument("--ofile", type=str, help = "output file")
    arg.add_argument("--mah", type=int, help = """which norm to use: 0 = l2 norm, 1 = elliptical norm (default)""")
    arg.add_argument("--known", help= "use known location and scatter", action="store_true")

    args = arg.parse_args()

    with open("param.txt", "r") as f:
        params = json.loads(f.read())

    if args.dim == 3:
        mu = np.asarray(params["location"]["mu3"])
        L  = np.asarray(params["scatter"]["S3"])
    else:
        mu = np.asarray(params["location"]["mu20"])
        L  = np.asarray(params["scatter"]["S20"])

    ofile = "out.csv"
    mah   = True
    known = False

    if args.ofile:
        ofile = args.ofile

    if args.mah == 0:
        mah = False

    if args.known:
        known = True

    main(args.rounds, args.n, args.k_n, args.df, mu, L, mah=mah, ofile=ofile, known=known)
