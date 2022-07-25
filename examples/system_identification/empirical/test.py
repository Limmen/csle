import math
import torch
import numpy as np
import gpytorch
from matplotlib import pyplot as plt
from csle_common.metastore.metastore_facade import MetastoreFacade


class GPRegressionModelWithGaussianNoise(gpytorch.models.ExactGP):
    def __init__(self, train_x, train_y, likelihood):
        super(GPRegressionModelWithGaussianNoise, self).__init__(train_x, train_y, likelihood)
        self.mean_module = gpytorch.means.ConstantMean()
        self.covar_module = gpytorch.kernels.ScaleKernel(gpytorch.kernels.RBFKernel())

    def forward(self, x):
        mean_x = self.mean_module(x)
        covar_x = self.covar_module(x)
        return gpytorch.distributions.MultivariateNormal(mean_x, covar_x)

if __name__ == '__main__':
    emulation_env_config = MetastoreFacade.get_emulation_by_name("csle-level9-001")
    emulation_statistic = MetastoreFacade.get_emulation_statistic(id=10)

    conditionals = ["no_intrusion"]
    metrics = ["alerts_weighted_by_priority"]
    empirical_conditionals = []
    max_val = 0
    for i, conditional in enumerate(conditionals):
        for j, metric in enumerate(metrics):
            counts = emulation_statistic.conditionals_counts[conditional][metric]
            for val,count in counts.items():
                if val > max_val:
                    max_val = val
    sample_space = list(range(0, max_val))
    # sample_space = np.arange(0,max_val, 1)
    # sample_space = list(range(0, 5000))
    observed_x = []
    observed_y = []
    emulation_statistic.compute_descriptive_statistics_and_distributions()
    for val,prob in emulation_statistic.conditionals_probs["no_intrusion"]["alerts_weighted_by_priority"].items():
        observed_x.append(val)
        observed_y.append(prob)

    observed_x = torch.tensor(observed_x)
    observed_y = torch.tensor(observed_y)

    # initialize likelihood and model, the Gaussian likelihood assumes observed data points have zero mean gaussian noise
    likelihood = gpytorch.likelihoods.GaussianLikelihood()
    model = GPRegressionModelWithGaussianNoise(observed_x, observed_y, likelihood)

    # get into train mode
    model.train()
    likelihood.train()

    # Use the adam optimizer
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)  # Includes GaussianLikelihood parameters

    # "Loss" for GPs - the marginal log likelihood
    mll = gpytorch.mlls.ExactMarginalLogLikelihood(likelihood, model)

    training_iter = 2

    # Find optimal model hyperparameters by minimizing the negative marignal likelihood loss through gradient descent.
    for i in range(training_iter):
        # Zero gradients from previous iteration
        optimizer.zero_grad()
        # Output from model
        output = model(observed_x)
        # Calc loss and backprop gradients
        loss = -mll(output, observed_y)
        loss.backward()
        print('Iter %d/%d - Loss: %.3f   lengthscale: %.3f noise: %.3f' % (
            i + 1, training_iter, loss.item(),
            model.covar_module.base_kernel.lengthscale.item(),
            model.likelihood.noise.item()
        ))
        optimizer.step()


    # Get into evaluation (predictive posterior) mode
    model.eval()
    likelihood.eval()

    # Test points are regularly spaced along [0,1]
    # Make predictions by feeding model through likelihood
    with torch.no_grad(), gpytorch.settings.fast_pred_var():
        # print(np.array(sample_space)[::500])
        test_x = torch.tensor(sample_space[::100])
        # print(test_x)
        # print(model(test_x))
        # torch.linspace(0, 1, 51)
        observed_pred = likelihood(model(test_x))

    with torch.no_grad():
        # Initialize plot
        f, ax = plt.subplots(1, 1, figsize=(4, 3))

        # Get upper and lower confidence bounds
        lower, upper = observed_pred.confidence_region()
        # Plot training data as black stars
        ax.plot(observed_x.numpy()[::100], observed_y.numpy()[::100], 'k*')
        # Plot predictive means as blue line
        ax.plot(test_x.numpy(), observed_pred.mean.numpy(), 'b')
        # Shade between the lower and upper confidence bounds
        # ax.fill_between(test_x.numpy(), lower.numpy(), upper.numpy(), alpha=0.5)
        # ax.set_ylim([-3, 3])
        ax.legend(['Observed Data', 'Mean', 'Confidence'])
        plt.show()