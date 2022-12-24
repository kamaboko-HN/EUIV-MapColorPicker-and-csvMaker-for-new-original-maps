rgb_l = [0, 45, 0]
#rgb_l = [255, 255, 0]

def resetLand():
    global rgb_l
    rgb_l = [0, 45, 0]
    return rgb_l

def pickLand():
    global rgb_l
    if rgb_l == [255, 255, 0]:
        return None
    
    else:
        if rgb_l[1] < 255:
            if rgb_l[0] < 135:
                rgb_l[0] += 15
                
            elif rgb_l[0] >= 135 and rgb_l[0] < 255:
                if rgb_l[2] < 255:
                    rgb_l[2] += 15
                    
                elif rgb_l[2] >= 255:
                    rgb_l[2] = 0
                    rgb_l[0] += 15
                    
            elif rgb_l[0] >= 255:
                rgb_l[0] = 0
                rgb_l[1] += 15
        
        return rgb_l
    
    
    
    
    
        