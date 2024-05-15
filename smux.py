import numpy as np
import math
import matplotlib.pyplot as plt
import scipy.special as sp

"""
Glossary:
eta_idler the global collection efficiency on the idler arm accounting for all these effects,
eta_signal is the overall transmission on the signal arm accounting for losses in the sources and filters.
"""


class spatial_multiplexing:
    def __init__(self, mux_dict) -> None:
        self.update_param(mux_dict)
        self.network_type = "gmzi"

        # lump recurring expressions to shorten equations
        self.sq_squared = np.abs(self.squeezing_param) ** 2
        self.idler_loss = 1 - self.eta_idler
        self.signal_loss = 1 - self.eta_signal

    def prob_trig_NRD(self):
        """
        Tracing out the signal mode and calculating the probability to get only one photon gives
        Equation 8
        """

        p_trig = ((1 - self.sq_squared) * self.sq_squared * self.eta_idler) / (
            (1 - self.idler_loss * self.sq_squared) ** 2
        )

        return p_trig

    def prob_single_photon_NRD(self):
        """
        The probability the heralded state contains one photon
        Equation 10
        """
        # Prob(1-photon|herald)
        p1_herald = (
            (1 - self.idler_loss * self.sq_squared) ** 2
            * self.eta_signal
            * (
                (1 + self.idler_loss * self.signal_loss * self.sq_squared)
                / (1 - self.idler_loss * self.signal_loss * self.sq_squared) ** 3
            )
        )

        return p1_herald

    def prob_multi_photon_NRD(self):
        """
        The probability for the heralded state to contain multi-photon contamination is given by
        Equation 11
        """
        p1_herald = self.prob_single_photon_NRD()
        # P(n-photon|herald)
        pn_herald = (
            self.eta_signal
            * (
                (1 - self.signal_loss * (self.sq_squared * self.idler_loss) ** 2)
                / (1 - self.sq_squared * self.signal_loss * self.idler_loss) ** 2
            )
            - p1_herald
        )

        return pn_herald

    def prob_mux_trig(self, num_sources):
        """
        The probability per clock-cycle that at least one HSPS in an array of N HSPSs triggers is given by
        Equation 12
        """
        return 1 - (1 - self.prob_trig_NRD()) ** num_sources

    def prob_mux_one(self, num_sources):
        """
        the probability per clock-cycle that at least one source emits a triggered single-photon
        Equation 13
        """

        return self.prob_single_photon_NRD() * (
            1 - (1 - self.prob_trig_NRD()) ** num_sources
        )

    def prob_mux_single(self, num_sources):
        """
        The probability per clock-cycle for a multiplexed source to emit a triggered singlephoton
        Equation 15
        """

        p_mux_single = (
            self.prob_mux_one(num_sources)
            * self.prob_mux_trig(num_sources)
            * self.eta_network()
        )
        return p_mux_single

    def eta_network(self):
        if self.network_type == "log_tree":
            return (
                self.eta_switch ** (np.log(self.num_sources) / np.log(2))
                * self.eta_delay
            )

        elif self.network_type == "gmzi":
            return self.eta_delay * self.eta_switch * self.eta_splitter**2
        else:
            return 1.0

    def calculate_single_photon_prob_array(self):
        return [self.prob_mux_single(n) for n in self.num_mode_array]

    # def param_sweep(self, param_name, min, max, step_size):

    #     for param in np.arange(min, max, step_size):

    def update_param(self, param):
        self.num_sources = param["num_sources"]
        self.num_mode_array = np.arange(1, self.num_sources)  # needs to be this
        self.eta_idler = param["eta_idler"]
        self.eta_signal = param["eta_signal"]
        self.squeezing_param = param["squeezing_param"]
        self.eta_delay = param["eta_delay"]
        self.eta_switch = param["eta_switch"]
        self.eta_splitter = param["eta_splitter"]  # NxN MMI


if __name__ == "__main__":

    smux_dict = {
        "num_sources": 100,  #  number of sources
        "eta_idler": 1.0,  #  efficiency of the idler
        "eta_signal": 1.0,  # efficiency of the signal
        "squeezing_param": 0.8,  #  squeezing parameter
        "eta_delay": 0.8,  # efficiency of the delay
        "eta_switch": 0.8,  #  efficiency of the switch
        "eta_splitter": 0.8,  # efficiency of the splitter
    }
    smux = spatial_multiplexing(smux_dict)

    fig1, ax1 = plt.subplots()
    ax1.plot(smux.num_mode_array, smux.calculate_single_photon_prob_array())
    ax1.set_ylabel("M-photon probability")
    ax1.set_xlabel("Number of modes")
    ax1.set_title(f"M-Photon time multiplexed source")
    ax1.grid(True)

    fig2, ax2 = plt.subplots()
    eta_idler_array = np.arange(0.9, 1.0, 0.01)
    ax2.grid(True)
    plt.show()
