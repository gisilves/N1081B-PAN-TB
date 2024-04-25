import pprint
import json
from N1081B_sdk import N1081B

pp = pprint.PrettyPrinter(indent=4)

print("Info for the first device")

N1081B_device1 = N1081B("pool05940004.cern.ch")
N1081B_device1.connect()
version_json = N1081B_device1.get_version()
pp.pprint(version_json)
serial_number = version_json["data"]["serial_number"]
software_version = version_json["data"]["software_version"]
zynq_version = version_json["data"]["zynq_version"]
fpga_version = version_json["data"]["fpga_version"]

#Download the configuration file to the device
config1 = N1081B_device1.download_configuration_file("Config_1")
print(config1)
with open('config1.json', 'w') as outfile:
    json.dump(config1, outfile)


print("\n\n\n")

print("Info for the second device")

N1081B_device2 = N1081B("pool05940001.cern.ch")
N1081B_device2.connect()
version_json = N1081B_device2.get_version()
pp.pprint(version_json)
serial_number = version_json["data"]["serial_number"]
software_version = version_json["data"]["software_version"]
zynq_version = version_json["data"]["zynq_version"]
fpga_version = version_json["data"]["fpga_version"]

#Download the configuration file to the device
config2 = N1081B_device2.download_configuration_file("Config_2")
print(config2)
with open('config2.json', 'w') as outfile:
    json.dump(config2, outfile)







