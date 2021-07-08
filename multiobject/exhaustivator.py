"""
Store multiple functions that dictate the placements of 
objects in the picture that are to be called by base.py
"""
import numpy as np
from utils.utilitary_functions import collide
from utils import get_rela_code

rela_code = get_rela_code()

def is_right(r_1, c_1, r_2, c_2, *args):
    tresh = abs(c_1 - c_2)/2
    return (c_1 > c_2) and ( abs(r_1 - r_2) < tresh), rela_code['right']

def is_left(r_1, c_1, r_2, c_2, *args):
    tresh = abs(c_1 - c_2)/2
    return (c_1 < c_2) and ( abs(r_1 - r_2) < tresh), rela_code['left']

def is_top(r_1, c_1, r_2, c_2, *args):
    tresh = abs(r_1 - r_2)/2
    return (r_1 < r_2) and ( abs(c_1 - c_2) < tresh), rela_code['top']
    
def is_below(r_1, c_1, r_2, c_2, *args):
    tresh = abs(r_1 - r_2)/2
    return (r_1  > r_2) and ( abs(c_1 - c_2) < tresh), rela_code['below']

def is_contact_right(r_1, c_1, r_2, c_2, vertices1, vertices2):
    tresh = abs(c_1 - c_2)/2
    is_right_bool = (c_1 > c_2) and ( abs(r_1 - r_2) < tresh)
    vert1 = vertices1.copy() +  np.array([r_1,c_1])
    vert2 = vertices2.copy() + np.array([r_2,c_2])

    collide_bool, _ = collide(vert1, vert2)

    return is_right_bool and collide_bool, rela_code['contact_right']

def is_contact_left(r_1, c_1, r_2, c_2, vertices1, vertices2):
    tresh = abs(c_1 - c_2)/2
    is_left_bool = (c_1 < c_2) and ( abs(r_1 - r_2) < tresh)
    vert1 = vertices1.copy() + np.array([r_1,c_1])
    vert2 = vertices2.copy() + np.array([r_2,c_2])

    collide_bool, _ = collide(vert1, vert2)

    return is_left_bool and collide_bool, rela_code['contact_left']

def is_contact_on(r_1, c_1, r_2, c_2, vertices1, vertices2):
    tresh = abs(r_1 - r_2)/2
    is_on_bool = (r_1 < r_2) and ( abs(c_1 - c_2) < tresh)
    vert1 = vertices1.copy() + np.array([r_1,c_1])
    vert2 = vertices2.copy() + np.array([r_2,c_2])

    collide_bool, _ = collide(vert1, vert2)

    return is_on_bool and collide_bool, rela_code['contact_on']

def is_contact_below(r_1, c_1, r_2, c_2, vertices1, vertices2):
    tresh = abs(r_1 - r_2)/2
    is_below_bool = (r_1 > r_2) and ( abs(c_1 - c_2) < tresh)
    vert1 = vertices1.copy() + np.array([r_1,c_1])
    vert2 = vertices2.copy() +  np.array([r_2,c_2])

    collide_bool, _ = collide(vert1, vert2)

    return is_below_bool and collide_bool, rela_code['contact_below']


class Exhaustivator:

    def __init__(self, count_rela, shape):

        self.shape = shape[:2]

        rela_created = list(count_rela.keys())
        self.rela_checkers, self.rela_names = [], []
        if 'right' in rela_created:
            self.rela_checkers.append(is_right)
            self.rela_names.append('right')
        if 'left' in rela_created:
            self.rela_checkers.append(is_left)
            self.rela_names.append('left')
        if 'top' in rela_created:
            self.rela_checkers.append(is_top)
            self.rela_names.append('top')
        if 'below' in rela_created:
            self.rela_checkers.append(is_below)
            self.rela_names.append('below')
        if 'contact_right' in rela_created:
            self.rela_checkers.append(is_contact_right)
            self.rela_names.append('contact_right')
        if 'contact_left' in rela_created:
            self.rela_checkers.append(is_contact_left)
            self.rela_names.append('contact_left')
        if 'contact_on' in rela_created:
            self.rela_checkers.append(is_contact_on)
            self.rela_names.append('contact_on')
        if 'contact_below' in rela_created:
            self.rela_checkers.append(is_contact_below)
            self.rela_names.append('contact_below')

        self.rela_count = {k: 0 for k in count_rela.keys()}

    def exhaustivate(self, coords, vertices, counts_rela):
        coords = np.array(coords)
        N, dim = coords.shape
        assert dim == 2
        assert N == len(vertices)
    
        Y = np.zeros((N,N,len(self.rela_checkers)))

        for i in range(N):
            r_1, c_1 = coords[i]*self.shape
            vertices1 = vertices[i].copy()
            for j in range(i):
                r_2, c_2 = coords[j]*self.shape
                vertices2 = vertices[j].copy()
                for k in range(len(self.rela_checkers)):
                    rela_checker = self.rela_checkers[k]
                    is_rela, rela_code = rela_checker(r_1, c_1, r_2, c_2, vertices1, vertices2)
                    if is_rela:
                        #Y[i,j][k] = rela_code
                        Y[i,j][k] = 1
                        self.rela_count[self.rela_names[k]] += 1
                        counts_rela[self.rela_names[k]] -= 1
                    is_rela, rela_code = rela_checker(r_2, c_2, r_1, c_1, vertices2, vertices1)
                    if is_rela:
                        #Y[j,i][k] = rela_code
                        Y[j,i][k] = 1
                        self.rela_count[self.rela_names[k]] += 1
                        counts_rela[self.rela_names[k]] -= 1
                    
        return Y, counts_rela    
    
    
    
    
    
    
    
    
    
    
    
    
    