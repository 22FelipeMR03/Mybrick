#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, ColorSensor, InfraredSensor)
from pybricks.parameters import Port, Color, Button
from pybricks.robotics import DriveBase
from pybricks.tools import wait

# Criação dos objetos
ev3 = EV3Brick()
motorB = Motor(Port.B)
motorD = Motor(Port.D)
color1 = ColorSensor(Port.S1)
color = ColorSensor(Port.S3)
ir_sensor = InfraredSensor(Port.S4)  # Adiciona o sensor infravermelho
robot = DriveBase(motorB, motorD, wheel_diameter=55.5, axle_track=104)

# Valores de calibração
calibration_values = {
    "BRANCO": (0, 0, 0),
    "PRETO": (0, 0, 0),
    "VERDE": (0, 0, 0),
    "MARROM": (0, 0, 0),
    "AMARELO": (0, 0, 0),
    "VERMELHO": (0, 0, 0)
}

# Função de calibração para um sensor e uma cor específicos
def calibrar_cor(sensor, nome_cor):
    ev3.speaker.beep()
    print(f"Coloque o sensor na cor {nome_cor} e pressione o botão central")
    while Button.CENTER not in ev3.buttons.pressed():
        pass
    calibration_values[nome_cor] = sensor.rgb()
    print(f"{nome_cor} calibrado para {calibration_values[nome_cor]}")
    wait(1000)

# Calibrar ambos os sensores para cada cor
def calibrar_sensores():
    cores = ["BRANCO", "PRETO", "VERDE", "MARROM", "AMARELO", "VERMELHO"]
    for cor in cores:
        calibrar_cor(color1, cor + "_1")
        calibrar_cor(color, cor + "_2")
    print("Calibração concluída")

# Chamar a função de calibração
calibrar_sensores()

# Função para determinar a cor baseada na calibração
def obter_cor(sensor):
    rgb = sensor.rgb()
    min_diff = float('inf')
    cor_detectada = None
    for nome_cor, valor in calibration_values.items():
        diff = sum((a - b) ** 2 for a, b in zip(rgb, valor))
        if diff < min_diff:
            min_diff = diff
            cor_detectada = nome_cor
    return cor_detectada

# Função para desviar de obstáculo
def desviar_obstaculo():
    robot.straight(-150)  # Recuar
    robot.turn(90)        # Girar para a direita
    robot.straight(150)   # Avançar
    robot.turn(-90)       # Girar para a esquerda para voltar à direção original
    robot.straight(150)   # Avançar novamente

# Loop principal do programa
while True:
    # Verificar a distância do obstáculo
    distancia = ir_sensor.distance()
    if distancia < 30:  # Distância em centímetros
        desviar_obstaculo()
        continue  # Pula o restante do loop e volta ao início

    cor1 = obter_cor(color1)
    cor = obter_cor(color)
    print(cor, cor1)

    if cor1 == "BRANCO_1" and cor == "BRANCO_2":
        robot.straight(100)  # Avançar reto (100 mm)
    elif cor1 == "PRETO_1" and cor == "BRANCO_2":
        motorB.run_time(-170, 1000)  # Girar motor B para trás por 1 segundo
        motorD.run_time(100, 1000)   # Girar motor D para frente por 1 segundo
    elif cor == "PRETO_2" and cor1 == "BRANCO_1":
        motorD.run_time(-170, 1000)  # Girar motor D para trás por 1 segundo
        motorB.run_time(100, 1000)   # Girar motor B para frente por 1 segundo
    elif cor == "PRETO_2" and cor1 == "PRETO_1":
        robot.straight(2000)  # Avançar reto (2000 mm)
    elif cor == "VERDE_2" and cor1 == "BRANCO_1":
        robot.turn(-90)  # Girar 90 graus para a esquerda
        robot.straight(100)  # Avançar reto (100 mm)
    elif cor == "BRANCO_2" and cor1 == "PRETO_1":
        robot.turn(90)  # Girar 90 graus para a direita
        robot.straight(100)  # Avançar reto (100 mm)
    elif cor in ["MARROM_2", "AMARELO_2"]:
        robot.straight(-200)  # Recuar reto (200 mm)
    elif cor == "VERMELHO_2" and cor1 == "VERMELHO_1":
        wait(10000)  # Esperar 10 segundos
