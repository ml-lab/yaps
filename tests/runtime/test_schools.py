import pystan
import numpy as np
import yaps
from .utils import compare_fit_objects, global_num_chains,global_num_iterations,global_random_seed

def test_schools():
    stan_code = """
    data {
        int<lower=0> J; // number of schools
        real y[J]; // estimated treatment effects
        real<lower=0> sigma[J]; // s.e. of effect estimates
    }
    parameters {
        real mu;
        real<lower=0> tau;
        real eta[J];
    }
    transformed parameters {
        real theta[J];
        for (j in 1:J)
            theta[j] = mu + tau * eta[j];
    }
    model {
        eta ~ normal(0, 1);
        y ~ normal(theta, sigma);
    }
    """

    # Round Trip from Stan to Yaps to Stan
    yaps_code = yaps.from_stan(code_string=stan_code)
    generated_stan_code = yaps.to_stan(yaps_code)

    # Add Data
    schools_dat = {'J': 8,
                'y': [28,  8, -3,  7, -1,  1, 18, 12],
                'sigma': [15, 10, 16, 11, 9, 11, 10, 18]}

    # Compile and fit original stan code
    sm1 = pystan.StanModel(model_code=str(stan_code))
    fit_stan = sm1.sampling(data=schools_dat, iter=global_num_iterations, chains=global_num_chains, seed=global_random_seed)

    # Compile and fit stan code generated by yaps
    sm2 = pystan.StanModel(model_code=str(generated_stan_code))
    fit_generated_stan = sm2.sampling(data=schools_dat, iter=global_num_iterations, chains=global_num_chains, seed=global_random_seed)

    compare_fit_objects(fit_stan, fit_generated_stan)

    # # Visualize
    # print(fit)
    # # if matplotlib is installed (optional, not required), a visual summary and
    # # traceplot are available
    #import matplotlib.pyplot as plt
    # fit.plot()
    # plt.show()

