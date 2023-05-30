from typing import List
from math import exp
from math import pow
from math import sin


class EPTMPRateFunction:
    """
    EPTMP or Exponential-Polynomial-Trigonometric rate function having Multiple Periodicities.
    This class is used for creating a rate function that can exhibit both global trends as well as
    periodic components with individual frequencies and amplitudes.
    (Kuhl and Wilson, 1995)
    """

    def __init__(self, thetas: List[float], gammas: List[float], phis: List[float], omegas: List[float]):
        """
        For more information about the EPTMP rate function and its parameters see Section 2.1.1 in the thesis.
        The length of gammas phis and omegas must be the same.

        :param List[float] thetas: Parameters influencing the overall trend over a long timeframe.
        :param List[float] gammas: Amplitudes.
        :param List[float] phis: Shifts.
        :param List[float] omegas: Frequencies.
        """
        self.thetas = thetas
        self.gammas = gammas
        self.phis = phis
        self.omegas = omegas
    
    def rate_f(self, t: float):
        """
        For more information about the EPTMP rate function and its parameters see Section 2.1.1 in the thesis.
        """
        # The first sum in equation 2.1 in the thesis
        theta_sum = 0
        for i, theta in enumerate(self.thetas):
            theta_sum += theta * pow(t, i)
        
        # The second sum in equation 2.1 in the thesis
        second_sum = 0
        for i, (gamma, phi, omega) in enumerate(zip(self.gammas, self.phis, self.omegas)):
            second_sum += gamma * sin(omega * t + phi)

        # Dont't forget to take the exponential
        return exp(theta_sum + second_sum)