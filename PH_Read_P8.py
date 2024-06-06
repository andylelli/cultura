import requests
import time
import sys
import smbus2
sys.path.insert(0,'/home/andylelli/gravity/GreenPonik_PH_Python/libs')
sys.path.insert(0,'/home/andylelli/gravity/GreenPonik_PH_Python/src')


from DFRobot_ADS1115 import ADS1115
from GreenPonik_PH import GreenPonik_PH

ADS1115_REG_CONFIG_PGA_6_144V = 0x00  # 6.144V range = Gain 2/3
ADS1115_REG_CONFIG_PGA_4_096V = 0x02  # 4.096V range = Gain 1
ADS1115_REG_CONFIG_PGA_2_048V = 0x04  # 2.048V range = Gain 2 (default)
ADS1115_REG_CONFIG_PGA_1_024V = 0x06  # 1.024V range = Gain 4
ADS1115_REG_CONFIG_PGA_0_512V = 0x08  # 0.512V range = Gain 8
ADS1115_REG_CONFIG_PGA_0_256V = 0x0A  # 0.256V range = Gain 16

## I2C address of the device
ADS1115_IIC_ADDRESS0				= 0x48
ADS1115_IIC_ADDRESS1				= 0x49

## ADS1115 Register Map
## Conversion register
ADS1115_REG_POINTER_CONVERT			= 0x00 
## Configuration register
ADS1115_REG_POINTER_CONFIG			= 0x01 
## Lo_thresh register
ADS1115_REG_POINTER_LOWTHRESH		= 0x02 
## Hi_thresh register
ADS1115_REG_POINTER_HITHRESH		= 0x03 

## ADS1115 Configuration Register
## No effect
ADS1115_REG_CONFIG_OS_NOEFFECT		= 0x00 
## Begin a single conversion
ADS1115_REG_CONFIG_OS_SINGLE		= 0x80 
## Differential P = AIN0, N = AIN1 (default)
ADS1115_REG_CONFIG_MUX_DIFF_0_1		= 0x00 
## Differential P = AIN0, N = AIN3
ADS1115_REG_CONFIG_MUX_DIFF_0_3		= 0x10 
## Differential P = AIN1, N = AIN3
ADS1115_REG_CONFIG_MUX_DIFF_1_3		= 0x20 
## Differential P = AIN2, N = AIN3
ADS1115_REG_CONFIG_MUX_DIFF_2_3		= 0x30 
## Single-ended P = AIN0, N = GND
ADS1115_REG_CONFIG_MUX_SINGLE_0		= 0x40 
## Single-ended P = AIN1, N = GND
ADS1115_REG_CONFIG_MUX_SINGLE_1		= 0x50 
## Single-ended P = AIN2, N = GND
ADS1115_REG_CONFIG_MUX_SINGLE_2		= 0x60 
## Single-ended P = AIN3, N = GND
ADS1115_REG_CONFIG_MUX_SINGLE_3		= 0x70 
## +/-6.144V range = Gain 2/3
ADS1115_REG_CONFIG_PGA_6_144V		= 0x00 
## +/-4.096V range = Gain 1
ADS1115_REG_CONFIG_PGA_4_096V		= 0x02 
## +/-2.048V range = Gain 2 (default)
ADS1115_REG_CONFIG_PGA_2_048V		= 0x04 
## +/-1.024V range = Gain 4
ADS1115_REG_CONFIG_PGA_1_024V		= 0x06 
## +/-0.512V range = Gain 8
ADS1115_REG_CONFIG_PGA_0_512V		= 0x08 
## +/-0.256V range = Gain 16
ADS1115_REG_CONFIG_PGA_0_256V		= 0x0A
## Continuous conversion mode
ADS1115_REG_CONFIG_MODE_CONTIN		= 0x00 
## Power-down single-shot mode (default)
ADS1115_REG_CONFIG_MODE_SINGLE		= 0x01 
## 8 samples per second
ADS1115_REG_CONFIG_DR_8SPS			= 0x00 
## 16 samples per second
ADS1115_REG_CONFIG_DR_16SPS			= 0x20 
## 32 samples per second
ADS1115_REG_CONFIG_DR_32SPS			= 0x40 
## 64 samples per second
ADS1115_REG_CONFIG_DR_64SPS			= 0x60 
## 128 samples per second (default)
ADS1115_REG_CONFIG_DR_128SPS		= 0x80
## 250 samples per second
ADS1115_REG_CONFIG_DR_250SPS		= 0xA0 
## 475 samples per second
ADS1115_REG_CONFIG_DR_475SPS		= 0xC0 
## 860 samples per second
ADS1115_REG_CONFIG_DR_860SPS		= 0xE0 
## Traditional comparator with hysteresis (default)
ADS1115_REG_CONFIG_CMODE_TRAD		= 0x00 
## Window comparator
ADS1115_REG_CONFIG_CMODE_WINDOW		= 0x10 
## ALERT/RDY pin is low when active (default)
ADS1115_REG_CONFIG_CPOL_ACTVLOW		= 0x00 
## ALERT/RDY pin is high when active
ADS1115_REG_CONFIG_CPOL_ACTVHI		= 0x08 
## Non-latching comparator (default)
ADS1115_REG_CONFIG_CLAT_NONLAT		= 0x00 
## Latching comparator
ADS1115_REG_CONFIG_CLAT_LATCH		= 0x04 
## Assert ALERT/RDY after one conversions
ADS1115_REG_CONFIG_CQUE_1CONV		= 0x00 
## Assert ALERT/RDY after two conversions
ADS1115_REG_CONFIG_CQUE_2CONV		= 0x01 
## Assert ALERT/RDY after four conversions
ADS1115_REG_CONFIG_CQUE_4CONV		= 0x02 
## Disable the comparator and put ALERT/RDY in high state (default)
ADS1115_REG_CONFIG_CQUE_NONE		= 0x03 

