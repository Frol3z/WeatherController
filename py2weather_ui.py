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

        # Density sliders
        density_layout = QHBoxLayout()
        density_label = QLabel(self, text='Density')
        density_slider = QSlider(orientation=Qt.Horizontal, minimum=0, maximum=100, value=10)
        density_slider.setMinimumWidth(100)
        density_slider.setMaximumWidth(100)
        density_slider.valueChanged.connect(self.controller.clouds_density_action)

        # Density keyframes
        density_add_keyframe_button = QPushButton('AK', self)
        density_delete_keyframe_button = QPushButton('DK', self)
        density_add_keyframe_button.clicked.connect(self.controller.clouds_density_add_keyframe_action)
        density_delete_keyframe_button.clicked.connect(self.controller.clouds_density_delete_keyframe_action)

        # Density layout
        density_layout.addWidget(density_label)
        density_layout.addStretch()
        density_layout.addWidget(density_slider)
        density_layout.addWidget(density_add_keyframe_button)
        density_layout.addWidget(density_delete_keyframe_button)

        # Storminess checkbox
        storminess_layout = QHBoxLayout()
        storminess_label = QLabel(self, text='Storminess')
        storminess_checkbox = QCheckBox(self)
        storminess_checkbox.stateChanged.connect(self.controller.clouds_storminess_action)

        # Storminess keyframes
        storminess_add_keyframe_button = QPushButton('AK', self)
        storminess_delete_keyframe_button = QPushButton('DK', self)
        storminess_add_keyframe_button.clicked.connect(self.controller.clouds_storminess_add_keyframe_action)
        storminess_delete_keyframe_button.clicked.connect(self.controller.clouds_storminess_delete_keyframe_action)

        # Storminess layout
        storminess_layout.addWidget(storminess_label)
        storminess_layout.addStretch()
        storminess_layout.addWidget(storminess_checkbox)
        storminess_layout.addWidget(storminess_add_keyframe_button)
        storminess_layout.addWidget(storminess_delete_keyframe_button)

        # Amount of Details sliders
        aod_layout = QHBoxLayout()
        aod_label = QLabel(self, text='Amount of Details')
        aod_slider = QSlider(orientation=Qt.Horizontal, minimum=0, maximum=100, value=60)
        aod_slider.setMinimumWidth(100)
        aod_slider.setMaximumWidth(100)
        aod_slider.valueChanged.connect(self.controller.clouds_aod_action)

        # Amount of Details keyframes
        aod_add_keyframe_button = QPushButton('AK', self)
        aod_delete_keyframe_button = QPushButton('DK', self)
        aod_add_keyframe_button.clicked.connect(self.controller.clouds_aod_add_keyframe_action)
        aod_delete_keyframe_button.clicked.connect(self.controller.clouds_aod_delete_keyframe_action)

        # Amount of Details layout
        aod_layout.addWidget(aod_label)
        aod_layout.addStretch()
        aod_layout.addWidget(aod_slider)
        aod_layout.addWidget(aod_add_keyframe_button)
        aod_layout.addWidget(aod_delete_keyframe_button)

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
        rain_enabled_slider = QSlider(orientation=Qt.Horizontal, minimum=0, maximum=1000, value=0)
        rain_enabled_slider.setMinimumWidth(100)
        rain_enabled_slider.setMaximumWidth(100)
        rain_enabled_slider.valueChanged.connect(self.controller.rain_enabled_action)

        # Rain enabled keyframes
        rain_enabled_add_keyframe_button = QPushButton('AK', self)
        rain_enabled_delete_keyframe_button = QPushButton('DK', self)
        rain_enabled_add_keyframe_button.clicked.connect(self.controller.rain_enabled_add_keyframe_action)
        rain_enabled_delete_keyframe_button.clicked.connect(self.controller.rain_enabled_delete_keyframe_action)

        # Rain enabled layout
        rain_enabled_layout.addWidget(rain_enabled_label)
        rain_enabled_layout.addStretch()
        rain_enabled_layout.addWidget(rain_enabled_slider)
        rain_enabled_layout.addWidget(rain_enabled_add_keyframe_button)
        rain_enabled_layout.addWidget(rain_enabled_delete_keyframe_button)

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

        # Wind speed keyframes
        speed_add_keyframe_button = QPushButton(text='AK')
        speed_add_keyframe_button.clicked.connect(self.controller.wind_speed_add_keyframe_action)
        speed_delete_keyframe_button = QPushButton(text='DK')
        speed_delete_keyframe_button.clicked.connect(self.controller.wind_speed_delete_keyframe_action)

        # Wind speed layout
        speed_layout.addWidget(speed_label)
        speed_layout.addStretch()
        speed_layout.addWidget(speed_slider)
        speed_layout.addWidget(speed_add_keyframe_button)
        speed_layout.addWidget(speed_delete_keyframe_button)

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

        # Wind direction keyframes
        direction_add_keyframe_button = QPushButton(text='AK')
        direction_add_keyframe_button.clicked.connect(self.controller.wind_direction_add_keyframe_action)
        direction_delete_keyframe_button = QPushButton(text='DK')
        direction_delete_keyframe_button.clicked.connect(self.controller.wind_direction_delete_keyframe_action)

        # Nest layouts
        direction_input_layout.addWidget(direction_x_input)
        direction_input_layout.addWidget(direction_y_input)
        direction_input_layout.addWidget(direction_z_input)

        direction_layout.addWidget(direction_label)
        direction_layout.addStretch()
        direction_layout.addLayout(direction_input_layout)
        direction_layout.addWidget(direction_add_keyframe_button)
        direction_layout.addWidget(direction_delete_keyframe_button)

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
