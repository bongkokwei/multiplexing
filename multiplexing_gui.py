import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QSlider,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from tmux import time_multiplexing
from smux import spatial_multiplexing

# TODO: replace exclude_param array to something smarter to tell the code not to scale my value to 100


class MultiplexingGUI(QMainWindow):
    def __init__(self, mux_dict, mux_class, exclude_param):
        super().__init__()

        self.setWindowTitle("Multiplexing Parameters")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)

        self.exclude_param = exclude_param
        self.mux_class = mux_class
        self.mux_dict = mux_dict
        self.sliders = {}
        self.labels = {}  # Store references to the QLabels

        for param, value in self.mux_dict.items():
            # Define parameter HBox to display slider name, slider value and value
            param_layout = QHBoxLayout()

            label = QLabel(param)
            param_layout.addWidget(label)

            if param in self.exclude_param:
                slider = QSlider(Qt.Horizontal)
                slider.setMinimum(1)
                slider.setMaximum(500)
                slider.setValue(value)
            else:
                slider = QSlider(Qt.Horizontal)
                slider.setMinimum(0)
                slider.setMaximum(100)
                slider.setValue(int(value * 100))

            # Connect slider to update plot
            slider.valueChanged.connect(self.update_plot)
            # Add slider to parameter Hbox
            param_layout.addWidget(slider)
            # Add parameter value to HBox
            value_label = QLabel(str(value))
            param_layout.addWidget(value_label)
            # Add param_layout to global parameter display
            layout.addLayout(param_layout)

            # Update store in reference
            self.sliders[param] = slider
            self.labels[param] = value_label  # Store the QLabel

        self.plot_label = QLabel()
        layout.addWidget(self.plot_label)

        self.update_plot()

    def update_plot(self):
        for param, slider in self.sliders.items():
            if param in self.exclude_param:
                self.mux_dict[param] = slider.value()
            else:
                self.mux_dict[param] = slider.value() / 100

            self.labels[param].setText(str(self.mux_dict[param]))

        mux = self.mux_class(self.mux_dict)
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.plot(mux.num_mode_array, mux.calculate_single_photon_prob_array())
        ax.set_ylabel("M-photon probability")
        ax.set_xlabel("Number of modes")
        ax.set_title(f"M-Photon multiplexed source")
        ax.grid(True)

        # Convert matplotlib figure to QImage
        fig.canvas.draw()
        width, height = fig.canvas.get_width_height()
        buffer = fig.canvas.buffer_rgba()
        q_img = QImage(buffer, width, height, QImage.Format_RGBA8888)
        plt.close(fig)

        # Convert QImage to QPixmap and set it as label pixmap
        pixmap = QPixmap.fromImage(q_img)
        self.plot_label.setPixmap(pixmap)
