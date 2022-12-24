rgb_b = [0, 0, 255] #R G B

def resetSea():
    global rgb_b
    rgb_b = [0, 0, 255]
    return rgb_b

def pickBlue():
    if rgb_b == [90, 255, 180]:
        return None
    
    else:
        if rgb_b[1] >= 255:
            rgb_b[1] = 0
            if rgb_b[0] < 90:
                rgb_b[0] += 15
            elif rgb_b[0] >= 90:
                if rgb_b[2] >= 180:
                    rgb_b[2] -= 15
        rgb_b[1] += 15
        return rgb_b


