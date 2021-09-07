import time
from controller import Robot, Camera


def get_ir_value(LS_IR, L_IR, ML_IR, MR_IR, R_IR, RS_IR):
    IR_VALUE = []
    IR_VALUE.append(LS_IR.getValue())
    IR_VALUE.append(L_IR.getValue())
    IR_VALUE.append(ML_IR.getValue())
    IR_VALUE.append(MR_IR.getValue())
    IR_VALUE.append(R_IR.getValue())
    IR_VALUE.append(RS_IR.getValue())
    return IR_VALUE


# Zmienne symulacji
track = "3"
algorithm = "Adaptacyjny"

# Instancja robota
robot = Robot()

# Predkosc maksymalna
max_speed = 6.28
# max_speed = 4.6
# max_speed = 4.6

# Krok symulacji
timestep = int(robot.getBasicTimeStep())

# Deklaracja i inicjalizacja silnikow
leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)

# Wlaczenie czujnikow podczerwieni
L_IR = robot.getDevice('ir_L')
L_IR.enable(timestep)
R_IR = robot.getDevice('ir_R')
R_IR.enable(timestep)
ML_IR = robot.getDevice('ir_ML')
ML_IR.enable(timestep)
MR_IR = robot.getDevice('ir_MR')
MR_IR.enable(timestep)
LS_IR = robot.getDevice('ir_LS')
LS_IR.enable(timestep)
RS_IR = robot.getDevice('ir_RS')
RS_IR.enable(timestep)

# Wlaczenie kamery
cam = robot.getDevice('CAM')
cam.enable(timestep)
# flaga czy robot wykryl tor
flag = False
i = 0
# flaga czy robot wykryl ostry skret
turn = False
# polowa rozdzielczosci kamery
y = 128

start_time = time.time()

# Petla glowna progaramu
###################################################################################
while robot.step(timestep) != -1:
    row = []
    left = []
    right = []
    ir_values = get_ir_value(LS_IR, L_IR, ML_IR, MR_IR, R_IR, RS_IR)
    left_speed = max_speed
    right_speed = max_speed
    cameraData = cam.getImage()
    for x in range(0, cam.getWidth()):
        gray = Camera.imageGetGray(cameraData, cam.getWidth(), x, 200)
        row.append(gray)
    left = row[0:y]
    right = row[y:2*y]
    left.reverse()
    if (max(left[0:64]) < 60 or max(right[0:64]) < 60) :
        turn = True
        max_speed = 4.6
    elif  (max(left[0:64]) > 60 and left[64] < 60) or (max(right[0:64]) > 60 and right[64] < 60) :
        turn = True
        max_speed = 1
    if turn and (ir_values[0] < 300 or ir_values[5] < 300):
        if ir_values[0] > 1000:
            for x in range(25):
                # ostry skret w prawo
                leftMotor.setVelocity(max_speed)
                rightMotor.setVelocity(-max_speed)
                ir_values[2] = L_IR.getValue()
                robot.step(timestep)
        else:
            for x in range(25):
                # ostry skret w lewo
                leftMotor.setVelocity(-max_speed)
                rightMotor.setVelocity(max_speed)
                ir_values[3] = R_IR.getValue()
                robot.step(timestep)
        turn = False
        max_speed = 6.28
    elif ir_values[1] > 1000 and ir_values[4] < 1000:
        if ir_values[2] > 1000:
            # skret w prawo
            right_speed = max_speed * 0.3
            flag = True
        else:
            # lekki skret w prawo
            right_speed = max_speed * 0.8
            flag = True
    elif ir_values[4] > 1000 and ir_values[1] < 1000:
        if ir_values[3] > 1000:
            # skret w lewo
            left_speed = max_speed * 0.3
            flag = True
        else:
            # lekki skret w lewo
            left_speed = max_speed * 0.8
            flag = True

    leftMotor.setVelocity(left_speed)
    rightMotor.setVelocity(right_speed)

    if ir_values[2] > 1550 and ir_values[3] > 1550 and flag:
        leftMotor.setVelocity(0)
        rightMotor.setVelocity(0)
        break

elapsed_time = round(time.time() - start_time, 2)
with open("wyniki.txt", "a") as f:
    f.write("Tor: {}\nRodzaj: {}\nCzas: {}s\n\n".format(track, algorithm, elapsed_time))
    """
    Zatrzymanie czasu oraz zapis wyniku do pliku tekstowego
    """
