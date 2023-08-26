import gpytorch


class GPRegressionModelWithGaussianNoise(gpytorch.models.ExactGP):
    """
    DTO representing a GPRegression model with Gaussian Noise
    """

    def __init__(self, train_x, train_y, likelihood):
        """
        Initializes the model

        :param train_x: the x-data points
        :param train_y: the y-data points
        :param likelihood: The Gaussian likelihood that defines the observational distribution.
                           Since we're using exact inference, the likelihood must be Gaussian.
        """
        super(GPRegressionModelWithGaussianNoise, self).__init__(train_x, train_y, likelihood)
        self.mean_module = gpytorch.means.ConstantMean()
        self.covar_module = gpytorch.kernels.ScaleKernel(gpytorch.kernels.RBFKernel())

    def forward(self, x) -> gpytorch.distributions.MultivariateNormal:
        """
        Compute the prior latent distribution on a given input using the mean and covariance functions

        :param x: the input
        :return: the prior
        """
        mean_x = self.mean_module(x)
        covar_x = self.covar_module(x)
        return gpytorch.distributions.MultivariateNormal(mean_x, covar_x)
