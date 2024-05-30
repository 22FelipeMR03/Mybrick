#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.iodevices import UARTDevice
from pybricks.parameters import Port
from time import sleep


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()

motorB = Motor(Port.B)
motorD = Motor(Port.D)
color1 = ColorSensor(Port.S1)
color = ColorSensor(Port.S3)
velocidade = 150


uart = UARTDevice(port=Port.S1, baudrate=115200)

ev3.speaker.beep()
robot = DriveBase(motorB, motorD, wheel_diameter=55.5, axle_track=104)

while True:
    cor1 = color1.color()
    cor = color.color()
    print(cor,cor1)
    sensor_data = uart.read()
    if sensor_data:
        try:
            decoded_data = sensor_data.decode('utf-8').strip()
            print(f"Received: {decoded_data}")
            sensor_value = int(decoded_data)
            if sensor_value == 1:
                robot.straight(2000)  
                print("1")
            elif sensor_value == 2:
                motorB.run_time(-170, 1000)  
                motorD.run_time(100, 1000)   
                print("2")
            elif sensor_value == 3:
                motorD.run_time(-170, 1000)      
                motorB.run_time(100, 1000)
                print("3")
            elif sensor_value == 4:
                robot.straight(2000)  
                print("4")
            elif cor1 == Color.RED and cor == Color.RED:
                 wait(10000) 
        except (UnicodeDecodeError, ValueError):
            pass  # Ignora erros de decodificação ou conversão


             
 
   