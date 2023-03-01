import machine
from pyb import ADC, Pin
import time

# Power Joystick
machine.Pin('A0', machine.Pin.OUT).low()
machine.Pin('A2', machine.Pin.OUT).high()
machine.Pin('A4', machine.Pin.OUT).low()
xAxis = ADC(machine.Pin('A3'))
yAxis = ADC(machine.Pin('A1'))
JsSwitch = ADC(machine.Pin('A5'))
hid = pyb.USB_HID()
prev = 1000
countxpos = 0
countxneg = 0
countypos = 0
countyneg = 0

while (1):
    x = xAxis.read()
    y = yAxis.read()
    if x < 1500:
        countxpos = 0
        if countxneg < 300:
            countxneg +=1
    elif x > 2200:
        if countxpos < 300:
            countxpos +=1
        countxneg = 0
    else:
        countxpos = 0
        countxneg = 0
    if y < 1400:
        countypos = 0
        if countyneg < 300:
            countyneg +=1
    elif y > 2200:
        if countypos < 300:
            countypos +=1
        countyneg = 0
    else:
        countypos = 0
        countyneg = 0
    val = JsSwitch.read()
    # hid.send((JsSwitch.read()<100, round(xAxis.read()/500) - 4, round(yAxis.read()/500)-4, 0))
    hid.send((val<100 and prev<100, -round((countypos - countyneg) / 75), -round((countxpos - countxneg) / 75), 0))
    prev = val
    #print("xpos = ", countxpos, "ypos = ", countypos, "xneg = ", countxneg, "yneg = ", countyneg, "sw = ", JsSwitch.read())
