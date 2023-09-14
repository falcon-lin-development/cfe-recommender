def is_power_of(number, base):
    if number < base:
        return number == 1
    
    return is_power_of(number / base, base)