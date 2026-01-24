import math

def get_arrow_direction_attacker(colors, activeColor_attacker):
    # Helper to check if any in range is active
    def is_active(start, end):
        return any(colors[i] == activeColor_attacker for i in range(start, end+1))

    # Diagonal directions

    if is_active(28, 31) and is_active(36, 39):
        return (2, 2)  # --> up right

    if is_active(24, 27) and is_active(32, 35):
        return (-2, -2) # --> down left

    if is_active(24, 27) and is_active(36, 39):
        return (-2, 2) # --> up left

    if is_active(28, 35):
        return (2, -2) # --> down right

    # Cardinal directions
    if is_active(28, 31):
        return (2, 0)  # --> right
    if is_active(36, 39):
        return (0, 2)  # --> up
    if is_active(24, 27):
        return (-2, 0) # --> left
    if is_active(32, 35):
        return (0, -2) # --> down
    return None




def get_arrow_direction_defender(colors, activeColor_defender, xBall, yBall, coordinates):
    active_positions = [
        (x, y)
        for i, (label, (x, y)) in enumerate(coordinates)
        if colors[i] == activeColor_defender
    ]

    
    if not active_positions:
        return
    
    xs = [p[0] for p in active_positions]
    ys = [p[1] for p in active_positions]
    
    centroid_x = sum(xs) / len(xs)
    centroid_y = sum(ys) / len(ys)

    left_group = []
    right_group = []
    
    for x, y in active_positions:
        if x > centroid_x:
            right_group.append((x, y))
        else:
            left_group.append((x, y))

    if not left_group or not right_group:
        dx = centroid_x
        dy = centroid_y
    else:
        lx = sum(x for x, y in left_group) / len(left_group)
        ly = sum(y for x, y in left_group) / len(left_group)
        rx = sum(x for x, y in right_group) / len(right_group)
        ry = sum(y for x, y in right_group) / len(right_group)

        dx = lx - rx
        dy = ly - ry


    angle = 90.0

    angle_rad = math.atan2(dy, dx)
    angle = angle_rad * 180.0 / math.pi
    
    if(angle < 0):
        angle += 360.0

   
    if(angle > 180.0):
        angle -= 180.0
        

    if((angle <= 20 and angle >= 0) or (angle <= 180 and angle >= 160)):
        dx = xBall
    elif((angle <= 120 and angle >= 70) or (angle <= 65 and angle >= 46) and yBall > 0):
        dx = 0
        dy = 100
    elif (angle <= 18 and angle >= 49 and yBall < 0 and xBall > 0):
        dx = -25
        dy = -50
    elif (angle <= 45 and angle >= 20 and yBall > 0):
        dy = 120
    elif (angle <= 160 and angle >= 135):
        dx = -100
    else:
        dx = 0
        
    yBorder = 1.5; 

    for i in range(23):
        if((angle <= 20 and angle >= 0) or (angle <= 180 and angle >= 160)):
            if(colors[i] == activeColor_defender and coordinates[i][1][1] > yBorder):
                dy = 100
                dx = 0
                break
            elif(colors[i] == activeColor_defender and coordinates[i][1][1] < -yBorder):
                dy = -100
                dx = 0
                break
            else:
                pass
            
    magnitude = math.sqrt(dx**2 + dy**2)
    if magnitude == 0:
        return None
    unit_dx = dx / magnitude
    unit_dy = dy / magnitude
    return (unit_dx, unit_dy)