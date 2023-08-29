import time
import requests
import math
import random
import board
import os
import time
import busio
from time import sleep
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

TOKEN = "BBFF-ec1vor7GomhjjKENts4iEzIbZrYCQs"  # Put your TOKEN here
DEVICE_LABEL = "dreamsquad"  # Put your device label here 
VARIABLE_LABEL_1 = "Sensor_TDS"  # Put your first variable label here
VARIABLE_LABEL_2 = "Sensor_ph"  # Put your second variable label here

def build_payload(variable_1, variable_2):
    #########TDS##############
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    ads.gain =2
    tdsanalog = AnalogIn(ads, ADS.P2)
    valuetds = tdsanalog.value
    volttds = (valuetds/32767*4.6)
    tds  = (-37.2)*volttds*volttds*volttds + (533.4)*volttds*volttds+ (121.8)*volttds + 2.8
    print("TDS value is ",tds,"ppm")
    print(volttds)
    ###################################

    #########PH########################
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    ads.gain =1
    k = 12.925
    phanalog = AnalogIn(ads, ADS.P0)
    valueph = phanalog.value
    #voltph = (valueph/65536*4.6)
    voltage = valueph*(5.0/65536)
    ph = k*voltage
    print ("pH value is", ph)
    ####################################
    # Creates two random values for sending data
    value_1 = ph
    value_2 = tds

    payload = {variable_1: value_1,
               variable_2: value_2}

    return payload


def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True


def main():
    payload = build_payload(
        VARIABLE_LABEL_1, VARIABLE_LABEL_2)

    print("[INFO] Attemping to send data")
    post_request(payload)
    print("[INFO] finished")


if __name__ == '__main__':
    while (True):
        main()
   

