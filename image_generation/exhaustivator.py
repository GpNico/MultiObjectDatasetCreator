"""
Store multiple functions that dictate the placements of 
objects in the picture that are to be called by base.py
"""
import numpy as np
from mathutils import Vector, Quaternion

def is_right(x_1, y_1, z_1, x_2, y_2, z_2, camera, r_1, r_2, *args):
    quat = camera.matrix_world.to_quaternion()
    inv_quat = Quaternion.inverted(quat)

    x_1_prime, y_1_prime, z_1_prime = inv_quat*Vector([x_1, y_1, z_1])
    x_2_prime, y_2_prime, z_2_prime = inv_quat*Vector([x_2, y_2, z_2])

    tresh = abs(x_1_prime - x_2_prime)/4
    return (x_1_prime > x_2_prime) and ( abs(z_1_prime - z_2_prime) < tresh) and abs(r_1 - z_1) < tresh and abs(r_2 - z_2) < tresh

def is_left(x_1, y_1, z_1, x_2, y_2, z_2, camera, r_1, r_2, *args):
    quat = camera.matrix_world.to_quaternion()
    inv_quat = Quaternion.inverted(quat)

    x_1_prime, y_1_prime, z_1_prime = inv_quat*Vector([x_1, y_1, z_1])
    x_2_prime, y_2_prime, z_2_prime = inv_quat*Vector([x_2, y_2, z_2])

    tresh = abs(x_1_prime - x_2_prime)/4
    return (x_1_prime < x_2_prime) and ( abs(z_1_prime - z_2_prime) < tresh) and abs(r_1 - z_1) < tresh and abs(r_2 - z_2) < tresh

def is_front(x_1, y_1, z_1, x_2, y_2, z_2, camera, r_1, r_2, *args):
    quat = camera.matrix_world.to_quaternion()
    inv_quat = Quaternion.inverted(quat)

    x_1_prime, y_1_prime, z_1_prime = inv_quat*Vector([x_1, y_1, z_1])
    x_2_prime, y_2_prime, z_2_prime = inv_quat*Vector([x_2, y_2, z_2])

    tresh = abs(z_1_prime - z_2_prime)/4
    return (z_1_prime > z_2_prime) and ( abs(x_1_prime - x_2_prime) < tresh) and abs(r_1 - z_1) < tresh and abs(r_2 - z_2) < tresh

def is_behind(x_1, y_1, z_1, x_2, y_2, z_2, camera, r_1, r_2, *args):
    quat = camera.matrix_world.to_quaternion()
    inv_quat = Quaternion.inverted(quat)

    x_1_prime, y_1_prime, z_1_prime = inv_quat*Vector([x_1, y_1, z_1])
    x_2_prime, y_2_prime, z_2_prime = inv_quat*Vector([x_2, y_2, z_2])

    tresh = abs(z_1_prime - z_2_prime)/4
    return (z_1_prime < z_2_prime) and ( abs(x_1_prime - x_2_prime) < tresh) and abs(r_1 - z_1) < tresh and abs(r_2 - z_2) < tresh

def is_contact_on(x_1, y_1, z_1, x_2, y_2, z_2, camera, r_1, r_2, *args):

    tresh = 0.05

    return abs(x_1 - x_2) < tresh and abs(y_1 - y_2) < tresh and abs(z_1 - (2*r_2 + r_1)) < tresh

def is_contact_below(x_1, y_1, z_1, x_2, y_2, z_2, camera, r_1, r_2, *args):

    tresh = 0.05

    return abs(x_1 - x_2) < tresh and abs(y_1 - y_2) < tresh and abs(z_2 - (2*r_1 + r_2)) < tresh

def is_contact_right(x_1, y_1, z_1, x_2, y_2, z_2, camera, r_1, r_2, *args):

    quat = camera.matrix_world.to_quaternion()
    inv_quat = Quaternion.inverted(quat)

    x_1_prime, y_1_prime, z_1_prime = inv_quat*Vector([x_1, y_1, z_1])
    x_2_prime, y_2_prime, z_2_prime = inv_quat*Vector([x_2, y_2, z_2])

    tresh = 0.05

    return abs(x_2_prime - (x_1_prime  - r_2 - r_1) ) < tresh and abs(z_1_prime - z_2_prime) < tresh and abs(r_1 - z_1) < tresh and abs(r_2 - z_2) < tresh

def is_contact_left(x_1, y_1, z_1, x_2, y_2, z_2, camera, r_1, r_2, *args):

    quat = camera.matrix_world.to_quaternion()
    inv_quat = Quaternion.inverted(quat)

    x_1_prime, y_1_prime, z_1_prime = inv_quat*Vector([x_1, y_1, z_1])
    x_2_prime, y_2_prime, z_2_prime = inv_quat*Vector([x_2, y_2, z_2])

    tresh = 0.05

    return abs(x_2_prime - (x_1_prime  + r_2 + r_1) ) < tresh and abs(z_1_prime - z_2_prime) < tresh and abs(r_1 - z_1) < tresh and abs(r_2 - z_2) < tresh

class Exhaustivator:

    def __init__(self, count_rela):

        rela_created = list(count_rela.keys())

        self.rela_checkers, self.rela_names = [], []
        if 'right' in rela_created:
            self.rela_checkers.append(is_right)
            self.rela_names.append('right')
        if 'left' in rela_created:
            self.rela_checkers.append(is_left)
            self.rela_names.append('left')
        if 'front' in rela_created:
            self.rela_checkers.append(is_front)
            self.rela_names.append('front')
        if 'behind' in rela_created:
            self.rela_checkers.append(is_behind)
            self.rela_names.append('behind')
        if 'contact_on' in rela_created:
            self.rela_checkers.append(is_contact_on)
            self.rela_names.append('contact_on')
        if 'contact_below' in rela_created:
            self.rela_checkers.append(is_contact_below)
            self.rela_names.append('contact_below')
        if 'contact_right' in rela_created:
            self.rela_checkers.append(is_contact_right)
            self.rela_names.append('contact_right')
        if 'contact_left' in rela_created:
            self.rela_checkers.append(is_contact_left)
            self.rela_names.append('contact_left')

        self.rela_count = {k: 0 for k in count_rela.keys()}


    def exhaustivate(self, coords, scales, counts_rela, camera):
        coords = np.array(coords)
        N, dim = coords.shape
        assert dim == 3
    
        Y = np.zeros((N,N,len(self.rela_checkers)))

        for i in range(N):
            x_1, y_1, z_1 = coords[i]
            r_1 = scales[i]
            for j in range(i):
                x_2, y_2, z_2 = coords[j]
                r_2 = scales[j]
                for k in range(len(self.rela_checkers)):
                    rela_checker = self.rela_checkers[k]
                    is_rela = rela_checker(x_1, y_1, z_1, x_2, y_2, z_2, camera, r_1, r_2)
                    if is_rela:
                        Y[i,j][k] = 1
                        self.rela_count[self.rela_names[k]] += 1
                        counts_rela[self.rela_names[k]] -= 1
                    is_rela = rela_checker(x_2, y_2, z_2, x_1, y_1, z_1, camera, r_2, r_1)
                    if is_rela:
                        Y[j,i][k] = 1
                        self.rela_count[self.rela_names[k]] += 1
                        counts_rela[self.rela_names[k]] -= 1
                    
        return Y, counts_rela    
    
    
    
    
    
    
    
    
    
    
    
    
    