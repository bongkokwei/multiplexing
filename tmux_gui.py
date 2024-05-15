from multiplexing_gui import MultiplexingGUI
from tmux import time_multiplexing
import sys
from PyQt5.QtWidgets import QApplication
from IPython.display import display
from IPython import get_ipython


def run_app():
    # Create a Qt application instance
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    tmux_dict = {
        "num_roundtrip_array": 100,
        "mean_photon_num": 0.18,
        "num_trigger": 4,
        "trigger_eff": 0.53,
        "delay_line_trans": 0.988,
        "optics_trans": 0.83,
        "m_photon_num": 1,
    }

    exclude_param = ["num_roundtrip_array", "num_trigger"]

    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Set Fusion style
    window = MultiplexingGUI(tmux_dict, time_multiplexing, exclude_param)
    window.show()

    # Run the app in the background
    def run():
        app.exec_()

    import threading

    thread = threading.Thread(target=run)
    thread.start()

    display(window)


def tmux_main():
    tmux_dict = {
        "num_roundtrip_array": 100,
        "mean_photon_num": 0.18,
        "num_trigger": 4,
        "trigger_eff": 0.53,
        "delay_line_trans": 0.988,
        "optics_trans": 0.83,
        "m_photon_num": 1,
    }

    exclude_param = ["num_roundtrip_array", "num_trigger"]

    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Set Fusion style
    window = MultiplexingGUI(tmux_dict, time_multiplexing, exclude_param)
    window.show()
    # sys.exit(app.exec_())


if __name__ == "__main__":
    tmux_main()
