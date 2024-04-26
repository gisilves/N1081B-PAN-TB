import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QLCDNumber
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap
from N1081B_sdk import N1081B

def enable_calibration():
    # Retrieve SEC_B configuration
    current_config = N1081B_device2.get_function_configuration(N1081B.Section.SEC_B)
    # Retrieve the 'enable' value for fake spill from current_config
    target_lemo = 1
    lemo_enables = current_config['data']['lemo_enables']
    fake_spill_en = target_enable_value = next(item['enable'] for item in lemo_enables if item['lemo'] == target_lemo)
    N1081B_device2.configure_digital_generator(N1081B.Section.SEC_B,True,fake_spill_en,False,False)
    update_status_labels()

def disable_calibration():
    # Retrieve SEC_B configuration
    current_config = N1081B_device2.get_function_configuration(N1081B.Section.SEC_B)
    # Retrieve the 'enable' value for fake spill from current_config
    target_lemo = 1
    lemo_enables = current_config['data']['lemo_enables']
    fake_spill_en = target_enable_value = next(item['enable'] for item in lemo_enables if item['lemo'] == target_lemo)
    N1081B_device2.configure_digital_generator(N1081B.Section.SEC_B,False,fake_spill_en,False,False)
    update_status_labels()

def enable_fake_spill():
    #Retrieve SEC_B configuration
    current_config = N1081B_device2.get_function_configuration(N1081B.Section.SEC_B)
    # Retrieve the 'enable' value for fake spill from current_config
    target_lemo = 0
    lemo_enables = current_config['data']['lemo_enables']
    cal_en = target_enable_value = next(item['enable'] for item in lemo_enables if item['lemo'] == target_lemo)
    N1081B_device2.configure_digital_generator(N1081B.Section.SEC_B,cal_en,True,False,False)
    update_status_labels()

def disable_fake_spill():
    #Retrieve SEC_B configuration
    current_config = N1081B_device2.get_function_configuration(N1081B.Section.SEC_B)
    # Retrieve the 'enable' value for fake busy from current_config
    target_lemo = 0
    lemo_enables = current_config['data']['lemo_enables']
    cal_en = target_enable_value = next(item['enable'] for item in lemo_enables if item['lemo'] == target_lemo)
    N1081B_device2.configure_digital_generator(N1081B.Section.SEC_B,cal_en,False,False,False)
    update_status_labels()

def enable_master_trigger():
    N1081B_device2.set_output_channel_configuration(N1081B.Section.SEC_A,0,True,True,1000,False)
    update_status_labels()

def disable_master_trigger():
    N1081B_device2.set_output_channel_configuration(N1081B.Section.SEC_A,0,False,True,1000,False)
    update_status_labels()

def update_status_labels():
    # Retrieve SEC_B configuration of PLU 2
    current_config = N1081B_device2.get_function_configuration(N1081B.Section.SEC_B)
    # Retrieve the 'enable' value for cal_enable from current_config
    target_lemo = 0
    lemo_enables = current_config['data']['lemo_enables']
    cal_status = target_enable_value = next(item['enable'] for item in lemo_enables if item['lemo'] == target_lemo)
    # Retrieve the 'enable' value for fake_spill and fake_busy from current_config
    target_lemo = 1
    lemo_enables = current_config['data']['lemo_enables']
    fake_spill_status = target_enable_value = next(item['enable'] for item in lemo_enables if item['lemo'] == target_lemo)

    #Retrieve SEC_A output status on device 2
    output_status = N1081B_device2.get_output_channel_configuration(N1081B.Section.SEC_A,0)
    master_trigger_status = output_status['data'].get('status')

    #Retrieve SEC_A input 2 configuration on device 1
    input_status = N1081B_device1.get_input_channel_configuration(N1081B.Section.SEC_A,2)
    hadron_trigger_status = input_status['data'].get('invert') == True
    
    # Set the background color of the QLabel based on the status
    cal_status_label.setStyleSheet("background-color: green" if cal_status else "background-color: gray")
    fake_spill_status_label.setStyleSheet("background-color: green" if fake_spill_status else "background-color: gray")
    hadron_trigger_status_label.setStyleSheet("background-color: green" if hadron_trigger_status else "background-color: gray")
    master_trigger_status_label.setStyleSheet("background-color: green" if master_trigger_status else "background-color: gray")

def update_lcd():
    #Retrieve SEC_D configuration of PLU 2
    current_config = N1081B_device2.get_function_results(N1081B.Section.SEC_D)
    target_lemo = 0
    lemo_counters = current_config['data']['counters']
    scaler = next(item['value'] for item in lemo_counters if item['lemo'] == target_lemo)
    triggers_lcd.display(scaler)

    target_lemo = 1
    lemo_counters = current_config['data']['counters']
    scaler = next(item['value'] for item in lemo_counters if item['lemo'] == target_lemo)
    spills_lcd.display(scaler)

def reset_trigger_counter():
    N1081B_device2.reset_channel(N1081B.Section.SEC_D,0,N1081B.FunctionType.FN_SCALER)
    update_lcd()

def reset_spill_counter():
    N1081B_device2.reset_channel(N1081B.Section.SEC_D,1,N1081B.FunctionType.FN_SCALER)
    update_lcd()    

def set_hadron_trigger():
    # If we want to trigger on hadrons, the Cerenkov will not fire
    # Set input 2 of SEC_A of device 1 to INVERT
    N1081B_device1.set_input_channel_configuration(N1081B.Section.SEC_A,channel=2, status=True, invert=True, enable_gate_delay=False, gate = 15, delay = 0)
    update_status_labels()

