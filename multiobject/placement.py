"""
Store multiple functions that dictate the placements of 
objects in the picture that are to be called by base.py
"""
import numpy as np
from utils.utilitary_functions import collide

"""
TWO OBJECTS
"""

thresh_force = 2

def random(**kwargs):
    r_1, c_1, obj_size_1, obj_size_2, x_shape = kwargs['r_1'], kwargs['c_1'], kwargs['obj_size_1'], kwargs['obj_size_2'], kwargs['x_shape']
    r_2 = np.random.randint(x_shape[0] - obj_size_2[0] + 1)
    c_2 = np.random.randint(x_shape[1] - obj_size_2[1] + 1)
    return r_2, c_2
    
def below(**kwargs):
    r_1, c_1, obj_size_1, obj_size_2, x_shape = kwargs['r_1'], kwargs['c_1'], kwargs['obj_size_1'], kwargs['obj_size_2'], kwargs['x_shape']
    r_2 = np.random.randint(low = r_1 + obj_size_1[0], high = x_shape[0] - obj_size_2[0] + 1)
    
    thresh = abs(r_1 - r_2)//thresh_force
    
    c_2 = np.random.randint(low = max(0, c_1 - thresh) , high = min(c_1 + thresh, x_shape[1] - obj_size_2[1]) + 1)
    
    return r_2, c_2
    
def top(**kwargs):
    r_1, c_1, obj_size_1, obj_size_2, x_shape = kwargs['r_1'], kwargs['c_1'], kwargs['obj_size_1'], kwargs['obj_size_2'], kwargs['x_shape']
    r_2 = np.random.randint(r_1 - obj_size_1[0])
    
    thresh = abs(r_1 - r_2)//thresh_force
    
    c_2 = np.random.randint(low = max(0, c_1 - thresh) , high = min(c_1 + thresh, x_shape[1] - obj_size_2[1]) + 1)
    
    return r_2, c_2
    
def right(**kwargs):
    r_1, c_1, obj_size_1, obj_size_2, x_shape = kwargs['r_1'], kwargs['c_1'], kwargs['obj_size_1'], kwargs['obj_size_2'], kwargs['x_shape']
    c_2 = np.random.randint(low = c_1 + obj_size_1[1], high = x_shape[1] - obj_size_2[1] + 1)
    
    thresh = abs(c_1 - c_2)//thresh_force
    
    r_2 = np.random.randint(low = max(0, r_1 - thresh), high = min(x_shape[0] - obj_size_2[0], r_1 + thresh) + 1)
    
    return r_2, c_2
    
def left(**kwargs):
    r_1, c_1, obj_size_1, obj_size_2, x_shape = kwargs['r_1'], kwargs['c_1'], kwargs['obj_size_1'], kwargs['obj_size_2'], kwargs['x_shape']
    
    c_2 = np.random.randint(max(0,c_1 - obj_size_1[1]))
    
    thresh = abs(c_1 - c_2)//thresh_force
    
    r_2 = np.random.randint(low = max(0, r_1 - thresh), high = min(x_shape[0] - obj_size_2[0], r_1 + thresh) + 1)
    
    return r_2, c_2
    
def right_and_top(**kwargs):
    r_1, c_1, obj_size_1, obj_size_2, x_shape = kwargs['r_1'], kwargs['c_1'], kwargs['obj_size_1'], kwargs['obj_size_2'], kwargs['x_shape']
    
    c_2 = np.random.randint(low = c_1 + obj_size_1[1], high = x_shape[1] - obj_size_2[1] + 1)
    r_2 = np.random.randint(r_1 - obj_size_1[0])
    
    return r_2, c_2
    


###########
# CONTACT #
###########

