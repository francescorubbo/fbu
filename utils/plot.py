import numpy as np
import pylab as plab
import matplotlib.pyplot as plt

def plotarray(todraw, outfilename='foo.png'):
    plab.figure()
    plab.hist(todraw, bins=50)
    plab.xlabel('unfold Ac')
    plab.ylabel('number of events')
    plab.title('posterior distribution of unfolded Ac')
    plab.savefig('%s.eps'%outfilename)

def plotarraymulti(todraw, outfilename='foo.png'):
    plt.figure()
    bins = np.linspace(-0.05, 0.15, 50)
    plt.hist(todraw[0], bins, histtype='stepfilled', normed=False, color='b',
             label='7TeV RMS=%f (WRONG--FIXME)'%(np.std(todraw[0])))
    plt.hist(todraw[1], bins, histtype='stepfilled', normed=False, color='r', alpha=0.5,
             label='8TeV RMS=%f (WRONG--FIXME)'%(np.std(todraw[1])))
    plt.title("Gaussian/Uniform Histogram")
    plt.xlabel('unfold Ac')
    plt.ylabel('number of events')
    plt.title('posterior distribution of unfolded Ac')
    plt.legend()
    plt.savefig(outfilename)
