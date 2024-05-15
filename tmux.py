import numpy as np
from numpy import inf
import math
import matplotlib.pyplot as plt
import scipy.special as sp


class time_multiplexing:
    def __init__(self, mux_dict) -> None:

        # Initial calculations (outside update_plot for efficiency)
        self.num_mode_array = np.arange(1, mux_dict["num_roundtrip_array"])
        self.mean_photon_num = mux_dict["mean_photon_num"]
        self.trigger_eff = mux_dict["trigger_eff"]
        self.num_trigger = mux_dict["num_trigger"]  # Simulates infinite detectors
        self.delay_line_trans = mux_dict["delay_line_trans"]
        self.optics_trans = mux_dict["optics_trans"]
        self.m_photon_num = mux_dict["m_photon_num"]

    def binom(self, n, k):
        """Calculates the binomial coefficient."""
        return sp.factorial(n) / (sp.factorial(k) * sp.factorial(n - k))

    def downConversionProb(self, k):
        """Calculates the probability of generating k-photon pairs with mean photon number mu."""
        return (self.mean_photon_num**k) / (1 + self.mean_photon_num) ** (k + 1)

    def triggerDetProb(self, k, d):
        """Calculates the trigger-photon detection probability for k-photon pairs."""
        endsum = k[-1]
        kMatrix = np.tril(np.tile(k.reshape(endsum, 1), (1, endsum)))
        lMatrix = np.tril(np.tile(k.reshape(1, endsum), (endsum, 1)))
        binomTriangle = np.tril(self.binom(kMatrix, lMatrix))
        prob = (
            (self.trigger_eff**lMatrix)
            * (1 - self.trigger_eff) ** (kMatrix - lMatrix)
            * binomTriangle
            * (1 / d) ** (lMatrix - 1)
        )
        return np.sum(prob, axis=1)

    def MPhotonEmitProb(self, M, N, k):
        """Calculates the M-photon emission probability conditioned by k-photon pairs."""
        jGrid, kGrid = np.meshgrid(np.arange(1, N + 1), np.arange(1, k + 1))
        return (
            (self.optics_trans * self.delay_line_trans ** (N - jGrid - 1)) ** M
            * (1 - self.optics_trans * self.delay_line_trans ** (N - jGrid - 1))
            ** (kGrid - M)
            * self.binom(kGrid, M)
        )

    def heraldPhotonPairProb(self, k, d):
        """Calculates the heralded photon pair probability."""
        kPhotonPair = np.arange(1, k + 1)
        prob_k_photon_k_click = self.downConversionProb(kPhotonPair) * (
            self.triggerDetProb(kPhotonPair, d)
        )
        return prob_k_photon_k_click

    def multiplexHeraldProb(self, d, N, endsum=100):
        """Calculates the multiplexed heralding probability."""
        j = np.arange(1, N + 1)
        heraldProb = np.sum(self.heraldPhotonPairProb(endsum, d))
        return 1 - (1 - heraldProb) ** (N - j)

    def multiplexMPhotonProb(self, d, N, M, endsum=100):
        """Calculates the probability of producing an M-photon state after time multiplexing."""
        j = np.arange(1, N + 1)
        noTriggerDetect = (1 - np.sum(self.heraldPhotonPairProb(endsum, d))) ** (N - j)
        detectTrigger = np.einsum(
            "i, ij",
            self.heraldPhotonPairProb(endsum, d),
            self.MPhotonEmitProb(M, N, endsum),
        )
        return np.sum(noTriggerDetect * detectTrigger)

    # def multiplexMPhotonProb(self, d, N, M, endsum=100):
    #     j = np.arange(1, N + 1)
    #     P_h = self.multiplexHeraldProb(d, N, M)
    #     p_mux = (1 - P_h) ** (N - j) * P_h*

    def calculate_single_photon_prob_array(self):
        return [
            self.multiplexMPhotonProb(
                self.num_trigger,
                n,
                self.m_photon_num,
            )
            for n in self.num_mode_array
        ]


if __name__ == "__main__":

    mux_dict = {
        "num_roundtrip_array": 100,
        "mean_photon_num": 0.18,
        "num_trigger": 10,
        "trigger_eff": 0.53,
        "delay_line_trans": 0.988,
        "optics_trans": 0.83,
        "m_photon_num": 1,
    }

    tmux = time_multiplexing(mux_dict)
    fig, ax = plt.subplots()
    ax.plot(tmux.num_roundtrip_array, tmux.calculate_single_photon_prob_array())
    ax.set_ylabel("M-photon probability")
    ax.set_xlabel("Number of round trips")
    ax.set_title(
        f"M-Photon time multiplexed source, number of heralds = {tmux.num_trigger}"
    )
    ax.grid(True)
    plt.show()
