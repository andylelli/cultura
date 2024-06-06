import time
import sys
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

ads1115 = ADS1115()
ph = GreenPonik_PH()
ph.begin()

def calibration(sensor):
    global ads1115
    global ph
    
    #Convert sensor to start from 0
    channel_raw = sensor - 1
    
    # Deduce the ads1115 address
    if channel_raw >= 0 and channel_raw <=3:
        address = 0x48
    else:
        address = 0x49
     
    # Set the ads1115 address
    ads1115.set_addr_ADS1115(address) 
        
    # GSt the ADC address (between 0 & 3)
    channel = channel_raw % 4

    # Sets the gain and input voltage range.
    ads1115.set_gain(ADS1115_REG_CONFIG_PGA_6_144V)
    
    # Get the Digital Value of Analog of selected channel
    adc1 = ads1115.read_voltage(channel)
    
    print("Calibrating sensor ", sensor, " - voltage: %.3f" % adc1['r'])
    print("Address: ", address)
    print("Channel: ", channel)
    return ph.calibration(adc1['r'], channel_raw)


if __name__ == "__main__":
    while True:
        sensor = 8
        calibration(sensor)
        time.sleep(1)
