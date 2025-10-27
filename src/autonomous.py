from src.utils import custom_set_speed, forward, calc_time, timed_sleep_with_override, right, left, set_speed, backward

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