ads1115 = ADS1115()
ph = GreenPonik_PH()
ph.begin()

bus = smbus2.SMBus(1)  # Use bus number 1

def api(channel, PH, unixTime):
    
    # Define the URL to which you want to send the POST request.
    url = 'https://phplaravel-1159228-4372033.cloudwaysapps.com/api/sensor/submit'

    # Define the data fields.
    data = {
        'channel': channel,
        'ph': PH,
        'time': unixTime
    }

    # Send the POST request with the data.
    response = requests.post(url, json=data)

    # Check if the request was successful (status code 201).
    if response.status_code == 201:
        print('POST request successful!')
    else:
        print('POST request failed with status code:', response.status_code)

def read_ph(address, channel, sensor):
    global ph

    adc1 = read_voltage(channel)
    
    # Convert voltage to pH
    PH = ph.readPH(adc1['r'], sensor)
    
    # Generate UNIX timestamp
    unixTime = int(time.time())
    
    # Write to screen
    print("Address: ", address, "Channel: ", channel, "Name: ", sensor, " PH:%.2f " % (PH))

    api(sensor, PH, unixTime)
    
    return PH
    
def read_voltage(channel):
            
    '''!
      @brief Configuration using a single read.
    '''
    addr_G = 0x48
    mygain = 0.1875
    mygain = 1
    
    if channel == 0:
        CONFIG_REG = [ADS1115_REG_CONFIG_OS_SINGLE | ADS1115_REG_CONFIG_MUX_SINGLE_0 | mygain | ADS1115_REG_CONFIG_MODE_CONTIN, ADS1115_REG_CONFIG_DR_128SPS | ADS1115_REG_CONFIG_CQUE_NONE]
    elif channel == 1:
        CONFIG_REG = [ADS1115_REG_CONFIG_OS_SINGLE | ADS1115_REG_CONFIG_MUX_SINGLE_1 | mygain | ADS1115_REG_CONFIG_MODE_CONTIN, ADS1115_REG_CONFIG_DR_128SPS | ADS1115_REG_CONFIG_CQUE_NONE]
    elif channel == 2:
        CONFIG_REG = [ADS1115_REG_CONFIG_OS_SINGLE | ADS1115_REG_CONFIG_MUX_SINGLE_2 | mygain | ADS1115_REG_CONFIG_MODE_CONTIN, ADS1115_REG_CONFIG_DR_128SPS | ADS1115_REG_CONFIG_CQUE_NONE]
    elif channel == 3:
        CONFIG_REG = [ADS1115_REG_CONFIG_OS_SINGLE | ADS1115_REG_CONFIG_MUX_SINGLE_3 | mygain | ADS1115_REG_CONFIG_MODE_CONTIN, ADS1115_REG_CONFIG_DR_128SPS | ADS1115_REG_CONFIG_CQUE_NONE]

    time.sleep(1)
    print("CONFIG_REG")
    print(CONFIG_REG)
    
    bus.write_i2c_block_data(0x48, 0x00, CONFIG_REG)
    
    return read_value()    
    
def read_value():
    '''!
      @brief  Read ADC value.
      @return raw  adc
    '''
    coefficient = 0.1875
    addr_G = 0x48
    reg = 0x01
    
    data = bus.read_i2c_block_data(addr_G, reg, 2)
    
    # Convert the data
    raw_adc = data[0] * 256 + data[1]
    
    if raw_adc > 32767:
        raw_adc -= 65535
    raw_adc = int(float(raw_adc)*coefficient)
    return {'r' : raw_adc}
        
if __name__ == "__main__":
    while True:

        mux_address = 0x70
        mux_channel = 0  # Select the channel of the multiplexer

        # Select the channel of the multiplexer
        bus.write_byte(mux_address, mux_channel)

        # Write to the device to specify the channel
        #bus.write_byte_data(device_address, channel_register, channel_value)

        # Read from the device
        #data = bus.read_byte_data(device_address, register)
        #print("Data read:", data)
        
        read_ph(0x48, 0, 1)
        #read_ph(0x48, 1, 2)
        #read_ph(0x48, 2, 3)
        #read_ph(0x48, 3, 4)
        #read_ph(0x49, 0, 5)
        #read_ph(0x49, 1, 6)
        #read_ph(0x49, 2, 7)
        #read_ph(0x49, 3, 8)        
        #time.sleep(10)                        
