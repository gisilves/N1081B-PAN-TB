import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QLCDNumber
from PyQt5.QtCore import QTimer
from N1081B_sdk import N1081B

def enable_calibration():
    N1081B_device2.configure_digital_generator(N1081B.Section.SEC_B,True,True,False,False)
    update_status_labels()

def disable_calibration():
    N1081B_device2.configure_digital_generator(N1081B.Section.SEC_B,False,False,False,False)
    update_status_labels()

def enable_fake_spill():
    #Retrieve SEC_B configuration
    current_config = N1081B_device2.get_function_configuration(N1081B.Section.SEC_B)
    # Retrieve the 'enable' value for fake spill from current_config
    target_lemo = 1
    lemo_enables = current_config['data']['lemo_enables']
    cal_en = target_enable_value = next(item['enable'] for item in lemo_enables if item['lemo'] == target_lemo)
    N1081B_device2.configure_digital_generator(N1081B.Section.SEC_B,cal_en,True,False,False)
    update_status_labels()

def disable_fake_spill():
    #Retrieve SEC_B configuration
    current_config = N1081B_device2.get_function_configuration(N1081B.Section.SEC_B)
    # Retrieve the 'enable' value for fake busy from current_config
    target_lemo = 1
    lemo_enables = current_config['data']['lemo_enables']
    cal_en = target_enable_value = next(item['enable'] for item in lemo_enables if item['lemo'] == target_lemo)
    N1081B_device1.configure_digital_generator(N1081B.Section.SEC_A,cal_en,False,False,False)
    update_status_labels()

def enable_master_trigger():
    N1081B_device1.set_output_channel_configuration(N1081B.Section.SEC_C,0,True,True,1000,False)
    N1081B_device1.set_output_channel_configuration(N1081B.Section.SEC_C,1,True,False,0,False)
    #N1081B_device2.configure_or_veto(N1081B.Section.SEC_C,True,True,False,False,False,False,0) 
    update_status_labels()

def disable_master_trigger():
    N1081B_device1.set_output_channel_configuration(N1081B.Section.SEC_C,0,False,True,1000,False)
    N1081B_device1.set_output_channel_configuration(N1081B.Section.SEC_C,1,False,False,0,False)
    #N1081B_device2.configure_or_veto(N1081B.Section.SEC_C,False,False,False,False,False,False,0)
    update_status_labels()

def update_status_labels():
    #Retrieve SEC_A configuration
    current_config = N1081B_device1.get_function_configuration(N1081B.Section.SEC_A)
    # Retrieve the 'enable' value for cal_enable from current_config
    target_lemo = 0
    lemo_enables = current_config['data']['lemo_enables']
    cal_status = target_enable_value = next(item['enable'] for item in lemo_enables if item['lemo'] == target_lemo)

    #Retrieve SEC_D configuration
    current_config = N1081B_device1.get_function_configuration(N1081B.Section.SEC_D)
    # Retrieve the 'enable' value for fake_spill and fake_busy from current_config
    target_lemo = 0
    lemo_enables = current_config['data']['lemo_enables']
    fake_spill_status = target_enable_value = next(item['enable'] for item in lemo_enables if item['lemo'] == target_lemo)

    target_lemo = 2
    lemo_enables = current_config['data']['lemo_enables']
    fake_busy_status = target_enable_value = next(item['enable'] for item in lemo_enables if item['lemo'] == target_lemo)

    #Retrieve SEC_C output status on device 2
    output_status = N1081B_device1.get_output_channel_configuration(N1081B.Section.SEC_C,0)
    master_trigger_status = output_status['data'].get('status')

    #Retrieve SEC_X input status on device X
    input_status = N1081B_device1.get_input_channel_configuration(N1081B.Section.SEC_A,0)
    real_spill_status = N1081B_device1.get_input_channel_configuration(N1081B.Section.SEC_A,0)['data'].get('status')

    # Set the background color of the QLabel based on the status
    cal_status_label.setStyleSheet("background-color: green" if cal_status else "background-color: gray")
    real_spill_status_label.setStyleSheet("background-color: green" if real_spill_status else "background-color: gray")
    fake_spill_status_label.setStyleSheet("background-color: green" if fake_spill_status else "background-color: gray")
    master_trigger_status_label.setStyleSheet("background-color: green" if master_trigger_status else "background-color: gray")

# def update_lcd():
#     target_lemo = 1
#     lemo_counters = current_config['data']['counters']
#     scaler_2 = next(item['value'] for item in lemo_counters if item['lemo'] == target_lemo)
#     triggers_lcd.display(scaler_2)

