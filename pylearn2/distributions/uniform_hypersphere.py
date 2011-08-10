import numpy as N
import theano.sandbox.rng_mrg
import theano.tensor as T
RandomStreams = theano.sandbox.rng_mrg.MRG_RandomStreams
from theano import config
from scipy.special import gammaln

class UniformHypersphere(object):
    def __init__(self, dim, radius):
        self.dim = dim
        self.radius = radius

        self.s_rng = RandomStreams(42)

        log_C = ( float(self.dim)/2.) * N.log(N.pi) - gammaln(1. +float(self.dim)/2.)

        self.logZ = N.log(self.dim) + log_C + (self.dim-1)*N.log(radius)

        assert not N.isnan(self.logZ)
        assert not N.isinf(self.logZ)

    def free_energy(self, X):
        #design matrix format

        return T.zeros_like(X[:,0])

    def log_prob(self, X):
        return - self.free_energy(X) - self.logZ

    def random_design_matrix(self, m):
        Z = self.s_rng.normal(size=(m, self.dim),
                              avg=0., std=1., dtype=config.floatX)


        Z.name = 'UH.rdm.Z'

        sq_norm_Z = T.sum(T.sqr(Z),axis=1)

        sq_norm_Z.name = 'UH.rdm.sq_norm_Z'

        eps = 1e-6
        mask = sq_norm_Z < eps

        mask.name = 'UH.rdm.mask'

        Z = (Z.T*(1.-mask)+mask).T

        Z.name = 'UH.rdm.Z2'

        sq_norm_Z = sq_norm_Z * (1.-mask)+self.dim * mask

        sq_norm_Z.name = 'UH.rdm.sq_norm_Z2'

        norm_Z = T.sqrt(sq_norm_Z)

        norm_Z.name = 'UH.rdm.sq_norm_Z2'

        rval = self.radius *(Z.T/norm_Z).T

        rval.name = 'UH.rdm.rval'

        return rval

