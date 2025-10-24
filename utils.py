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
m4_forward = Pin(19,Pin.OUT)
m4_backward = Pin(18,Pin.OUT)
END = PWM(Pin(21))

#servo motors
# Don't initialize servo_2 and servo_3 at startup - they share pins with motor 4
servo_2 = None
servo_3 = None

servo_1 = PWM(Pin(28))
servo_1.freq(50)

Start_Button = Pin(2,Pin.IN, Pin.PULL_UP)

uart = UART(0, 9600)

def set_speed(new_speed):
    ENA.duty_u16(new_speed)
    ENB.duty_u16(new_speed)
    ENC.duty_u16(new_speed)
    END.duty_u16(new_speed)

def custom_set_speed():
    ENA.duty_u16(40000)
    ENB.duty_u16(45000)
    ENC.duty_u16(40000)
    END.duty_u16(45000)

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
    global servo_2, servo_3
    try:
        if servo_2:
            servo_2.deinit()
    except:
        pass
    try:
        if servo_3:
            servo_3.deinit()
    except:
        pass
    servo_2 = None
    servo_3 = None

def enable_servos():
    """Re-enable servo PWM"""
    global servo_2, servo_3
    try:
        if servo_2:
            servo_2.deinit()
        if servo_3:
            servo_3.deinit()
    except:
        pass
    
    servo_2 = PWM(Pin(18))
    servo_2.freq(50)
    servo_3 = PWM(Pin(19))
    servo_3.freq(50)

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
    # Bot moves 40.5 cm in 1 second, so speed is 40.5 cm/s
    # Time = Distance / Speed
    return 1.8*(float(dist) / 40.5)


#autonomous behavior for red start side
def red_autonomous_behavior():
    custom_set_speed()
    forward()
    if timed_sleep_with_override(calc_time(67)):
        return True
    
    right()
    if timed_sleep_with_override(0.89):
        return True

    forward()
    if timed_sleep_with_override(calc_time(76)):  
        return True
    
    left()
    if timed_sleep_with_override(1):
        return True

    # Reduce speed for final approach
    set_speed(25000)
    
    backward()
    if timed_sleep_with_override(3):
        return True
    
    # Restore original speed after autonomous completes
    set_speed(65000)
    
    return False

#autonomous behavior for blue start side
def blue_autonomous_behavior():
    custom_set_speed()
    forward()
    if timed_sleep_with_override(calc_time(45)):
        return True
    
    right()
    if timed_sleep_with_override(0.89):
        return True

    forward()
    if timed_sleep_with_override(calc_time(61)):  
        return True
    
    left()
    if timed_sleep_with_override(1):
        return True

    # Reduce speed for final approach
    set_speed(25000)
    
    backward()
    if timed_sleep_with_override(3):
        return True
    
    # Restore original speed after autonomous completes
    set_speed(65000)
    
    return False

def CalculateAngle(angle):
   angle = fabs((angle * (6000 / 180)) + 2000)
   angle = round(angle)
   return angle

def reinitialize_motor4():
    """Reinitialize motor 4 pins after servo use"""
    global m4_forward, m4_backward
    m4_forward = Pin(18, Pin.OUT)
    m4_backward = Pin(19, Pin.OUT)
    m4_forward.off()
    m4_backward.off()

def servo_up():
    # Stop motor 4 first
    m4_forward.off()
    m4_backward.off()
    sleep(0.1)  # Brief delay to ensure pins are free
    
    # Create fresh PWM objects
    try:
        servo2 = PWM(Pin(18))
        servo2.freq(50)
        servo3 = PWM(Pin(19))
        servo3.freq(50)
        
        # Move servos
        servo2.duty_u16(CalculateAngle(0))
        servo3.duty_u16(CalculateAngle(180))
        sleep(0.5)  # Give servo time to reach position
        
        # Clean up
        servo2.deinit()
        servo3.deinit()
    except Exception as e:
        print(f"Servo error: {e}")
    
    # Reinitialize motor 4 pins for digital output
    reinitialize_motor4()

def servo_down():
    # Stop motor 4 first
    m4_forward.off()
    m4_backward.off()
    sleep(0.1)  # Brief delay to ensure pins are free
    
    # Create fresh PWM objects
    try:
        servo2 = PWM(Pin(18))
        servo2.freq(50)
        servo3 = PWM(Pin(19))
        servo3.freq(50)
        
        # Move servos
        servo2.duty_u16(CalculateAngle(180))
        servo3.duty_u16(CalculateAngle(0))
        sleep(0.5)  # Give servo time to reach position
        
        # Clean up
        servo2.deinit()
        servo3.deinit()
    except Exception as e:
        print(f"Servo error: {e}")
    
    # Reinitialize motor 4 pins for digital output
    reinitialize_motor4()

def alternate_servos_with_override(cycles, delay_sec):
    """Alternate servos between 0 and 90 degrees
    
    Args:
        cycles: Number of complete up/down cycles
        delay_sec: Time to wait at each position
        
    Returns:
        True if manual override detected, False otherwise
    """
    m4_forward.off()
    m4_backward.off()
    sleep(0.1)
    
    try:
        servo2 = PWM(Pin(18))
        servo2.freq(50)
        servo3 = PWM(Pin(19))
        servo3.freq(50)
        
        for i in range(cycles):
            # Move to up position
            servo2.duty_u16(CalculateAngle(0))
            servo3.duty_u16(CalculateAngle(180))
            
            if timed_sleep_with_override(delay_sec):
                servo2.deinit()
                servo3.deinit()
                reinitialize_motor4()
                return True
            
            # Move to down position
            servo2.duty_u16(CalculateAngle(180))
            servo3.duty_u16(CalculateAngle(0))
            
            if timed_sleep_with_override(delay_sec):
                servo2.deinit()
                servo3.deinit()
                reinitialize_motor4()
                return True
        
        servo2.deinit()
        servo3.deinit()
    except Exception as e:
        print(f"Servo error: {e}")
    
    # Reinitialize motor 4 pins for digital output
    reinitialize_motor4()
    return False

def servo_open():
    """Open the lifting mechanism using servo 1"""
    servo_1.duty_u16(CalculateAngle(0))  # Open position
    sleep(0.5)  # Give servo time to reach position

def servo_close():
    """Close the lifting mechanism using servo 1"""
    servo_1.duty_u16(CalculateAngle(180))  # Close position
    sleep(0.5)  # Give servo time to reach position

# ok button configuration
def Start():
    # Wait for button to be pressed (value == 1)
    while Start_Button.value() == 0:
        sleep(0.01)