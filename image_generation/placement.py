"""
Store multiple functions that dictate the placements of 
objects in the picture that are to be called by base.py
"""
import numpy as np
from mathutils import Vector, Quaternion

"""
TWO OBJECTS
"""

thresh_force = 8
    
def right(**kwargs):
    x_1, y_1, r_1, r_2 = kwargs['x_1'], kwargs['y_1'], kwargs['r_1'], kwargs['r_2']
    z_1, z_2 = r_1, r_2
    camera = kwargs['camera']

    quat = camera.matrix_world.to_quaternion()
    inv_quat = Quaternion.inverted(quat)

    x_1_prime, y_1_prime, z_1_prime = inv_quat*Vector([x_1, y_1, z_1])

    x_2_prime = np.random.uniform(low = x_1_prime + 2*r_1, high = 3)
    
    thresh = abs(x_1_prime - x_2_prime)/thresh_force
    
    z_2_prime = np.random.uniform(low = max(-3, z_1_prime - thresh), high = min(3, z_1_prime + thresh))
    #y_2_prime = y_1_prime

    q0, q1, q2, q3 = quat.w, quat.x, quat.y, quat.z
    y_2_prime = (1/(2*(q0*q1 + q2*q3)))*(z_2 - z_2_prime*(q0**2 - q1**2 - q2**2 + q3**2) - 2*x_2_prime*(q1*q3-q0*q2) )

    x_2, y_2, z_2 = quat*Vector([x_2_prime, y_2_prime, z_2_prime])

    return x_2, y_2, z_2

def left(**kwargs):
    x_1, y_1, r_1, r_2 = kwargs['x_1'], kwargs['y_1'], kwargs['r_1'], kwargs['r_2']
    z_1, z_2 = r_1, r_2
    camera = kwargs['camera']

    quat = camera.matrix_world.to_quaternion()
    inv_quat = Quaternion.inverted(quat)

    x_1_prime, y_1_prime, z_1_prime = inv_quat*Vector([x_1, y_1, z_1])

    x_2_prime = np.random.uniform(low = -3, high = x_1_prime - 2*r_1)
    
    thresh = abs(x_1_prime - x_2_prime)/thresh_force
    
    z_2_prime = np.random.uniform(low = max(-3, z_1_prime - thresh), high = min(3, z_1_prime + thresh))
    #y_2_prime = y_1_prime

    q0, q1, q2, q3 = quat.w, quat.x, quat.y, quat.z
    y_2_prime = (1/(2*(q0*q1 + q2*q3)))*(z_2 - z_2_prime*(q0**2 - q1**2 - q2**2 + q3**2) - 2*x_2_prime*(q1*q3-q0*q2) )

    x_2, y_2, z_2 = quat*Vector([x_2_prime, y_2_prime, z_2_prime])

    return x_2, y_2, z_2

def front(**kwargs):
    x_1, y_1, r_1, r_2 = kwargs['x_1'], kwargs['y_1'], kwargs['r_1'], kwargs['r_2']
    z_1, z_2 = r_1, r_2
    camera = kwargs['camera']

    quat = camera.matrix_world.to_quaternion()
    inv_quat = Quaternion.inverted(quat)

    x_1_prime, y_1_prime, z_1_prime = inv_quat*Vector([x_1, y_1, z_1])

    z_2_prime = np.random.uniform(low = z_1_prime + 2*r_1, high = 3)
    
    thresh = abs(z_1_prime - z_2_prime)/thresh_force
    
    x_2_prime = np.random.uniform(low = max(-3, x_1_prime - thresh), high = min(3, x_1_prime + thresh))
    #y_2_prime = y_1_prime

    q0, q1, q2, q3 = quat.w, quat.x, quat.y, quat.z
    y_2_prime = (1/(2*(q0*q1 + q2*q3)))*(z_2 - z_2_prime*(q0**2 - q1**2 - q2**2 + q3**2) - 2*x_2_prime*(q1*q3-q0*q2) )

    x_2, y_2, z_2 = quat*Vector([x_2_prime, y_2_prime, z_2_prime])

    return x_2, y_2, z_2

