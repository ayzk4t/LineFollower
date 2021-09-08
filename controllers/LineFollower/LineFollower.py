import time

from controller import Robot, Camera

# Zmienne symulacji
track = "3"
algorithm = "Adaptacyjny"

# Instancja robota
robot = Robot()

# Prędkość maksymalna
max_speed = 6.28
# max_speed = 4.6


# Krok symulacji
timestep = int(robot.getBasicTimeStep())

# Deklaracja i inicjalizacja silników
leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)

# Włączenie czujników podczerwieni
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
# flaga czy robot wykryl ostry skret
turn = False
# flaga czy robot wykryl tor
flag = False
y = 128

start_time = time.time()

while robot.step(timestep) != -1:
    L_IR_value = L_IR.getValue()
    R_IR_value = R_IR.getValue()
    ML_IR_value = ML_IR.getValue()
    MR_IR_value = MR_IR.getValue()
    LS_IR_value = LS_IR.getValue()
    RS_IR_value = RS_IR.getValue()
    
    if turn == False:
        max_speed = 6.28
    row = []
    left = []
    right = []
    left_speed = max_speed
    right_speed = max_speed
    
    cameraData = cam.getImage()
    for x in range(0, cam.getWidth()):
        gray = Camera.imageGetGray(cameraData, cam.getWidth(), x, y)
        row.append(gray)
    left = row[0:y]
    right = row[y:2*y]
    left.reverse()
    if max(left) < 60 or max(right) < 60:
        turn = True
        max_speed = 4.6

    if (L_IR_value > 1000 and R_IR_value > 1000 and ML_IR_value > 1000 and MR_IR_value > 1000 and
            L_IR_value < 1500 and R_IR_value < 1500 and ML_IR_value < 1500 and MR_IR_value < 1500 and flag):
        robot.step(timestep)
        robot.step(timestep)
        leftMotor.setVelocity(0)
        rightMotor.setVelocity(0)
        if LS_IR_value > 1000:
            while ML_IR_value > 300:
                # ostry skręt w prawo
                leftMotor.setVelocity(max_speed)
                rightMotor.setVelocity(-max_speed)
                ML_IR_value = L_IR.getValue()
                robot.step(timestep)
            turn = False
        else:
            while MR_IR_value > 300:
                # ostry skręt w lewo
                leftMotor.setVelocity(-max_speed)
                rightMotor.setVelocity(max_speed)
                MR_IR_value = R_IR.getValue()
                robot.step(timestep)
            turn = False
    elif L_IR_value > 1000 and R_IR_value < 1000:
        if ML_IR_value > 1000:
            # skręt w prawo
            right_speed = max_speed * 0.3
            flag = True
        else:
            # lekki skręt w prawo
            right_speed = max_speed * 0.8
            flag = True
    elif R_IR_value > 1000 and L_IR_value < 1000:
        if MR_IR_value > 1000:
            # skręt w lewo
            left_speed = max_speed * 0.3
            flag = True
        else:
            # lekki skręt w lewo
            left_speed = max_speed * 0.8
            flag = True

    leftMotor.setVelocity(left_speed)
    rightMotor.setVelocity(right_speed)

    if ML_IR_value > 1550 and MR_IR_value > 1550 and flag:
        leftMotor.setVelocity(0)
        rightMotor.setVelocity(0)
        break

elapsed_time = round(time.time() - start_time, 2)
with open("wyniki.txt", "a") as f:
    f.write("Tor: {}\nRodzaj: {}\nCzas: {}s\n\n".format(track, algorithm, elapsed_time))
