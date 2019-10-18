def relay_states_registar_value(relay_states):
    num = 0
    n = 8
    for relay_state in relay_states:
        if relay_state:
            num += 2**n
        
        n += 1

    return num

def relay_states_from_register_value(value):
    relay_states = []
    num = value

    for i in range(11, 7, -1):
        if num >= 2**i:
            num -= 2**i
            relay_states.append(1)
        else:
            relay_states.append(0)

    return relay_states
