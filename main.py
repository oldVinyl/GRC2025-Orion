from machine import UART,Pin, PWM
from time import sleep, ticks_ms, ticks_diff
from math import fabs

# Set the relay pins as output pins
#motor 1
ENA = PWM(Pin(10))
m1_forward = Pin(11,Pin.OUT)
m1_backward = Pin(12,Pin.OUT)

#motor 2
m2_forward = Pin(14,Pin.OUT)
m2_backward = Pin(15,Pin.OUT)
ENB = PWM(Pin(13))

#motor 3
m3_forward = Pin(17,Pin.OUT)
m3_backward = Pin(16,Pin.OUT)
ENC = PWM(Pin(20))

#motor 4
m4_forward = Pin(18,Pin.OUT)
m4_backward = Pin(19,Pin.OUT)
END = PWM(Pin(21))

#servo motors
pwm_2 = PWM(Pin(18))
pwm_2.freq(50)
pwm_3 = PWM(Pin(19))
pwm_3.freq(50)

Start_Button = Pin(2,Pin.IN, Pin.PULL_UP)

uart = UART(0, 9600)

speed = 50000 # 0 - 65025

ENA.duty_u16(speed)
ENB.duty_u16(speed) 
ENC.duty_u16(speed)
END.duty_u16(speed)

# Mode tracking
autonomous_mode = True
autonomous_completed = False

def forward():
    disable_servos()
    m1_forward.on()
    m1_backward.off()
    m2_forward.on()
    m2_backward.off()
    m3_forward.on()
    m3_backward.off()
    m4_forward.on()
    m4_backward.off()

def backward():
    disable_servos()
    m1_forward.off()
    m1_backward.on()
    m2_forward.off()
    m2_backward.on()
    m3_forward.off()
    m3_backward.on()
    m4_forward.off()
    m4_backward.on()

def left():
    disable_servos()
    m1_forward.off()
    m1_backward.on()
    m2_forward.on()
    m2_backward.off()
    m3_forward.off()
    m3_backward.on()
    m4_forward.on()
    m4_backward.off()

def right():
    disable_servos()
    m1_forward.on()
    m1_backward.off()
    m2_forward.off()
    m2_backward.on()
    m3_forward.on()
    m3_backward.off()
    m4_forward.off()
    m4_backward.on()

def stop():
    m1_forward.off()
    m1_backward.off()
    m2_forward.off()
    m2_backward.off()
    m3_forward.off()
    m3_backward.off()
    m4_forward.off()
    m4_backward.off()

def disable_servos():
    """Disable servo PWM to allow motor 4 to work"""
    pwm_2.deinit()
    pwm_3.deinit()

def enable_servos():
    """Re-enable servo PWM"""
    global pwm_2, pwm_3
    pwm_2 = PWM(Pin(18))
    pwm_2.freq(50)
    pwm_3 = PWM(Pin(19))
    pwm_3.freq(50)

def check_manual_override():
    if uart.any():
        return uart.readline()
    return None

def timed_sleep_with_override(duration_sec):
    start_time = ticks_ms()
    duration_ms = duration_sec * 1000
    while ticks_diff(ticks_ms(), start_time) < duration_ms:
        cmd = check_manual_override()
        if cmd:
            return cmd
        sleep(0.05)
    return None


def calc_time(dist):
    # Bot moves 50 cm in 1 second, so speed is 50 cm/s
    # Time = Distance / Speed
    return float(dist) / 50.0

def set_speed(new_speed):
    ENA.duty_u16(new_speed)
    ENB.duty_u16(new_speed)
    ENC.duty_u16(new_speed)
    END.duty_u16(new_speed)

#autonomous behavior for red start side
def red_autonomous_behavior():
    forward()
    if timed_sleep_with_override(2):  
        return True
    
    print(calc_time(70))
    
    right()
    if timed_sleep_with_override(1):
        return True

    forward()
    if timed_sleep_with_override(calc_time(73.5)):  
        return True
    
    right()
    if timed_sleep_with_override(1):
        return True
    
    # Reduce speed for final approach
    set_speed(25000)
    
    forward()
    if timed_sleep_with_override(calc_time(10)):
        return True
    
    return False

def CalculateAngle(angle):
   angle = fabs((angle * (6000 / 180)) + 2000)
   angle = round(angle)
   return angle

def alternate_servos_with_override(cycles, delay_sec):
    """Alternate servos between 0 and 90 degrees
    
    Args:
        cycles: Number of complete up/down cycles
        delay_sec: Time to wait at each position
        
    Returns:
        True if manual override detected, False otherwise
    """
    enable_servos()
    m4_forward.off()
    m4_backward.off()
    
    for i in range(cycles):
        # Move to 90 degrees (up position)
        pwm_2.duty_u16(CalculateAngle(0))
        pwm_3.duty_u16(CalculateAngle(180))
        
        if timed_sleep_with_override(delay_sec):
            return True
        
        # Move to 0 degrees (down position)
        pwm_2.duty_u16(CalculateAngle(180))
        pwm_3.duty_u16(CalculateAngle(0))
        
        if timed_sleep_with_override(delay_sec):
            return True
    
    return False

def servo_up():
    enable_servos()
    m4_forward.off()
    m4_backward.off()
    pwm_2.duty_u16(CalculateAngle(0))
    pwm_3.duty_u16(CalculateAngle(180))

def servo_down():
    enable_servos()
    m4_forward.off()
    m4_backward.off()
    pwm_2.duty_u16(CalculateAngle(180))
    pwm_3.duty_u16(CalculateAngle(0))

# ok button configuration
def Start():
    # Wait for button to be pressed (value == 1)
    while Start_Button.value() == 0:
        sleep(0.01)


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
        if red_autonomous_behavior():
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




