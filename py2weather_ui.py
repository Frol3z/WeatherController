from PySide6.QtCore import Qt
from PySide6.QtWidgets import *

class WeatherUI(QWidget):
    def __init__(self, controller, *args, **kwargs):
        super(WeatherUI, self).__init__(*args, **kwargs)
        self.controller = controller
        self.setParent(controller.maya_main_window)
        self.setWindowFlags(Qt.Window)
        self.setObjectName('WeatherUI_uniqueId')
        self.setWindowTitle('Weather Controller')
        self.setGeometry(50, 50, 350, 150)
        self.build_ui()

    def build_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.build_create_env_ui()
        self.build_clouds_ui()
        self.build_rain_ui()

    def build_create_env_ui(self):
        button = QPushButton('Create Environment', self)
        button.clicked.connect(self.controller.create_env_button_action)
        env_layout = QHBoxLayout(self)
        env_layout.addWidget(button, alignment=Qt.AlignCenter)

        self.main_layout.addLayout(env_layout)

    def build_clouds_ui(self):
        clouds_layout = QVBoxLayout(self)

        # Section separator
        separator = QFrame(self)
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)

        # Section title
        title_label = QLabel(self, text='Clouds', alignment=Qt.AlignCenter)
        # Make it bold
        font = title_label.font()
        font.setBold(True)
        title_label.setFont(font)

        # Density
        density_layout = QHBoxLayout()
        density_label = QLabel(self, text='Density')
        density_slider = QSlider(orientation=Qt.Horizontal, minimum=0, maximum=100, value=10)
        density_slider.setMinimumWidth(100)
        density_slider.setMaximumWidth(100)
        density_slider.valueChanged.connect(self.controller.clouds_density_action)
        density_layout.addWidget(density_label)
        density_layout.addStretch()
        density_layout.addWidget(density_slider)

        # Storminess
        storminess_layout = QHBoxLayout()
        storminess_label = QLabel(self, text='Storminess')
        storminess_checkbox = QCheckBox(self)
        storminess_checkbox.stateChanged.connect(self.controller.clouds_storminess_action)
        storminess_layout.addWidget(storminess_label)
        storminess_layout.addStretch()
        storminess_layout.addWidget(storminess_checkbox)

        # Amount of Details
        aod_layout = QHBoxLayout()
        aod_label = QLabel(self, text='Amount of Details')
        aod_slider = QSlider(orientation=Qt.Horizontal, minimum=0, maximum=100, value=60)
        aod_slider.setMinimumWidth(100)
        aod_slider.setMaximumWidth(100)
        aod_slider.valueChanged.connect(self.controller.clouds_aod_action)
        aod_layout.addWidget(aod_label)
        aod_layout.addStretch()
        aod_layout.addWidget(aod_slider)

        # Add sub-HBox in the main cloud VBox
        clouds_layout.addWidget(separator)
        clouds_layout.addWidget(title_label)
        clouds_layout.addLayout(density_layout)
        clouds_layout.addLayout(storminess_layout)
        clouds_layout.addLayout(aod_layout)

        self.main_layout.addLayout(clouds_layout)

    def build_rain_ui(self):
        rain_layout = QVBoxLayout(self)

        # Section separator
        separator = QFrame(self)
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)

        # Section title
        title_label = QLabel(self, text='Rain', alignment=Qt.AlignCenter)
        # Make it bold
        font = title_label.font()
        font.setBold(True)
        title_label.setFont(font)

        # @todo Rain UI

        rain_layout.addWidget(title_label)
        rain_layout.addWidget(separator)
        self.main_layout.addLayout(rain_layout)
