from time import sleep
from utils import set_speed, red_autonomous_behavior, blue_autonomous_behavior, forward, backward, left, right, stop, servo_up, servo_down, servo_open, servo_close, Start, uart

# Set initial speed
set_speed(50000)

# Mode tracking
autonomous_mode = True
autonomous_completed = False

Start()
print("Started")
sleep(3)

# Clear any initial UART data from Bluetooth module connection
while uart.any():
    uart.read()

#Main loop
while True:
    if autonomous_mode and not autonomous_completed:
        # Run autonomous behavior and check for manual override
        if blue_autonomous_behavior():
            # Manual override detected
            autonomous_mode = False
        else:
            # Autonomous completed normally
            autonomous_completed = True
            autonomous_mode = False
            stop()
    else:
        # Manual mode
        if uart.any():
            value = uart.readline()
            print(value)

            if value == b'F':
                forward()
            elif value == b'B':
                backward()
            elif value == b'L':
                left()
            elif value == b'R':
                right()
            elif value == b'S':
                stop()
            elif value == b'1':
                servo_down()
            elif value == b'2':
                servo_up()
            elif value == b'3':
                servo_open()
            elif value == b'4':
                servo_close()




