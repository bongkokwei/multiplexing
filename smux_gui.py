from multiplexing_gui import MultiplexingGUI
from smux import spatial_multiplexing
import sys
from PyQt5.QtWidgets import QApplication
from IPython.display import display
from IPython import get_ipython


def run_app():
    # Create a Qt application instance
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    smux_dict = {
        "num_sources": 100,  #  number of sources
        "eta_idler": 0.98,  #  efficiency of the idler
        "eta_signal": 0.85,  # efficiency of the signal
        "squeezing_param": 0.88,  #  squeezing parameter
        "eta_delay": 0.83,  # efficiency of the delay
        "eta_switch": 0.72,  #  efficiency of the switch
        "eta_splitter": 0.68,  # efficiency of the splitter
    }

    exclude_smux_param = ["num_sources"]

    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Set Fusion style
    window = MultiplexingGUI(smux_dict, spatial_multiplexing, exclude_smux_param)
    window.show()

    display(window)
    # Run the Qt application event loop
    app.exec_()


def smux_main():

    smux_dict = {
        "num_sources": 100,  #  number of sources
        "eta_idler": 0.98,  #  efficiency of the idler
        "eta_signal": 0.85,  # efficiency of the signal
        "squeezing_param": 0.88,  #  squeezing parameter
        "eta_delay": 0.83,  # efficiency of the delay
        "eta_switch": 0.72,  #  efficiency of the switch
        "eta_splitter": 0.68,  # efficiency of the splitter
    }

    exclude_smux_param = ["num_sources"]

    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Set Fusion style
    window = MultiplexingGUI(smux_dict, spatial_multiplexing, exclude_smux_param)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_app()