def set_eletron_trigger():
    # If we want to trigger on electrons, the Cerenkov will fire
    # Set input 2 of SEC_A of device 1 to NORMAL
    N1081B_device1.set_input_channel_configuration(N1081B.Section.SEC_A,channel=2, status=True, invert=False, enable_gate_delay=False, gate = 15, delay = 0)
    update_status_labels()

N1081B_device1 = N1081B("128.141.115.60")
N1081B_device1.connect()

N1081B_device2 = N1081B("128.141.115.123")
N1081B_device2.connect()

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("N1081B Control for PAN TB")
window.resize(400, 300)

layout = QVBoxLayout()
layout.setSpacing(5)

# Create a horizontal layout for the logo
logo_layout = QHBoxLayout()
# Add the logo to the layout (logo.png should be in the same directory as this script)
logo = QLabel()
logo.setPixmap(QPixmap("logo.png"))
# Center the logo
logo.setAlignment(logo.alignment() | Qt.AlignCenter)
layout.addWidget(logo)

# Define a dictionary to hold button styles (rounded corners, lightgray background)
button_styles = {
    "font-size": "15px"
}

# Create buttons and apply styles
buttons = [
    ("ENABLE CAL", enable_calibration),
    ("DISABLE CAL", disable_calibration),
    ("ENABLE FAKE SPILL", enable_fake_spill),
    ("DISABLE FAKE SPILL", disable_fake_spill),
    ("SET HADRON TRIGGER", set_hadron_trigger),
    ("SET ELECTRON TRIGGER", set_eletron_trigger),
    ("ENABLE MASTER TRIGGER", enable_master_trigger),
    ("DISABLE MASTER TRIGGER", disable_master_trigger),
    ("RESET TRIGGERS", reset_trigger_counter),
    ("RESET SPILLS", reset_spill_counter),
]

for button_text, button_action in buttons:
    button = QPushButton(button_text)
    button.clicked.connect(button_action)
    # Apply styles from the dictionary
    button.setStyleSheet("; ".join(f"{key}: {value}" for key, value in button_styles.items()))
    layout.addWidget(button)

layout.setSpacing(10)

# Create a horizontal layout for each status indicator
cal_layout = QHBoxLayout()
fake_spill_layout = QHBoxLayout()
hadron_trigger_layout = QHBoxLayout()
master_trigger_layout = QHBoxLayout()
triggers_layout = QHBoxLayout()
spills_layout = QHBoxLayout()
reset_triggers_layout = QHBoxLayout()
reset_spills_layout = QHBoxLayout()

# Add text label to the left of each LED indicator
cal_label = QLabel("CAL ENABLE")
cal_layout.addWidget(cal_label)
cal_status_label = QLabel()
cal_status_label.setFixedSize(20, 15)
cal_layout.addWidget(cal_status_label)
layout.addLayout(cal_layout)

hadron_trigger_label = QLabel("HADRON TRIGGER")
hadron_trigger_layout.addWidget(hadron_trigger_label)
hadron_trigger_status_label = QLabel()
hadron_trigger_status_label.setFixedSize(20, 15)
hadron_trigger_layout.addWidget(hadron_trigger_status_label)
layout.addLayout(hadron_trigger_layout)

fake_spill_label = QLabel("FAKE SPILL")
fake_spill_layout.addWidget(fake_spill_label)
fake_spill_status_label = QLabel()
fake_spill_status_label.setFixedSize(20, 15)
fake_spill_layout.addWidget(fake_spill_status_label)
layout.addLayout(fake_spill_layout)

master_trigger_label = QLabel("TRIGGER OUTPUT")
master_trigger_layout.addWidget(master_trigger_label)
master_trigger_status_label = QLabel()
master_trigger_status_label.setFixedSize(20, 15)
master_trigger_layout.addWidget(master_trigger_status_label)
layout.addLayout(master_trigger_layout)

# Add a QLCDNumber to display the number of triggers
triggers_label = QLabel("TRIGGERS")
triggers_layout.addWidget(triggers_label)
triggers_lcd = QLCDNumber()
triggers_lcd.setFixedSize(250, 20)
triggers_layout.addWidget(triggers_lcd)
layout.addLayout(triggers_layout)

triggers_lcd.setDigitCount(12)
triggers_lcd.setSegmentStyle(QLCDNumber.Flat)

# Add a QLCDNumber to display the number of spills (real or fake)
spills_label = QLabel("SPILLS")
spills_layout.addWidget(spills_label)
spills_lcd = QLCDNumber()
spills_lcd.setFixedSize(250, 20)
spills_layout.addWidget(spills_lcd)
layout.addLayout(spills_layout)

spills_lcd.setDigitCount(12)
spills_lcd.setSegmentStyle(QLCDNumber.Flat)

# Add a RESET TRIGGER button
reset_trigger_button = QPushButton("RESET TRIGGERS")
reset_trigger_button.clicked.connect(reset_trigger_counter)
layout.addWidget(reset_trigger_button)

# Add a RESET SPILL button
reset_spill_button = QPushButton("RESET SPILLS")
reset_spill_button.clicked.connect(reset_spill_counter)
layout.addWidget(reset_spill_button)

update_status_labels()
update_lcd() 

# Set a timer to update the lcd every 1s
timer = QTimer()
timer.timeout.connect(update_lcd)
# Update the status labels
timer.timeout.connect(update_status_labels)
timer.start(1000)

window.setLayout(layout)
window.show()

sys.exit(app.exec_())