def cright(**kwargs):
    r_1, c_1, obj_size_1, obj_size_2, x_shape = kwargs['r_1'], kwargs['c_1'], kwargs['obj_size_1'], kwargs['obj_size_2'], kwargs['x_shape']
    vertices1, vertices2 = kwargs['vertices1'].copy(), kwargs['vertices2'].copy()

    c_2 = c_1 + obj_size_2[1]//2
    r_2 = np.random.randint(low = r_1 - obj_size_1[0]//4, high = r_1 + obj_size_1[0]//4)

    #adjust coordinates
    vertices1 += np.array([r_1, c_1])
    vertices2 += np.array([r_2, c_2])

    collide_bool, MPV = collide(vertices2, vertices1)

    if collide_bool:
        MPV_unit = MPV/np.linalg.norm(MPV)

        r_2 += MPV[0] - 2*MPV_unit[0]
        c_2 += MPV[1] - 2*MPV_unit[1]

        r_2 = int(r_2)
        c_2 = int(c_2)

    tresh = abs(c_1 - c_2)/2
    is_still_right = (c_1 < c_2) and ( abs(r_1 - r_2) < tresh)
    if is_still_right:
        return r_2, c_2
    else:
        raise Exception('Object Not Right !')
    
def cleft(**kwargs):
    r_1, c_1, obj_size_1, obj_size_2, x_shape = kwargs['r_1'], kwargs['c_1'], kwargs['obj_size_1'], kwargs['obj_size_2'], kwargs['x_shape']
    vertices1, vertices2 = kwargs['vertices1'].copy(), kwargs['vertices2'].copy()
    
    c_2 = c_1 - obj_size_1[1]//2
    r_2 = np.random.randint(low = r_1 - obj_size_1[0]//4, high = r_1 + obj_size_1[0]//4)

    #adjust coordinates
    vertices1 += np.array([r_1, c_1])
    vertices2 += np.array([r_2, c_2])

    collide_bool, MPV = collide(vertices2, vertices1)

    if collide_bool:
        MPV_unit = MPV/np.linalg.norm(MPV)

        r_2 += MPV[0] - 2*MPV_unit[0]
        c_2 += MPV[1] - 2*MPV_unit[1]

        r_2 = int(r_2)
        c_2 = int(c_2)
    
    tresh = abs(c_1 - c_2)/2
    is_still_left = (c_2 < c_1) and ( abs(r_1 - r_2) < tresh)
    if is_still_left:
        return r_2, c_2
    else:
        raise Exception('Object Not Left !')
    
def con(**kwargs):
    r_1, c_1, obj_size_1, obj_size_2, x_shape = kwargs['r_1'], kwargs['c_1'], kwargs['obj_size_1'], kwargs['obj_size_2'], kwargs['x_shape']
    vertices1, vertices2 = kwargs['vertices1'].copy(), kwargs['vertices2'].copy()
    
    c_2 = c_1
    r_2 = r_1 - obj_size_1[0]//4

    #adjust coordinates
    vertices1 += np.array([r_1, c_1])
    vertices2 += np.array([r_2, c_2])

    collide_bool, MPV = collide(vertices2, vertices1)

    if collide_bool:
        MPV_unit = MPV/np.linalg.norm(MPV)

        r_2 += MPV[0] - 2*MPV_unit[0]
        c_2 += MPV[1] - 2*MPV_unit[1]

        r_2 = int(r_2)
        c_2 = int(c_2)
    
    tresh = abs(r_1 - r_2)/2
    is_still_top = (r_1 > r_2) and ( abs(c_1 - c_2) < tresh)
    if is_still_top:
        return r_2, c_2
    else:
        raise Exception('Object Not top !')

def cbelow(**kwargs):
    r_1, c_1, obj_size_1, obj_size_2, x_shape = kwargs['r_1'], kwargs['c_1'], kwargs['obj_size_1'], kwargs['obj_size_2'], kwargs['x_shape']
    vertices1, vertices2 = kwargs['vertices1'].copy(), kwargs['vertices2'].copy()
    
    c_2 = c_1
    r_2 = r_1 + obj_size_1[0]//4

    #adjust coordinates
    vertices1 += np.array([r_1, c_1])
    vertices2 += np.array([r_2, c_2])

    collide_bool, MPV = collide(vertices2, vertices1)

    if collide_bool:
        MPV_unit = MPV/np.linalg.norm(MPV)

        r_2 += MPV[0] - 2*MPV_unit[0]
        c_2 += MPV[1] - 2*MPV_unit[1]

        r_2 = int(r_2)
        c_2 = int(c_2)

    tresh = abs(r_1 - r_2)/2
    is_still_below = (r_2 > r_1) and ( abs(c_1 - c_2) < tresh)
    if is_still_below:
        return r_2, c_2
    else:
        raise Exception('Object Not Below !')
    




"""
THREE OBJECTS
"""

def aligned(**kwargs):
    r_1, c_1, obj_size_1, obj_size_2, x_shape = kwargs['r_1'], kwargs['c_1'], kwargs['obj_size_1'], kwargs['obj_size_2'], kwargs['x_shape']
    r_2, c_2, obj_size_3 = kwargs['r_2'], kwargs['c_2'], kwargs['obj_size_3']
    
    a = (r_1 - r_2)/(c_1 - c_2)
    b = r_1 - a*c_1
    
    c_M, c_m = max(c_1, c_2), min(c_1, c_2)
    r_M, r_m = max(r_1, r_2), min(r_1, r_2)
    
    #c_3 = np.random.randint(low = c_m, high = c_M + 1)
    c_3 = np.random.randint(x_shape[1] - obj_size_3[1] + 1)
    
    r_3_theo = a*c_3 + b
    
    thresh = (r_M - r_m)//8
    
    r_3 = np.random.randint(low = int(r_3_theo - thresh), high = int(r_3_theo + thresh) + 1)
    
    return r_3, c_3
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    