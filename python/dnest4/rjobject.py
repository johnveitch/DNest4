import numpy as np
import numpy.random as rng

__all__ = ["RJObject", "ConditionalPrior"]

class ConditionalPrior:
    """
    An object of this class describes p(theta | alpha) and
    the current value of alpha. This is a 'ClassicMassInf' example
    you can adapt to your own purposes.
    """
    def __init__(self):
        # Known hyperparameters
        self.x_min, self.x_max = -10.0, 10.0

        # Unknown hyperparameter
        self.mu = 0.0

    def from_prior(self):
        # Log-uniform prior for mu
        self.mu = np.exp(np.log(1E-3) + np.log(1E6)*rng.rand())

    def to_uniform(self, components):
        """
        Transform components to U(0, 1)
        """
        # Uniform prior for positions
        components[:,0] = (components[:,0] - self.x_min)\
                                /(self.x_max - self.x_min)

        # Exponential prior for amplitudes (given mu)
        components[:,1] = 1. - np.exp(-components[:,1]/self.mu)

    def from_uniform(self, components):
        """
        Transform components from U(0, 1)
        """
        # Uniform prior for positions
        components[:,0] = self.x_min + (self.x_max - self.x_min)*components[:,0]

        # Exponential prior for amplitudes (given mu)
        components[:,1] = -self.mu*np.log(1.0 - components[:,1])

    def log_pdf(self, components):
        """
        Evaluate the density p(x|alpha)
        """
        # Check hard boundaries
        if np.any((components[:,0] < self.x_min) |\
                                (components[:,0] > self.x_max)):
            return -np.Inf
        if np.any(components[:,1] < 0.0):
            return -np.Inf

        # Uniform density for position,
        # exponential density for amplitude
        return -np.log(self.x_max - self.x_min)\
               -np.log(self.mu) - np.sum(components[:,1])/self.mu


class RJObject:
    """
    An RJObject is a collection of N objects where N is unknown
    and the objects' properties may have a hierarchically-specified
    prior distribution.
    """

    def __init__(self, N_max, ndim, conditional_prior):
        """
        N_max (default=10): The maximum number of components allowed
        ndim = dimensionality of the parameter space of a component
        conditional_prior = ConditionalPrior object
        """
        self.N_max = N_max
        self.ndim = ndim
        self.N = 0
        self.components = np.empty((self.N_max, ndim))
        self.conditional_prior = conditional_prior

    def from_prior(self):
        """
        Generate hyperparameters and components from the prior
        """
        self.N = rng.randint(self.N_max + 1)
        self.conditional_prior.from_prior()
        self.components[0:self.N, :] = rng.rand(self.N, self.ndim)
        self.conditional_prior.from_uniform(self.components[0:self.N, :])

    def perturb(self):
        """
        Metropolis-Hastings proposal
        """

        # Choose a proposal type
        choice = rng.rand_int(5)


    def perturb_N(self):
        """
        Propose a new value for N using birth-death
        """
        pass


if __name__ == "__main__":
    """
    Do some tests.
    """
    import matplotlib.pyplot as plt
    rng.seed(1)

    # Generate an RJObject from the prior five times.
    rjobject = RJObject(10, 2, ConditionalPrior())

    for i in range(0, 5):
        rjobject.from_prior()
        print("N =", rjobject.N)

        if rjobject.N >= 1:
            plt.hist(rjobject.components[0:rjobject.N,0], 100,
                        weights=rjobject.components[0:rjobject.N,1])
            plt.xlim([rjobject.conditional_prior.x_min,\
                            rjobject.conditional_prior.x_max])
            plt.show()

    # Now check that the conditional_prior.to_uniform and from_uniform
    # are truly inverses of each other
    x = rng.rand(100, 100)
    y = x.copy()
    rjobject.conditional_prior.from_uniform(y)
    rjobject.conditional_prior.to_uniform(y)
    print("to_uniform and from_uniform are inverses:", np.allclose(x, y))