def reset_scalers():
    N1081B_device1.reset_channel(N1081B.Section.SEC_D,0,N1081B.FunctionType.FN_SCALER)
    N1081B_device1.reset_channel(N1081B.Section.SEC_D,1,N1081B.FunctionType.FN_SCALER)
    #update_lcd()    
 
N1081B_device1 = N1081B("128.141.115.123")
N1081B_device1.connect()

N1081B_device2 = N1081B("128.141.115.123")
N1081B_device2.connect()

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("N1081B Control for PAN TB")
window.resize(400, 300)

layout = QVBoxLayout()

# Create a horizontal layout for each status indicator
cal_layout = QHBoxLayout()
fake_spill_layout = QHBoxLayout()
real_spill_layout = QHBoxLayout()
master_trigger_layout = QHBoxLayout()

triggers_layout = QHBoxLayout()

resete_scalers_layout = QHBoxLayout()

# ENABLE CAL button 
enable_button = QPushButton("ENABLE CAL")
enable_button.clicked.connect(enable_calibration)
enable_button.setStyleSheet("font-size: 20px;")
layout.addWidget(enable_button)

# DISABLE CAL button 
disable_button = QPushButton("DISABLE CAL")
disable_button.clicked.connect(disable_calibration)
disable_button.setStyleSheet("font-size: 20px;")
layout.addWidget(disable_button)

# ENABLE FAKE SPILL button 
enable_spill_button = QPushButton("ENABLE FAKE SPILL")
enable_spill_button.clicked.connect(enable_fake_spill)
enable_spill_button.setStyleSheet("font-size: 20px;")
layout.addWidget(enable_spill_button)

# DISABLE FAKE SPILL button 
disable_spill_button = QPushButton("DISABLE FAKE SPILL")
disable_spill_button.clicked.connect(disable_fake_spill)
disable_spill_button.setStyleSheet("font-size: 20px;")
layout.addWidget(disable_spill_button)

# ENABLE MASTER TRIGGER button
enable_master_trigger_button = QPushButton("ENABLE MASTER TRIGGER")
enable_master_trigger_button.clicked.connect(enable_master_trigger)
enable_master_trigger_button.setStyleSheet("font-size: 20px;")
layout.addWidget(enable_master_trigger_button)

# DISABLE MASTER TRIGGER button
disable_master_trigger_button = QPushButton("DISABLE MASTER TRIGGER")
disable_master_trigger_button.clicked.connect(disable_master_trigger)
disable_master_trigger_button.setStyleSheet("font-size: 20px;")
layout.addWidget(disable_master_trigger_button)


# Add text label to the left of each LED indicator
cal_label = QLabel("CAL ENABLE")
cal_layout.addWidget(cal_label)
cal_status_label = QLabel()
cal_status_label.setFixedSize(20, 20)
cal_layout.addWidget(cal_status_label)
layout.addLayout(cal_layout)

real_spill_label = QLabel("REAL SPILL")
real_spill_layout.addWidget(real_spill_label)
real_spill_status_label = QLabel()
real_spill_status_label.setFixedSize(20, 20)
real_spill_layout.addWidget(real_spill_status_label)
layout.addLayout(real_spill_layout)

fake_spill_label = QLabel("FAKE SPILL")
fake_spill_layout.addWidget(fake_spill_label)
fake_spill_status_label = QLabel()
fake_spill_status_label.setFixedSize(20, 20)
fake_spill_layout.addWidget(fake_spill_status_label)
layout.addLayout(fake_spill_layout)

master_trigger_label = QLabel("TRIGGER OUTPUT")
master_trigger_layout.addWidget(master_trigger_label)
master_trigger_status_label = QLabel()
master_trigger_status_label.setFixedSize(20, 20)
master_trigger_layout.addWidget(master_trigger_status_label)
layout.addLayout(master_trigger_layout)

# Add a QLCDNumber to display the number of triggers
triggers_label = QLabel("TRIGGERS")
triggers_layout.addWidget(triggers_label)
triggers_lcd = QLCDNumber()
triggers_lcd.setFixedSize(250, 30)
triggers_layout.addWidget(triggers_lcd)
layout.addLayout(triggers_layout)

triggers_lcd.setDigitCount(12)
triggers_lcd.setSegmentStyle(QLCDNumber.Flat)

# Add a RESET SCALERS button
reset_scalers_button = QPushButton("RESET SCALERS")
reset_scalers_button.clicked.connect(reset_scalers)
reset_scalers_button.setStyleSheet("font-size: 20px;")
layout.addWidget(reset_scalers_button)

update_status_labels()
#update_lcd() 

# Set a timer to update the lcd every 1s
timer = QTimer()
#timer.timeout.connect(update_lcd)
# Update the status labels
timer.timeout.connect(update_status_labels)
timer.start(1000)

window.setLayout(layout)
window.show()

sys.exit(app.exec_())
