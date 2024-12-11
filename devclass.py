# Import required modules/packages/library
import pexpect

# Class to hold information about a generic network device
class NetworkDevice():
 def __init__(self, name, ip, user='cisco', pw='cisco123!'):
 self.name = name
 self.ip_address = ip
 self.username = user
 self.password = pw
 def connect(self):
 self.session = None
 def get_interfaces(self):
 self.interfaces = '--- Base Device, unknown get interfaces ---'

  # Class to hold information about an IOS network device
class NetworkDeviceIOS(NetworkDevice):
 def __init__(self, name, ip, user='cisco', pw='cisco123!'):
 NetworkDevice.__init__(self, name, ip, user, pw)
 def connect(self):
 print('--- connecting IOS: telnet ' + self.ip_address)
 self.session = pexpect.spawn('telnet ' + self.ip_address,
 encoding='utf-8', timeout=20)
 result = self.session.expect(['Username:', pexpect.TIMEOUT, pexpect.EOF])
 self.session.sendline(self.username)
 result = self.session.expect('Password:')
 # Successfully got password prompt, logging in with password
 self.session.sendline(self.password)
 self.session.expect(['>', pexpect.TIMEOUT, pexpect.EOF])
 # Must set terminal length to zero for long replies, no pauses
 self.session.sendline('terminal length 0')
 result = self.session.expect(['>', pexpect.TIMEOUT, pexpect.EOF])
 def get_interfaces(self):
 self.session.sendline('show interfaces summary')
 result = self.session.expect(['>', pexpect.TIMEOUT, pexpect.EOF])
 self.interfaces = self.session.before

  # Class to hold information about an IOS-XR network device
class NetworkDeviceXR(NetworkDevice):
 # Initialize
 def __init__(self, name, ip, user='cisco', pw='cisco123!'):
 NetworkDevice.__init__(self, name, ip, user, pw)
 # Connect to device
 def connect(self):
 print('--- connecting XR: ssh '+ self.username + '@' +
 self.ip_address)
 self.session = pexpect.spawn('ssh ' + self.username +
 '@' + self.ip_address,
encoding='utf-8', timeout=20)
 result = self.session.expect(['password:', pexpect.TIMEOUT, pexpect.EOF])
 # Check for failure
 if result != 0:
 print('--- Timout or unexpected reply from device')
 return 0
 # Successfully got password prompt, logging in with password
 print('--- password:', self.password)
 self.session.sendline(self.password)
 self.session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])
 # Get interfaces from device
 def get_interfaces(self):
 self.session.sendline('show interface brief')
 result = self.session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])
 self.interfaces = self.session.before
