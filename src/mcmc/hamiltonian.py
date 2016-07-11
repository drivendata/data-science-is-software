# flake8: noqa
from __future__ import print_function

import numpy as np

# this makes matplotlib be called
# happily in a virtualenv from a jupyter notebook
import matplotlib
#matplotlib.use('nbagg')

import matplotlib.pyplot as plt

import prettyplotlib as pplt

blues_rev = pplt.brewer2mpl.get_map('Blues', 'Sequential', 9, reverse=True).mpl_colormap
c1, c2 = pplt.brewer2mpl.get_map('Dark2', 'Qualitative', 8).mpl_colors[3:5]

def run_diagnostics(samples, function=None, plots=True):
    if plots:
        xlim = (-0.5, 1.5)
        ylim = (-1.5, 1.)

        # plot the sample distribution
        plt.hist2d(samples[:,0], samples[:,1], bins=50, cmap=blues_rev)

        # overlay the true function
        if function:
            plot_true_function(function, xlim, ylim)

        plt.show()

        plot_diagnostics(samples)

    gelman_rubin(samples)

    # gewecke
    #geweke_val = pymc.diagnostics.geweke(samples, intervals=1)[0][0][1]
    Geweke(samples)


def gelman_rubin(samples):
    # g-r conventionally uses 10 chains
    # we'll assume an appropriate burnin
    # so we can divide our chains into 10
    # seaprate ones
    m_chains = 10
    length, dims = samples.shape
    n_draws = length//m_chains

    # split the chain into 10 subchains
    total_length = n_draws * m_chains
    chain_draws = samples[:total_length,:].reshape(n_draws, m_chains, dims)

    # calculate within chain variance for each dimension
    var_j = np.var(chain_draws, axis=1)
    var_wc = np.mean(var_j, axis=0)

    # calculate between chain variance for each dimension
    mu_j = np.mean(chain_draws, axis=1)
    var_bc = np.var(mu_j, axis=0) * n_draws

    # calculate the estimated variance per dimension
    var = (1 - (1/n_draws))*var_wc + (1/n_draws)*var_bc

    # calculate potential scale reduction factor
    R = np.sqrt(var/var_wc)

    print("The Gelman-Rubin potential scale reduction factor is: ", R, " (< 1.1 indicates good mixing)")

def Geweke(trace, intervals=1, length=200, first=0.1):
    first*=len(trace)
    # take two parts of the chain.
    # subsample lenght
    nsl=length

    z =np.empty(intervals)
    for k in np.arange(0, intervals):
        # beg of each sub samples
        bega=first+k*length
        begb = len(trace)/2 + k*length

        sub_trace_a = trace[bega:bega+nsl]
        sub_trace_b = trace[begb:begb+nsl]

        theta_a = np.mean(sub_trace_a)
        theta_b = np.mean(sub_trace_b)
        var_a  = np.var(sub_trace_a)
        var_b  = np.var(sub_trace_b)

        z[k] = (theta_a-theta_b)/np.sqrt( var_a + var_b)

    print("The Geweke Diagnostic Value is: ", np.abs(z), "(< 1.96 indicates convergence)")


def plot_diagnostics(samples):
    # Samples Trace
    plot_traces(samples)

    # Samples Autocorrelation
    plot_acorr(samples)

def plot_traces(samples):
    lens, dims = samples.shape
    figs, axes = plt.subplots(dims,1)

    for d in range(dims):
        pplt.plot(axes[d], np.arange(lens), samples[:,d])


def plot_acorr(x_vals, maxlags=200):
    figs, axes = plt.subplots(1,2)

    # plot x autocorrelation
    axes[0].acorr(x_vals[:,0]-np.mean(x_vals[:,0]),
                  normed=True,
                  usevlines=False,
                  maxlags=maxlags,
                  color=c1,
                  alpha=0.1)
    axes[0].set_xlim((0, maxlags))
    axes[0].set_title(r"Autocorrelation of $x$")

    # plot y autocorrelation
    axes[1].acorr(x_vals[:,1]-np.mean(x_vals[:,1]),
                  normed=True,
                  usevlines=False,
                  maxlags=1000,
                  color=c2,
                  alpha=0.1)

    axes[1].set_xlim((0, maxlags))
    axes[1].set_title(r"Autocorrelation of $y$")
    plt.show()


def plot_true_function(function, xlim, ylim, ax=None):
    # get plotting object
    ax = plt if not ax else ax

    # plot true function
    xs = np.linspace(xlim[0], xlim[1], 1000)
    ys = np.linspace(ylim[0], ylim[1], 1000)
    XX, YY = np.meshgrid(xs, ys)

    # reshape
    LS = np.vstack([XX.ravel(), YY.ravel()])
    ZZ = function(LS.T).reshape(1000, 1000)

    plt.contour(XX, YY, ZZ.reshape(1000, 1000),
                cmap=pplt.brewer2mpl.get_map('Blues', 'Sequential', 9, reverse=False).mpl_colormap)

def hamiltonian(sample_size, U, K, grad_U, dims=2, L=5, epsilon=0.1, burn_in=10, thinning=10):
    sample_size = (sample_size + burn_in)*thinning

    # initial position
    current_q = np.ones(dims).reshape(-1, dims)

    H = np.zeros(sample_size)
    qall = np.zeros((sample_size, dims))

    for j in np.arange(sample_size):

        q = current_q.copy()

        # draw a new p
        p = np.random.normal(0, 1, dims).reshape(-1, dims)
        current_p = p.copy()

        # Make a half step for momentum at the beginning
        p = p - epsilon * grad_U(q)/2.0

        # alternate full steps for position and momentum
        for i in range(L):
            q = q + epsilon*p

            if (i != L-1):
                p = p - epsilon*grad_U(q)

        #make a half step at the end
        p = p - epsilon*grad_U(q)/2.

        # negate the momentum
        p= -p

        current_U = U(current_q)
        current_K = K(current_p)

        proposed_U = U(q)
        proposed_K = K(p)
        A=np.exp(current_U-proposed_U+current_K-proposed_K)

        # accept/reject
        if np.random.rand() < A:
            current_q = q.copy()
            qall[j,:] = q.copy()
        else:
            qall[j, :] = current_q.copy()

        H[j] = U(current_q)+K(current_p)

    return qall[burn_in::thinning], H[burn_in::thinning]


if __name__ == "__main__":
    f = lambda X: np.exp(-100*(np.sqrt(X[:,1]**2 + X[:,0]**2)- 1)**2 + (X[:,0]-1)**3 - X[:,1] - 5)

    # potential and kinetic energies
    U = lambda q: -np.log(f(q))
    K = lambda p: p.dot(p.T) / 2

    # gradient of the potential energy
    def grad_U(X):
        x, y = X[0,:]

        xy_sqrt = np.sqrt(y**2 + x**2)

        mid_term = 100*2*(xy_sqrt - 1)
        grad_x = 3*((x-1)**2) - mid_term * ((x) / (xy_sqrt))
        grad_y = -1 - mid_term * ((y) / (xy_sqrt))

        return -1*np.array([grad_x, grad_y]).reshape(-1, 2)

    ham_samples, H = hamiltonian(2500, U, K, grad_U)
    run_diagnostics(ham_samples)