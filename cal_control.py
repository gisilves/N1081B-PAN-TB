import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QLCDNumber, QTabWidget, QLineEdit
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap
from N1081B_sdk import N1081B

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("N1081B Control for PAN TB")
        self.resize(400, 300)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        
        # Create a horizontal layout for the logo
        self.logo_layout = QHBoxLayout()
        # Add the logo to the layout (logo.png should be in the same directory as this script)
        self.logo = QLabel()
        self.logo.setPixmap(QPixmap("logo.png"))
        # Center the logo
        self.logo.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.logo)

        # Create a QTabWidget to hold the buttons and another tab
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        # Create a tab for the buttons
        self.tab = QWidget()
        self.tab_widget.addTab(self.tab, "Controls")

        # Create a horizontal layout for the buttons
        self.button_layout = QVBoxLayout()
        self.button_layout.setSpacing(5)
        self.tab.setLayout(self.button_layout)

        # Define a dictionary to hold button styles (rounded corners, lightgray background)
        self.button_styles = {
            "font-size": "15px"
        }

        # Create buttons and apply styles
        self.buttons = [
            ("ENABLE CAL", self.enable_calibration),
            ("DISABLE CAL", self.disable_calibration),
            ("ENABLE FAKE SPILL", self.enable_fake_spill),
            ("DISABLE FAKE SPILL", self.disable_fake_spill),
            ("SET HADRON TRIGGER", self.set_hadron_trigger),
            ("SET ELECTRON TRIGGER", self.set_eletron_trigger),
            ("ENABLE MASTER TRIGGER", self.enable_master_trigger),
            ("DISABLE MASTER TRIGGER", self.disable_master_trigger),
            ("RESET TRIGGERS", self.reset_trigger_counter),
            ("RESET SPILLS", self.reset_spill_counter),
        ]

        # Loop over the buttons and add them to the layout (except the last two)
        for button_text, button_action in self.buttons[:-2]:
            button = QPushButton(button_text)
            button.clicked.connect(button_action)
            # Apply styles from the dictionary
            button.setStyleSheet("; ".join(f"{key}: {value}" for key, value in self.button_styles.items()))
            self.button_layout.addWidget(button)

        # Add the second tab for the settings
        self.tab2 = QWidget()
        self.tab_widget.addTab(self.tab2, "Settings")

        # Add a layout for the settings tab
        self.settings_layout = QVBoxLayout()
        self.tab2.setLayout(self.settings_layout)

        self.scint_threshold_label = QLabel("Scintillator Threshold")
        self.settings_layout.addWidget(self.scint_threshold_label)

        self.scint_threshold_layout = QHBoxLayout()
        self.scint_threshold = QLineEdit()
        self.scint_threshold_layout.addWidget(self.scint_threshold)
        self.set_threshold_button = QPushButton("Set Scintillator Threshold")
        self.set_threshold_button.clicked.connect(self.set_scint_threshold)
        self.scint_threshold_layout.addWidget(self.set_threshold_button)
        self.settings_layout.addLayout(self.scint_threshold_layout)

        self.cerenkov_threshold_label = QLabel("Cerenkov Threshold")
        self.settings_layout.addWidget(self.cerenkov_threshold_label)

        self.cerenkov_threshold_layout = QHBoxLayout()
        self.cerenkov_threshold = QLineEdit()
        self.cerenkov_threshold_layout.addWidget(self.cerenkov_threshold)
        self.set_threshold_button = QPushButton("Set Cerenkov Threshold")
        self.set_threshold_button.clicked.connect(self.set_cerenkov_threshold)
        self.cerenkov_threshold_layout.addWidget(self.set_threshold_button)
        self.settings_layout.addLayout(self.cerenkov_threshold_layout)

        # Create a layout for each status indicator
        self.cal_layout = QHBoxLayout()
        self.fake_spill_layout = QHBoxLayout()
        self.hadron_trigger_layout = QHBoxLayout()
        self.master_trigger_layout = QHBoxLayout()
        self.triggers_layout = QHBoxLayout()
        self.spills_layout = QHBoxLayout()
        self.reset_triggers_layout = QHBoxLayout()
        self.reset_spills_layout = QHBoxLayout()

        # Add text label to the left of each LED indicator
        self.cal_label = QLabel("CAL ENABLE")
        self.cal_layout.addWidget(self.cal_label)
        self.cal_status_label = QLabel()
        self.cal_status_label.setFixedSize(20, 15)
        self.cal_layout.addWidget(self.cal_status_label)
        self.layout.addLayout(self.cal_layout)

        self.hadron_trigger_label = QLabel("HADRON TRIGGER")
        self.hadron_trigger_layout.addWidget(self.hadron_trigger_label)
        self.hadron_trigger_status_label = QLabel()
        self.hadron_trigger_status_label.setFixedSize(20, 15)
        self.hadron_trigger_layout.addWidget(self.hadron_trigger_status_label)
        self.layout.addLayout(self.hadron_trigger_layout)

        self.fake_spill_label = QLabel("FAKE SPILL")
        self.fake_spill_layout.addWidget(self.fake_spill_label)
        self.fake_spill_status_label = QLabel()
        self.fake_spill_status_label.setFixedSize(20, 15)
        self.fake_spill_layout.addWidget(self.fake_spill_status_label)
        self.layout.addLayout(self.fake_spill_layout)

        self.master_trigger_label = QLabel("TRIGGER OUTPUT")
        self.master_trigger_layout.addWidget(self.master_trigger_label)
        self.master_trigger_status_label = QLabel()
        self.master_trigger_status_label.setFixedSize(20, 15)
        self.master_trigger_layout.addWidget(self.master_trigger_status_label)
        self.layout.addLayout(self.master_trigger_layout)

        # Add a QLCDNumber to display the number of triggers
        self.triggers_label = QLabel("TRIGGERS")
        self.triggers_layout.addWidget(self.triggers_label)
        self.triggers_lcd = QLCDNumber()
        self.triggers_lcd.setFixedSize(250, 20)
        self.triggers_layout.addWidget(self.triggers_lcd)
        self.layout.addLayout(self.triggers_layout)
        self.triggers_lcd.setDigitCount(12)
        self.triggers_lcd.setSegmentStyle(QLCDNumber.Flat)

        # Add a QLCDNumber to display the number of spills (real or fake)
        self.spills_label = QLabel("SPILLS")
        self.spills_layout.addWidget(self.spills_label)
        self.spills_lcd = QLCDNumber()
        self.spills_lcd.setFixedSize(250, 20)
        self.spills_layout.addWidget(self.spills_lcd)
        self.layout.addLayout(self.spills_layout)
        self.spills_lcd.setDigitCount(12)
        self.spills_lcd.setSegmentStyle(QLCDNumber.Flat)

        # Add the remaing buttons to the main layout
        for button_text, button_action in self.buttons[-2:]:
            button = QPushButton(button_text)
            button.clicked.connect(button_action)
            self.layout.addWidget(button)

        # Initialize the devices
        print("Initializing devices...\n")

        print("Input the IP address of the first device (press Enter to use default):")
        ip1 = input()
        print("Input the IP address of the second device (press Enter to use default):")
        ip2 = input()

        try:
            self.init_devices(ip1, ip2)
        except Exception as e:
            print(f"Error initializing devices: {e}")
            print("Please check the IP addresses and try again.")
            sys.exit(1)

        self.update_status_labels()
        self.update_lcd() 

        # Set a timer to update the lcd every 1s
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_lcd)
        # Update the status labels
        self.timer.timeout.connect(self.update_status_labels)
        self.timer.start(1000)

    def init_devices(self, ip1, ip2):

        # If inserted IP addresses are empty, use default ones
        if ip1 == "":
            ip1 = "128.141.115.60"
        if ip2 == "":
            ip2 = "128.141.115.123"

        # Create N1081B objects for the two devices
        self.N1081B_device1 = N1081B(ip1)
        self.N1081B_device1.connect()

        self.N1081B_device2 = N1081B(ip2)
        self.N1081B_device2.connect()

    def enable_calibration(self):
        # Retrieve SEC_B configuration
        current_config = self.N1081B_device2.get_function_configuration(N1081B.Section.SEC_B)
        # Retrieve the 'enable' value for fake spill from current_config
        target_lemo = 1
        lemo_enables = current_config['data']['lemo_enables']
        fake_spill_en = target_enable_value = next(item['enable'] for item in lemo_enables if item['lemo'] == target_lemo)
        self.N1081B_device2.configure_digital_generator(N1081B.Section.SEC_B,True,fake_spill_en,False,False)
        self.update_status_labels()

    def disable_calibration(self):
        # Retrieve SEC_B configuration
        current_config = self.N1081B_device2.get_function_configuration(N1081B.Section.SEC_B)
        # Retrieve the 'enable' value for fake spill from current_config
        target_lemo = 1
        lemo_enables = current_config['data']['lemo_enables']
        fake_spill_en = target_enable_value = next(item['enable'] for item in lemo_enables if item['lemo'] == target_lemo)
        self.N1081B_device2.configure_digital_generator(N1081B.Section.SEC_B,False,fake_spill_en,False,False)
        self.update_status_labels()

    def enable_fake_spill(self):
        #Retrieve SEC_B configuration
        current_config = self.N1081B_device2.get_function_configuration(N1081B.Section.SEC_B)
        # Retrieve the 'enable' value for fake spill from current_config
        target_lemo = 0
        lemo_enables = current_config['data']['lemo_enables']
        cal_en = target_enable_value = next(item['enable'] for item in lemo_enables if item['lemo'] == target_lemo)
        self.N1081B_device2.configure_digital_generator(N1081B.Section.SEC_B,cal_en,True,False,False)
        self.update_status_labels()

    def disable_fake_spill(self):
        #Retrieve SEC_B configuration
        current_config = self.N1081B_device2.get_function_configuration(N1081B.Section.SEC_B)
        # Retrieve the 'enable' value for fake busy from current_config
        target_lemo = 0
        lemo_enables = current_config['data']['lemo_enables']
        cal_en = target_enable_value = next(item['enable'] for item in lemo_enables if item['lemo'] == target_lemo)
        self.N1081B_device2.configure_digital_generator(N1081B.Section.SEC_B,cal_en,False,False,False)
        self.update_status_labels()

    def enable_master_trigger(self):
        self.N1081B_device2.set_output_channel_configuration(N1081B.Section.SEC_A,0,True,True,1000,False)
        self.update_status_labels()

    def disable_master_trigger(self):
        self.N1081B_device2.set_output_channel_configuration(N1081B.Section.SEC_A,0,False,True,1000,False)
        self.update_status_labels()

    def update_status_labels(self):
        # Retrieve SEC_B configuration of PLU 2
        current_config = self.N1081B_device2.get_function_configuration(N1081B.Section.SEC_B)
        # Retrieve the 'enable' value for cal_enable from current_config
        target_lemo = 0
        lemo_enables = current_config['data']['lemo_enables']
        cal_status = target_enable_value = next(item['enable'] for item in lemo_enables if item['lemo'] == target_lemo)
        # Retrieve the 'enable' value for fake_spill and fake_busy from current_config
        target_lemo = 1
        lemo_enables = current_config['data']['lemo_enables']
        fake_spill_status = target_enable_value = next(item['enable'] for item in lemo_enables if item['lemo'] == target_lemo)

        #Retrieve SEC_A output status on device 2
        output_status = self.N1081B_device2.get_output_channel_configuration(N1081B.Section.SEC_A,0)
        master_trigger_status = output_status['data'].get('status')

        #Retrieve SEC_A input 2 configuration on device 1
        input_status = self.N1081B_device1.get_input_channel_configuration(N1081B.Section.SEC_A,2)
        hadron_trigger_status = input_status['data'].get('invert') == True
        
        # Set the background color of the QLabel based on the status
        self.cal_status_label.setStyleSheet("background-color: green" if cal_status else "background-color: gray")
        self.fake_spill_status_label.setStyleSheet("background-color: green" if fake_spill_status else "background-color: gray")
        self.hadron_trigger_status_label.setStyleSheet("background-color: green" if hadron_trigger_status else "background-color: gray")
        self.master_trigger_status_label.setStyleSheet("background-color: green" if master_trigger_status else "background-color: gray")

    def update_lcd(self):
        #Retrieve SEC_D configuration of PLU 2
        current_config = self.N1081B_device2.get_function_results(N1081B.Section.SEC_D)
        target_lemo = 0
        lemo_counters = current_config['data']['counters']
        scaler = next(item['value'] for item in lemo_counters if item['lemo'] == target_lemo)
        self.triggers_lcd.display(scaler)

        target_lemo = 1
        lemo_counters = current_config['data']['counters']
        scaler = next(item['value'] for item in lemo_counters if item['lemo'] == target_lemo)
        self.spills_lcd.display(scaler)

    def reset_trigger_counter(self):
        self.N1081B_device2.reset_channel(N1081B.Section.SEC_D,0,N1081B.FunctionType.FN_SCALER)
        self.update_lcd()

    def reset_spill_counter(self):
        self.N1081B_device2.reset_channel(N1081B.Section.SEC_D,1,N1081B.FunctionType.FN_SCALER)
        self.update_lcd()    

    def set_hadron_trigger(self):
        # If we want to trigger on hadrons, the Cerenkov will not fire
        # Set input 2 of SEC_A of device 1 to INVERT
        self.N1081B_device1.set_input_channel_configuration(N1081B.Section.SEC_A,channel=2, status=True, invert=True, enable_gate_delay=False, gate = 15, delay = 0)
        self.update_status_labels()

    def set_eletron_trigger(self):
        # If we want to trigger on electrons, the Cerenkov will fire
        # Set input 2 of SEC_A of device 1 to NORMAL
        self.N1081B_device1.set_input_channel_configuration(N1081B.Section.SEC_A,channel=2, status=True, invert=False, enable_gate_delay=False, gate = 15, delay = 0)
        self.update_status_labels()

    def set_cerenkov_threshold(self):
        pass

    def set_scint_threshold(self):
        pass
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
