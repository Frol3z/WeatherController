from PySide6.QtCore import Qt
from PySide6.QtGui import QDoubleValidator
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
        self.build_wind_ui()

    def build_create_env_ui(self):
        button = QPushButton('Create Environment', self)
        button.clicked.connect(self.controller.create_env_button_action)
        env_layout = QHBoxLayout(self)
        env_layout.addWidget(button, alignment=Qt.AlignCenter)

        self.main_layout.addLayout(env_layout)

    def build_clouds_ui(self):
        clouds_layout = QVBoxLayout(self)

        self.create_section_header('Clouds', clouds_layout)

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
        clouds_layout.addLayout(density_layout)
        clouds_layout.addLayout(storminess_layout)
        clouds_layout.addLayout(aod_layout)

        self.main_layout.addLayout(clouds_layout)

    def build_rain_ui(self):
        rain_layout = QVBoxLayout(self)

        self.create_section_header('Rain', rain_layout)

        # Rain enabled checkbox
        rain_enabled_layout = QHBoxLayout()
        rain_enabled_label = QLabel(self, text='Enable Rain')
        rain_enabled_checkbox = QCheckBox(self)
        rain_enabled_checkbox.stateChanged.connect(self.controller.rain_enabled_action)
        rain_enabled_layout.addWidget(rain_enabled_label)
        rain_enabled_layout.addStretch()
        rain_enabled_layout.addWidget(rain_enabled_checkbox)

        rain_layout.addLayout(rain_enabled_layout)
        self.main_layout.addLayout(rain_layout)

    def build_wind_ui(self):
        wind_layout = QVBoxLayout(self)
        self.create_section_header('Wind', wind_layout)

        # Wind speed slider
        speed_layout = QHBoxLayout()
        speed_label = QLabel(self, text='Wind Speed')
        speed_slider = QSlider(orientation=Qt.Horizontal, minimum=0, maximum=100, value=0)
        speed_slider.setMinimumWidth(100)
        speed_slider.setMaximumWidth(100)
        speed_slider.valueChanged.connect(self.controller.wind_speed_action)
        speed_layout.addWidget(speed_label)
        speed_layout.addStretch()
        speed_layout.addWidget(speed_slider)

        # Wind direction
        direction_layout = QHBoxLayout()
        validator = QDoubleValidator()
        validator.setRange(-99.999, 99.999) # @todo fix this
        validator.setDecimals(3)
        direction_label = QLabel(self, text='Wind Direction')

        # Inputs
        direction_input_layout = QHBoxLayout()

        # X axis
        direction_x_input = QLineEdit(self)
        direction_x_input.setMinimumWidth(50)
        direction_x_input.setMaximumWidth(50)
        direction_x_input.setText('1.000')
        direction_x_input.setValidator(validator)

        # Y axis
        direction_y_input = QLineEdit(self)
        direction_y_input.setMinimumWidth(50)
        direction_y_input.setMaximumWidth(50)
        direction_y_input.setText('0.000')
        direction_y_input.setValidator(validator)

        # Z axis
        direction_z_input = QLineEdit(self)
        direction_z_input.setMinimumWidth(50)
        direction_z_input.setMaximumWidth(50)
        direction_z_input.setText('0.000')
        direction_z_input.setValidator(validator)

        # Connect inputs
        direction_x_input.editingFinished.connect(lambda: self.controller.wind_direction_action(float(direction_x_input.text()), 'X'))
        direction_y_input.editingFinished.connect(lambda: self.controller.wind_direction_action(float(direction_y_input.text()), 'Y'))
        direction_z_input.editingFinished.connect(lambda: self.controller.wind_direction_action(float(direction_z_input.text()), 'Z'))

        # Nest layouts
        direction_input_layout.addWidget(direction_x_input)
        direction_input_layout.addWidget(direction_y_input)
        direction_input_layout.addWidget(direction_z_input)

        direction_layout.addWidget(direction_label)
        direction_layout.addStretch()
        direction_layout.addLayout(direction_input_layout)

        wind_layout.addLayout(speed_layout)
        wind_layout.addLayout(direction_layout)
        self.main_layout.addLayout(wind_layout)

    def create_section_header(self, title, layout):
        # Section separator
        separator = QFrame(self)
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)

        # Section title
        title_label = QLabel(self, text=title, alignment=Qt.AlignCenter)
        # Make it bold
        font = title_label.font()
        font.setBold(True)
        title_label.setFont(font)

        # Attach to layout
        layout.addWidget(separator)
        layout.addWidget(title_label)