def behind(**kwargs):
    x_1, y_1, r_1, r_2 = kwargs['x_1'], kwargs['y_1'], kwargs['r_1'], kwargs['r_2']
    z_1, z_2 = r_1, r_2
    camera = kwargs['camera']

    quat = camera.matrix_world.to_quaternion()
    inv_quat = Quaternion.inverted(quat)

    x_1_prime, y_1_prime, z_1_prime = inv_quat*Vector([x_1, y_1, z_1])

    z_2_prime = np.random.uniform(low = -3, high = z_1_prime - 2*r_1)
    
    thresh = abs(z_1_prime - z_2_prime)/thresh_force
    
    x_2_prime = np.random.uniform(low = max(-3, x_1_prime - thresh), high = min(3, x_1_prime + thresh) )
    #y_2_prime = y_1_prime

    q0, q1, q2, q3 = quat.w, quat.x, quat.y, quat.z
    y_2_prime = (1/(2*(q0*q1 + q2*q3)))*(z_2 - z_2_prime*(q0**2 - q1**2 - q2**2 + q3**2) - 2*x_2_prime*(q1*q3-q0*q2) )

    x_2, y_2, z_2 = quat*Vector([x_2_prime, y_2_prime, z_2_prime])

    return x_2, y_2, z_2

def con(**kwargs):
    x_1, y_1, r_1, r_2 = kwargs['x_1'], kwargs['y_1'], kwargs['r_1'], kwargs['r_2']
    z_1, z_2 = r_1, r_2
    camera = kwargs['camera']

    x_2, y_2 = x_1, y_1
    z_2 = 2*z_1 + r_2

    return x_2, y_2, z_2

def cright(**kwargs):
    x_1, y_1, r_1, r_2 = kwargs['x_1'], kwargs['y_1'], kwargs['r_1'], kwargs['r_2']
    z_1, z_2 = r_1, r_2
    camera = kwargs['camera']

    quat = camera.matrix_world.to_quaternion()
    inv_quat = Quaternion.inverted(quat)

    x_1_prime, y_1_prime, z_1_prime = inv_quat*Vector([x_1, y_1, z_1])

    x_2_prime = x_1_prime  + r_2 + r_1

    q0, q1, q2, q3 = quat.w, quat.x, quat.y, quat.z

    z_2_prime = z_1_prime
    #z_2_prime = (1/(2*(q2*q3 - q0*q1) - ((q0**2 - q1**2 + q2**2 - q3**2)*(q0**2 - q1**2 - q2**2 + q3**2))/(2*(q0*q1 + q2*q3)) ))*( y_1 
    #    - 2*x_2_prime*(q0*q3 + q1*q2) - ((q0**2 - q1**2 + q2**2 - q3**2)/(2*(q0*q1 + q2*q3)))*(z_1 - 2*x_2_prime*(q1*q3 - q0*q2)) )
    y_2_prime = (1/(2*(q0*q1 + q2*q3)))*(z_2 - z_2_prime*(q0**2 - q1**2 - q2**2 + q3**2) - 2*x_2_prime*(q1*q3-q0*q2) )
    
    x_2, y_2, z_2 = quat*Vector([x_2_prime, y_2_prime, z_2_prime])

    return x_2, y_2, z_2

def cleft(**kwargs):
    x_1, y_1, r_1, r_2 = kwargs['x_1'], kwargs['y_1'], kwargs['r_1'], kwargs['r_2']
    z_1, z_2 = r_1, r_2
    camera = kwargs['camera']

    quat = camera.matrix_world.to_quaternion()
    inv_quat = Quaternion.inverted(quat)

    x_1_prime, y_1_prime, z_1_prime = inv_quat*Vector([x_1, y_1, z_1])

    x_2_prime = x_1_prime  - r_2 - r_1

    q0, q1, q2, q3 = quat.w, quat.x, quat.y, quat.z

    z_2_prime = z_1_prime
    #z_2_prime = (1/(2*(q2*q3 - q0*q1) - ((q0**2 - q1**2 + q2**2 - q3**2)*(q0**2 - q1**2 - q2**2 + q3**2))/(2*(q0*q1 + q2*q3)) ))*( y_1 
    #    - 2*x_2_prime*(q0*q3 + q1*q2) - ((q0**2 - q1**2 + q2**2 - q3**2)/(2*(q0*q1 + q2*q3)))*(z_1 - 2*x_2_prime*(q1*q3 - q0*q2)) )
    y_2_prime = (1/(2*(q0*q1 + q2*q3)))*(z_2 - z_2_prime*(q0**2 - q1**2 - q2**2 + q3**2) - 2*x_2_prime*(q1*q3-q0*q2) )
    
    x_2, y_2, z_2 = quat*Vector([x_2_prime, y_2_prime, z_2_prime])

    return x_2, y_2, z_2


    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    