import requests
import time
import sys
sys.path.insert(0,'../libs/')
sys.path.insert(0,'../src/')


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

def api(PH, unixTime):
    
    # Define the URL to which you want to send the POST request.
    url = 'https://phplaravel-1159228-4372033.cloudwaysapps.com/api/sensor/submit'

    # Define the data fields.
    data = {
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

def read_ph():
    global ads1115
    global ph
    # Set the IIC address
    #ads1115.setAddr_ADS1115(0x48)
    ads1115.set_addr_ADS1115(0x48)
    
    # Sets the gain and input voltage range.
    ads1115.set_gain(ADS1115_REG_CONFIG_PGA_6_144V)
    
    # Get the Digital Value of Analog of selected channel
    adc1 = ads1115.read_voltage(0)
    
    # Convert voltage to pH
    PH = ph.readPH(adc1['r'])
    
    # Generate UNIX timestamp
    unixTime = int(time.time())
    
    # Write to screen
    print("PH:%.2f " % (PH))
    
    api(PH, unixTime)
    
    return PH


if __name__ == "__main__":
    while True:
        read_ph()
        time.sleep(5)
