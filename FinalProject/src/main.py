from Adafruit_IO import Client
from i2c_device import I2CDevice
print("loading pynq overlay...")
from pynq.overlays.base import BaseOverlay
from pynq.lib import MicroblazeLibrary
base = BaseOverlay("base.bit")
ADDR = 8
SCL_PIN = 2
SDA_PIN = 3
DATA_LEN = 5 #bytes
liba = MicroblazeLibrary(base.PMODA, ['i2c'])
arduino = I2CDevice(liba, SDA_PIN, SCL_PIN, ADDR, DATA_LEN)

UNAME = input('Enter username: ')
KEY = input('Enter Key: ')
FEED = 'welcome-feed'

#Create a client that can send information to the Adafruit Cloud
aio = Client(UNAME, KEY)
#create the feed that the data gets sent to
feed = aio.feeds(FEED)

response = input('\t-Read Temp(y/n): ')
while response != 'n':
    data = arduino.read_and_get_data()
    #send the data to desired feed
    aio.send(feed.key, data)
    response = input('\t-Read Temp(y/n): ')
