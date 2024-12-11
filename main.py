# Import required modules/packages/library
from util import read_devices_info
from util import print_device_info
from util import write_devices_info

# read CSV info for all devices
devices_list = read_devices_info('devices-02.csv')

# Connect to device, show interface summary, display
for device in devices_list:
   print('==== Device ===============================================')
   # connect to this specific device
   device.connect()
   # get interface info for specific device
   device.get_interfaces()
   # print device details for this device
   print_device_info(device)
   # write CSV entry for all devices
Write_devices_info('devices-02-out.csv', devices_list)
