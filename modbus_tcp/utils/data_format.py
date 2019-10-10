def isPort(port_str):    
    try:
        port = int(port_str)
    except ValueError:
        return False

    if ((0 > port) or (port > 65535)): return False
    else: return True


def isIpAdress(ip_adress_str):
    ip_split = ip_adress_str.split('.')

    if(len(ip_split) is 4):

        for ip_part in ip_split:

            if (0 > int(ip_part)) or (int(ip_part) > 255):
                return False

        return True

    else:
        return False
